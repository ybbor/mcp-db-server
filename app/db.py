"""
Database management utilities for MCP Database Server

Handles connection management, query execution, and safety checks.
"""

import os
import re
import logging
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Conditionally import database drivers (optional; SQLAlchemy handles most)
try:
    import asyncpg  # postgres async driver
except ImportError:
    asyncpg = None

try:
    import pymysql  # mysql driver
except ImportError:
    pymysql = None

try:
    import aiosqlite  # sqlite async driver
except ImportError:
    aiosqlite = None

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self):
        self.database_url = self._get_database_url()
        self.database_type = self._detect_database_type()
        self.engine = None
        self._initialize_engine()
    
    def _get_database_url(self) -> str:
        """Get database URL from environment variables, normalized for async usage"""
        # Priority: explicit full URLs
        db_url = (
            os.getenv("DATABASE_URL")
            or os.getenv("DB_URL")
            or os.getenv("POSTGRES_URL")
            or os.getenv("MYSQL_URL")
            or os.getenv("MSSQL_URL")
            or os.getenv("SQLSERVER_URL")
        )

        # If no full URL, try to construct from discrete parts
        if not db_url:
            db_type = (os.getenv("DB_TYPE") or "postgresql").lower()
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT")
            user = os.getenv("DB_USER", "postgres" if db_type == "postgresql" else "sa")
            password = os.getenv("DB_PASSWORD", "postgres" if db_type == "postgresql" else "YourStrong!Passw0rd")
            database = os.getenv("DB_NAME", "postgres" if db_type == "postgresql" else "master")

            if db_type in ("postgres", "postgresql"):
                port = port or "5432"
                db_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
            elif db_type in ("mysql",):
                port = port or "3306"
                # aiomysql is the async dialect
                db_url = f"mysql+aiomysql://{user}:{password}@{host}:{port}/{database}"
            elif db_type in ("sqlite",):
                # file DB or memory; if DB_NAME holds a path, use it; else :memory:
                if database and database not in ("sqlite", "memory"):
                    db_url = f"sqlite+aiosqlite:///{database}"
                else:
                    db_url = "sqlite+aiosqlite:///:memory:"
            elif db_type in ("mssql", "sqlserver"):
                # Default to pyodbc with Driver 18; trust server cert can be toggled via env
                port = port or "1433"
                driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
                trust = os.getenv("DB_TRUST_SERVER_CERTIFICATE", "yes")
                encrypt = os.getenv("DB_ENCRYPT", "yes")
                # URL-encode spaces in driver automatically handled by SQLAlchemy when using query params
                db_url = (
                    f"mssql+pyodbc://{user}:{password}@{host}:{port}/{database}"
                    f"?driver={driver.replace(' ', '+')}&Encrypt={encrypt}&TrustServerCertificate={trust}"
                )
            else:
                # Fallback to Postgres
                port = port or "5432"
                db_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
        else:
            # Normalize url schemes to async-capable dialects
            if db_url.startswith("postgresql://"):
                db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            elif db_url.startswith("mysql://"):
                db_url = db_url.replace("mysql://", "mysql+aiomysql://", 1)
            elif db_url.startswith(("mssql://", "sqlserver://")):
                # Normalize to mssql+pyodbc; ensure a driver param exists
                db_url = re.sub(r"^(mssql|sqlserver)://", "mssql+pyodbc://", db_url, count=1)
                if "driver=" not in db_url:
                    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server").replace(" ", "+")
                    join_char = "&" if "?" in db_url else "?"
                    db_url = f"{db_url}{join_char}driver={driver}"
                # Sensible secure defaults if not present
                if "Encrypt=" not in db_url:
                    db_url += "&Encrypt=yes"
                if "TrustServerCertificate=" not in db_url:
                    db_url += "&TrustServerCertificate=yes"
            elif db_url.startswith("sqlite://") and "+aiosqlite" not in db_url:
                db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://", 1)

        return db_url
    
    def _detect_database_type(self) -> str:
        """Detect database type from URL"""
        url = self.database_url.lower()
        if "postgresql" in url or "postgres" in url:
            return "postgresql"
        elif "mysql" in url:
            return "mysql"
        elif "sqlite" in url:
            return "sqlite"
        elif "mssql" in url or "sqlserver" in url:
            return "mssql"
        else:
            return "postgresql"  # Default fallback
    
    def _initialize_engine(self):
        """Initialize SQLAlchemy async engine"""
        try:
            self.engine = create_async_engine(
                self.database_url,
                poolclass=NullPool,
                echo=False
            )
            logger.info(f"Database engine initialized for {self.database_type}")
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise
    
    async def test_connection(self) -> bool:
        """Test database connection"""
        try:
            async with self.engine.begin() as conn:
                # A simple cross-DB ping
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    async def list_tables(self) -> List[Dict[str, Any]]:
        """List all tables in the database"""
        try:
            async with self.engine.begin() as conn:
                if self.database_type == "postgresql":
                    query = text("""
                        SELECT 
                            table_name,
                            (SELECT COUNT(*) FROM information_schema.columns 
                             WHERE table_schema = t.table_schema 
                             AND table_name = t.table_name) as column_count
                        FROM information_schema.tables t
                        WHERE table_schema = 'public'
                        AND table_type = 'BASE TABLE'
                        ORDER BY table_name
                    """)
                elif self.database_type == "sqlite":
                    query = text("""
                        SELECT 
                            name as table_name,
                            0 as column_count
                        FROM sqlite_master 
                        WHERE type='table' 
                        AND name NOT LIKE 'sqlite_%'
                        ORDER BY name
                    """)
                elif self.database_type == "mssql":
                    # Use sys.* for better performance; restrict to user tables
                    query = text("""
                        SELECT 
                            t.name AS table_name,
                            COUNT(c.column_id) AS column_count
                        FROM sys.tables AS t
                        LEFT JOIN sys.columns AS c ON c.object_id = t.object_id
                        INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
                        WHERE s.name NOT IN ('sys')
                        GROUP BY t.name
                        ORDER BY t.name
                    """)
                else:  # MySQL
                    query = text("""
                        SELECT 
                            table_name,
                            (SELECT COUNT(*) FROM information_schema.columns 
                             WHERE table_schema = t.table_schema 
                             AND table_name = t.table_name) as column_count
                        FROM information_schema.tables t
                        WHERE table_schema = DATABASE()
                        AND table_type = 'BASE TABLE'
                        ORDER BY table_name
                    """)
                
                result = await conn.execute(query)
                tables = []
                for row in result:
                    # Index-based for broad compatibility
                    table_info = {
                        "table_name": row[0],
                        "column_count": int(row[1]) if len(row) > 1 and row[1] is not None else 0
                    }
                    
                    # For SQLite, compute accurate column_count
                    if self.database_type == "sqlite":
                        col_result = await conn.execute(text(f"PRAGMA table_info({row[0]})"))
                        table_info["column_count"] = len(list(col_result))
                    
                    tables.append(table_info)
                
                return tables
        except Exception as e:
            logger.error(f"Error listing tables: {e}")
            raise
    
    async def describe_table(self, table_name: str) -> List[Dict[str, Any]]:
        """Get column information for a specific table"""
        try:
            async with self.engine.begin() as conn:
                if self.database_type == "postgresql":
                    query = text("""
                        SELECT 
                            column_name,
                            data_type,
                            is_nullable
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                        AND table_name = :table_name
                        ORDER BY ordinal_position
                    """)
                    params = {"table_name": table_name}
                elif self.database_type == "sqlite":
                    result = await conn.execute(text(f"PRAGMA table_info({table_name})"))
                    columns = []
                    for r in result:
                        # pragma returns: cid,name,type,notnull,dflt_value,pk
                        columns.append({
                            "column_name": r[1],
                            "data_type": r[2],
                            "is_nullable": (r[3] == 0)  # notnull==0 means nullable
                        })
                    return columns
                elif self.database_type == "mssql":
                    # Support schema-qualified names; OBJECT_ID handles it
                    query = text("""
                        SELECT 
                            c.name AS column_name,
                            t.name AS data_type,
                            CASE WHEN c.is_nullable = 1 THEN 'YES' ELSE 'NO' END AS is_nullable
                        FROM sys.columns c
                        JOIN sys.types t ON t.user_type_id = c.user_type_id
                        WHERE c.object_id = OBJECT_ID(:tbl)
                        ORDER BY c.column_id
                    """)
                    params = {"tbl": table_name}
                else:  # MySQL
                    query = text("""
                        SELECT 
                            column_name,
                            data_type,
                            is_nullable
                        FROM information_schema.columns
                        WHERE table_schema = DATABASE()
                        AND table_name = :table_name
                        ORDER BY ordinal_position
                    """)
                    params = {"table_name": table_name}
                
                result = await conn.execute(query, params)
                return [
                    {
                        "column_name": row[0],
                        "data_type": row[1],
                        "is_nullable": (str(row[2]).upper() == "YES")
                    }
                    for row in result
                ]
        except Exception as e:
            logger.error(f"Error describing table {table_name}: {e}")
            raise

    def _is_query_safe(self, query: str) -> bool:
        """Check if query is safe (read-only operations only)"""
        # Remove comments and normalize whitespace
        cleaned_query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
        cleaned_query = re.sub(r'/\*.*?\*/', '', cleaned_query, flags=re.DOTALL)
        cleaned_query = ' '.join(cleaned_query.split())
        cleaned_upper = cleaned_query.upper()
        
        # Disallow any data-definition/manipulation or exec
        dangerous_patterns = [
            r'\bDROP\b', r'\bDELETE\b', r'\bINSERT\b', r'\bUPDATE\b',
            r'\bALTER\b', r'\bCREATE\b', r'\bTRUNCATE\b', r'\bREPLACE\b',
            r'\bMERGE\b', r'\bEXEC\b', r'\bEXECUTE\b', r'\bCALL\b',
            r'\bGRANT\b', r'\bREVOKE\b'
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, cleaned_upper):
                return False
        
        # Must start with SELECT (allow leading CTEs)
        if not re.match(r'^\s*(WITH\s+.*?\)\s*)?SELECT\b', cleaned_upper):
            return False
        
        return True

    def _apply_limit(self, query: str, limit: int) -> str:
        """Apply a row limit in a database-appropriate way."""
        q = query.strip().rstrip(';')
        upper = q.upper().lstrip()

        # If query already has a limiting construct, leave it
        has_limit = (
            re.search(r'\bLIMIT\s+\d+\b', upper) or
            re.match(r'^SELECT\s+TOP\s+\d+\b', upper) or
            re.search(r'\bFETCH\s+NEXT\s+\d+\s+ROWS\s+ONLY\b', upper)  # OFFSET/FETCH
        )
        if has_limit:
            # For existing LIMIT in non-MSSQL, replace with requested limit
            if self.database_type in ("postgresql", "mysql", "sqlite"):
                q = re.sub(r'\bLIMIT\s+\d+\b', f'LIMIT {limit}', q, flags=re.IGNORECASE)
            elif self.database_type == "mssql":
                # If it's FETCH NEXT, replace the number
                q = re.sub(r'(\bFETCH\s+NEXT\s+)\d+(\s+ROWS\s+ONLY\b)', rf'\g<1>{limit}\g<2>', q, flags=re.IGNORECASE)
                q = re.sub(r'(^\s*SELECT\s+TOP\s+)\d+(\b)', rf'\g<1>{limit}\g<2>', q, flags=re.IGNORECASE)
            return q

        # Apply new limit
        if self.database_type in ("postgresql", "mysql", "sqlite"):
            return f"{q} LIMIT {limit}"
        elif self.database_type == "mssql":
            # Robust wrap to preserve ORDER BY etc.
            return f"SELECT TOP {limit} * FROM ({q}) AS _sub"
        else:
            return f"{q} LIMIT {limit}"

    async def execute_safe_query(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Execute a query with safety checks"""
        if not self._is_query_safe(query):
            raise ValueError("Query contains unsafe operations. Only SELECT queries are allowed.")
        
        limited_query = self._apply_limit(query, limit)
        
        try:
            async with self.engine.begin() as conn:
                result = await conn.execute(text(limited_query))
                
                # Convert rows to dictionaries
                rows = []
                keys = result.keys()
                for row in result:
                    row_dict = {}
                    for i, col in enumerate(keys):
                        value = row[i]
                        if hasattr(value, 'isoformat'):
                            value = value.isoformat()
                        elif hasattr(value, '__str__') and not isinstance(value, (str, int, float, bool, type(None))):
                            value = str(value)
                        row_dict[col] = value
                    rows.append(row_dict)
                return rows
                
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    async def execute_unsafe_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute any SQL query without safety restrictions (allows CREATE, DELETE, INSERT, etc.)"""
        try:
            async with self.engine.begin() as conn:
                result = await conn.execute(text(query))

                if result.returns_rows:
                    rows = []
                    keys = result.keys()
                    for row in result:
                        row_dict = {}
                        for i, col in enumerate(keys):
                            value = row[i]
                            if hasattr(value, 'isoformat'):
                                value = value.isoformat()
                            elif hasattr(value, '__str__') and not isinstance(value, (str, int, float, bool, type(None))):
                                value = str(value)
                            row_dict[col] = value
                        rows.append(row_dict)
                    return rows
                else:
                    return [{"affected_rows": result.rowcount, "status": "success", "query_type": "modification"}]

        except Exception as e:
            logger.error(f"Error executing unsafe query: {e}")
            raise

# Global database manager instance
_db_manager: Optional[DatabaseManager] = None

async def get_db_manager() -> DatabaseManager:
    """Dependency to get database manager instance"""
    global _db_manager
    
    if _db_manager is None:
        _db_manager = DatabaseManager()
        if not await _db_manager.test_connection():
            raise Exception("Cannot connect to database")
    
    return _db_manager

async def cleanup_db_manager():
    """Cleanup database manager"""
    global _db_manager
    
    if _db_manager and _db_manager.engine:
        await _db_manager.engine.dispose()
        _db_manager = None
