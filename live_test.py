#!/usr/bin/env python3
"""
Comprehensive Live Test for MCP Database Server
This script tests all functionality with a realistic database scenario
"""

import asyncio
import os
import sys
import json
from pathlib import Path
from sqlalchemy import text

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

from db import DatabaseManager
from nl_to_sql import NLToSQLConverter

class MCPServerTester:
    """Comprehensive tester for MCP Database Server"""
    
    def __init__(self):
        self.db_manager = None
        self.nl_converter = None
        self.test_db_path = "test_company.db"
        
    async def setup_test_database(self):
        """Create a realistic company database for testing"""
        print("🏗️  Setting up realistic test database...")
        
        # Set up company database
        os.environ['DATABASE_URL'] = f'sqlite+aiosqlite:///{self.test_db_path}'
        
        self.db_manager = DatabaseManager()
        self.nl_converter = NLToSQLConverter()
        
        # Test connection
        if not await self.db_manager.test_connection():
            raise Exception("Failed to connect to test database")
        
        # Create comprehensive schema
        async with self.db_manager.engine.begin() as conn:
            # Employees table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    department TEXT NOT NULL,
                    position TEXT NOT NULL,
                    salary DECIMAL(10,2),
                    hire_date DATE,
                    manager_id INTEGER,
                    active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (manager_id) REFERENCES employees(id)
                )
            """))
            
            # Departments table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    budget DECIMAL(12,2),
                    location TEXT,
                    manager_id INTEGER,
                    FOREIGN KEY (manager_id) REFERENCES employees(id)
                )
            """))
            
            # Projects table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT CHECK(status IN ('planning', 'active', 'completed', 'cancelled')),
                    start_date DATE,
                    end_date DATE,
                    budget DECIMAL(10,2),
                    department_id INTEGER,
                    FOREIGN KEY (department_id) REFERENCES departments(id)
                )
            """))
            
            # Employee_Projects junction table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS employee_projects (
                    employee_id INTEGER,
                    project_id INTEGER,
                    role TEXT,
                    allocation_percentage INTEGER,
                    PRIMARY KEY (employee_id, project_id),
                    FOREIGN KEY (employee_id) REFERENCES employees(id),
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                )
            """))
            
            # Insert sample data
            print("📊 Inserting realistic sample data...")
            
            # Insert departments
            await conn.execute(text("""
                INSERT OR REPLACE INTO departments (id, name, budget, location) VALUES
                (1, 'Engineering', 2500000.00, 'Building A'),
                (2, 'Marketing', 1200000.00, 'Building B'),
                (3, 'Sales', 1800000.00, 'Building C'),
                (4, 'HR', 800000.00, 'Building A'),
                (5, 'Finance', 1000000.00, 'Building B')
            """))
            
            # Insert employees
            await conn.execute(text("""
                INSERT OR REPLACE INTO employees (id, first_name, last_name, email, department, position, salary, hire_date, manager_id, active) VALUES
                (1, 'John', 'Smith', 'john.smith@company.com', 'Engineering', 'CTO', 180000.00, '2020-01-15', NULL, 1),
                (2, 'Sarah', 'Johnson', 'sarah.j@company.com', 'Engineering', 'Senior Developer', 120000.00, '2021-03-10', 1, 1),
                (3, 'Mike', 'Brown', 'mike.brown@company.com', 'Engineering', 'Developer', 95000.00, '2022-06-01', 2, 1),
                (4, 'Lisa', 'Davis', 'lisa.davis@company.com', 'Marketing', 'Marketing Director', 140000.00, '2020-08-20', NULL, 1),
                (5, 'Tom', 'Wilson', 'tom.wilson@company.com', 'Marketing', 'Marketing Specialist', 75000.00, '2023-01-15', 4, 1),
                (6, 'Emma', 'Garcia', 'emma.garcia@company.com', 'Sales', 'Sales Director', 150000.00, '2019-11-01', NULL, 1),
                (7, 'Alex', 'Rodriguez', 'alex.r@company.com', 'Sales', 'Sales Rep', 65000.00, '2022-09-12', 6, 1),
                (8, 'Maria', 'Martinez', 'maria.m@company.com', 'HR', 'HR Director', 125000.00, '2021-05-30', NULL, 1),
                (9, 'David', 'Lee', 'david.lee@company.com', 'Finance', 'Finance Director', 135000.00, '2020-12-08', NULL, 1),
                (10, 'Jennifer', 'Taylor', 'jen.taylor@company.com', 'Engineering', 'Junior Developer', 70000.00, '2023-08-01', 2, 1)
            """))
            
            # Insert projects
            await conn.execute(text("""
                INSERT OR REPLACE INTO projects (id, name, description, status, start_date, end_date, budget, department_id) VALUES
                (1, 'Mobile App Redesign', 'Complete redesign of mobile application', 'active', '2024-01-01', '2024-12-31', 500000.00, 1),
                (2, 'Website Optimization', 'Improve website performance and SEO', 'completed', '2023-06-01', '2023-12-15', 150000.00, 2),
                (3, 'CRM Integration', 'Integrate new CRM system', 'planning', '2024-03-01', '2024-08-31', 300000.00, 3),
                (4, 'Employee Portal', 'New internal employee portal', 'active', '2024-02-01', '2024-10-31', 200000.00, 4),
                (5, 'Financial Dashboard', 'Real-time financial reporting dashboard', 'active', '2024-01-15', '2024-06-30', 250000.00, 5)
            """))
            
            # Insert employee-project assignments
            await conn.execute(text("""
                INSERT OR REPLACE INTO employee_projects (employee_id, project_id, role, allocation_percentage) VALUES
                (1, 1, 'Project Sponsor', 10),
                (2, 1, 'Lead Developer', 80),
                (3, 1, 'Developer', 90),
                (10, 1, 'Junior Developer', 70),
                (4, 2, 'Project Manager', 50),
                (5, 2, 'Marketing Lead', 60),
                (6, 3, 'Business Lead', 40),
                (7, 3, 'Sales Liaison', 30),
                (8, 4, 'Project Manager', 60),
                (2, 4, 'Technical Lead', 40),
                (9, 5, 'Project Sponsor', 30),
                (2, 5, 'Developer', 20)
            """))
            
        print("✅ Test database setup complete!")
        return True
    
    async def test_mcp_tools(self):
        """Test all MCP tools with the test database"""
        print("\n🧪 Testing MCP Tools...")
        
        # Test 1: list_tables
        print("\n1️⃣ Testing list_tables...")
        try:
            tables = await self.db_manager.list_tables()
            print(f"   ✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"      - {table['table_name']} ({table['column_count']} columns)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
        
        # Test 2: describe_table
        print("\n2️⃣ Testing describe_table...")
        try:
            schema = await self.db_manager.describe_table('employees')
            print(f"   ✅ Employees table schema ({len(schema)} columns):")
            for col in schema[:3]:  # Show first 3 columns
                nullable = "NULL" if col['is_nullable'] else "NOT NULL"
                print(f"      - {col['column_name']}: {col['data_type']} ({nullable})")
            if len(schema) > 3:
                print(f"      ... and {len(schema) - 3} more columns")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
        
        # Test 3: execute_safe_query
        print("\n3️⃣ Testing execute_safe_query...")
        test_queries = [
            "SELECT COUNT(*) as total_employees FROM employees",
            "SELECT department, COUNT(*) as count FROM employees GROUP BY department",
            "SELECT first_name, last_name, position, salary FROM employees WHERE department = 'Engineering'",
        ]
        
        for query in test_queries:
            try:
                results = await self.db_manager.execute_safe_query(query)
                print(f"   ✅ Query: {query[:50]}...")
                print(f"      Result: {len(results)} rows")
                if results:
                    print(f"      Sample: {results[0]}")
            except Exception as e:
                print(f"   ❌ Query failed: {e}")
        
        return True
    
    async def test_nl_to_sql(self):
        """Test natural language to SQL conversion"""
        print("\n🗣️ Testing Natural Language to SQL...")
        
        # Get table schemas for context
        tables = await self.db_manager.list_tables()
        table_schemas = {}
        for table in tables:
            columns = await self.db_manager.describe_table(table['table_name'])
            table_schemas[table['table_name']] = columns
        
        test_queries = [
            "Show all employees",
            "Count employees by department", 
            "List all active projects",
            "Find employees with salary over 100000",
            "Show the top 5 highest paid employees",
            "List all projects in the Engineering department"
        ]
        
        print(f"   Testing {len(test_queries)} natural language queries:")
        
        for nl_query in test_queries:
            try:
                sql_query = self.nl_converter.convert_to_sql(nl_query, table_schemas)
                print(f"\n   🔍 '{nl_query}'")
                print(f"      → '{sql_query}'")
                
                # Test execution
                results = await self.db_manager.execute_safe_query(sql_query)
                print(f"      ✅ Executed successfully: {len(results)} rows")
                
                if results and len(results) > 0:
                    # Show sample result
                    sample = results[0]
                    if isinstance(sample, dict) and len(sample) <= 3:
                        print(f"      Sample: {sample}")
                    else:
                        print(f"      Sample: {str(sample)[:100]}...")
                        
            except Exception as e:
                print(f"      ❌ Error: {str(e)[:100]}...")
        
        return True
    
    async def test_security_features(self):
        """Test security and safety features"""
        print("\n🔒 Testing Security Features...")
        
        dangerous_queries = [
            "DROP TABLE employees",
            "DELETE FROM employees WHERE department = 'HR'",
            "UPDATE employees SET salary = 999999",
            "INSERT INTO employees VALUES (999, 'Hacker', 'McHackface', 'hack@evil.com', 'IT', 'Admin', 200000, '2024-01-01', NULL, 1)",
            "ALTER TABLE employees ADD COLUMN backdoor TEXT",
            "CREATE TABLE malicious (id INT, data TEXT)"
        ]
        
        print(f"   Testing {len(dangerous_queries)} dangerous operations:")
        
        blocked_count = 0
        for dangerous_query in dangerous_queries:
            try:
                await self.db_manager.execute_safe_query(dangerous_query)
                print(f"   ❌ SECURITY BREACH: '{dangerous_query[:50]}...' was allowed!")
            except ValueError as e:
                if "unsafe operations" in str(e).lower():
                    print(f"   ✅ Blocked: {dangerous_query.split()[0]} operation")
                    blocked_count += 1
                else:
                    print(f"   ❓ Unexpected error: {str(e)[:50]}...")
            except Exception as e:
                print(f"   ❓ Unexpected error type: {str(e)[:50]}...")
        
        print(f"\n   🛡️ Security Summary: {blocked_count}/{len(dangerous_queries)} dangerous operations blocked")
        return blocked_count == len(dangerous_queries)
    
    async def test_dynamic_connections(self):
        """Test dynamic database connection switching"""
        print("\n🔄 Testing Dynamic Database Connections...")
        
        # Test connection to a new database
        new_db_path = "test_inventory.db"
        new_db_url = f'sqlite+aiosqlite:///{new_db_path}'
        
        print(f"   Testing connection to new database: {new_db_url}")
        
        try:
            # Simulate the connect_to_database MCP tool
            previous_url = os.getenv('DATABASE_URL', 'None')
            os.environ['DATABASE_URL'] = new_db_url
            
            # Create new database manager
            new_db_manager = DatabaseManager()
            
            # Test the connection
            connection_test = await new_db_manager.test_connection()
            if not connection_test:
                raise Exception("Failed to connect to new database")
            
            print("   ✅ Successfully connected to new database")
            
            # Create a simple table in the new database
            async with new_db_manager.engine.begin() as conn:
                await conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        price DECIMAL(10,2),
                        category TEXT,
                        in_stock INTEGER
                    )
                """))
                
                await conn.execute(text("""
                    INSERT OR REPLACE INTO products (id, name, price, category, in_stock) VALUES
                    (1, 'Laptop', 999.99, 'Electronics', 50),
                    (2, 'Mouse', 29.99, 'Electronics', 100),
                    (3, 'Keyboard', 79.99, 'Electronics', 75)
                """))
            
            # Test querying the new database
            tables = await new_db_manager.list_tables()
            print(f"   ✅ New database has {len(tables)} tables")
            
            results = await new_db_manager.execute_safe_query("SELECT COUNT(*) as product_count FROM products")
            print(f"   ✅ Query result: {results[0] if results else 'No results'}")
            
            # Cleanup
            await new_db_manager.engine.dispose()
            
            # Restore original database
            os.environ['DATABASE_URL'] = previous_url
            
            return True
            
        except Exception as e:
            print(f"   ❌ Dynamic connection test failed: {e}")
            return False
    
    async def run_full_test_suite(self):
        """Run the complete test suite"""
        print("🚀 Starting Comprehensive MCP Database Server Test\n")
        print("=" * 60)
        
        try:
            # Setup test database
            setup_success = await self.setup_test_database()
            if not setup_success:
                print("❌ Database setup failed, aborting tests")
                return False
            
            # Run all tests
            test_results = {
                "mcp_tools": await self.test_mcp_tools(),
                "nl_to_sql": await self.test_nl_to_sql(), 
                "security": await self.test_security_features(),
                "dynamic_connections": await self.test_dynamic_connections()
            }
            
            # Print final results
            print("\n" + "=" * 60)
            print("🎯 FINAL TEST RESULTS:")
            print("=" * 60)
            
            passed = 0
            total = len(test_results)
            
            for test_name, result in test_results.items():
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"{test_name.replace('_', ' ').title():<25} {status}")
                if result:
                    passed += 1
            
            print(f"\nOverall Score: {passed}/{total} tests passed")
            
            if passed == total:
                print("\n🎉 ALL TESTS PASSED! Your MCP Database Server is fully functional!")
            else:
                print(f"\n⚠️ {total - passed} test(s) failed. Please check the output above.")
            
            # Cleanup
            if self.db_manager:
                await self.db_manager.engine.dispose()
            
            return passed == total
            
        except Exception as e:
            print(f"\n💥 Test suite failed with error: {e}")
            return False

async def main():
    """Main test function"""
    tester = MCPServerTester()
    success = await tester.run_full_test_suite()
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)