#!/usr/bin/env python3
"""Test script for MCP server tools"""

import asyncio
import os
import sys
from pathlib import Path
from sqlalchemy import text

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

from db import DatabaseManager
from nl_to_sql import NLToSQLConverter

async def test_mcp_tools():
    """Test the main MCP server tools"""
    print("=== Testing MCP Database Server Tools ===\n")
    
    # Set up test database
    os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///test_students.db'
    
    # Initialize components
    db_manager = DatabaseManager()
    nl_converter = NLToSQLConverter()
    
    print(f"✅ Database URL: {db_manager.database_url}")
    print(f"✅ Database Type: {db_manager.database_type}")
    
    # Test connection
    connection_ok = await db_manager.test_connection()
    print(f"✅ Connection test: {'PASS' if connection_ok else 'FAIL'}")
    
    if not connection_ok:
        print("❌ Database connection failed, stopping tests")
        return
    
    # Create a test table with sample data
    print("\n=== Setting up test data ===")
    try:
        async with db_manager.engine.begin() as conn:
            # Create students table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER,
                    grade TEXT,
                    email TEXT
                )
            """))
            
            # Insert sample data
            await conn.execute(text("""
                INSERT OR REPLACE INTO students (id, name, age, grade, email) VALUES
                (1, 'John Doe', 20, 'A', 'john@example.com'),
                (2, 'Jane Smith', 19, 'B+', 'jane@example.com'),
                (3, 'Bob Johnson', 21, 'A-', 'bob@example.com'),
                (4, 'Alice Brown', 18, 'A+', 'alice@example.com'),
                (5, 'Charlie Wilson', 22, 'B', 'charlie@example.com')
            """))
            print("✅ Test table created and populated")
    except Exception as e:
        print(f"❌ Error setting up test data: {e}")
        return
    
    # Test list_tables functionality
    print("\n=== Testing list_tables ===")
    try:
        tables = await db_manager.list_tables()
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table['table_name']} ({table['column_count']} columns)")
    except Exception as e:
        print(f"❌ Error listing tables: {e}")
    
    # Test describe_table functionality
    print("\n=== Testing describe_table ===")
    try:
        if tables:
            table_name = tables[0]['table_name']
            columns = await db_manager.describe_table(table_name)
            print(f"✅ Table '{table_name}' schema:")
            for col in columns:
                nullable = "NULL" if col['is_nullable'] else "NOT NULL"
                print(f"  - {col['column_name']}: {col['data_type']} ({nullable})")
    except Exception as e:
        print(f"❌ Error describing table: {e}")
    
    # Test execute_safe_query functionality
    print("\n=== Testing execute_safe_query ===")
    try:
        results = await db_manager.execute_safe_query("SELECT * FROM students")
        print(f"✅ Query executed successfully, {len(results)} rows returned")
        if results:
            print("Sample result:")
            print(f"  {results[0]}")
    except Exception as e:
        print(f"❌ Error executing query: {e}")
    
    # Test NL to SQL conversion
    print("\n=== Testing NL to SQL conversion ===")
    try:
        # Get table schemas for context
        table_schemas = {}
        for table in tables:
            columns = await db_manager.describe_table(table['table_name'])
            table_schemas[table['table_name']] = columns
        
        test_queries = [
            "Show all students",
            "Count the number of students",
            "Get the first 3 students"
        ]
        
        for nl_query in test_queries:
            try:
                sql_query = nl_converter.convert_to_sql(nl_query, table_schemas)
                print(f"✅ '{nl_query}' -> '{sql_query}'")
                
                # Test execution
                results = await db_manager.execute_safe_query(sql_query)
                print(f"   Executed successfully, {len(results)} rows")
            except Exception as e:
                print(f"❌ '{nl_query}' -> Error: {e}")
                
    except Exception as e:
        print(f"❌ Error in NL to SQL testing: {e}")
    
    # Test safety features
    print("\n=== Testing safety features ===")
    dangerous_queries = [
        "DROP TABLE students",
        "DELETE FROM students",
        "UPDATE students SET name = 'hacked'",
        "INSERT INTO students VALUES (999, 'test', 99, 'F', 'test@test.com')"
    ]
    
    for dangerous_query in dangerous_queries:
        try:
            await db_manager.execute_safe_query(dangerous_query)
            print(f"❌ Dangerous query '{dangerous_query}' was allowed!")
        except ValueError as e:
            print(f"✅ Dangerous query '{dangerous_query}' was blocked: {str(e)[:50]}...")
        except Exception as e:
            print(f"❓ Unexpected error for '{dangerous_query}': {e}")
    
    # Clean up
    await db_manager.engine.dispose()
    print(f"\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())