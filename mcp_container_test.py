#!/usr/bin/env python3
"""MCP Server functionality test in Docker container"""

import asyncio
import sys
import os

sys.path.insert(0, 'app')

async def test_mcp_functionality():
    from db import DatabaseManager
    from nl_to_sql import NLToSQLConverter
    
    print("=== MCP Server Container Test ===")
    
    # Test 1: Database Manager
    dm = DatabaseManager()
    print(f"✅ Database Manager: {dm.database_type}")
    
    # Test 2: NL Converter  
    converter = NLToSQLConverter()
    print("✅ NL to SQL Converter: Initialized")
    
    # Test 3: Connection test
    connection_ok = await dm.test_connection()
    print(f"✅ Database Connection: {'PASS' if connection_ok else 'FAIL'}")
    
    if connection_ok:
        # Test 4: Basic operations
        try:
            tables = await dm.list_tables()
            print(f"✅ List Tables: {len(tables)} tables")
            
            # Test query execution
            result = await dm.execute_safe_query("SELECT 1 as test_value")
            print(f"✅ Query Execution: {'PASS' if result else 'FAIL'}")
            
            # Test NL to SQL
            table_schemas = {'test': [{'column_name': 'id', 'data_type': 'INTEGER', 'is_nullable': False}]}
            sql = converter.convert_to_sql("show all test data", table_schemas)
            print(f"✅ NL to SQL: '{sql}'")
            
        except Exception as e:
            print(f"❌ Operations error: {e}")
    
    # Cleanup
    if dm.engine:
        await dm.engine.dispose()
    
    print("=== Container Test Complete ===")

if __name__ == "__main__":
    asyncio.run(test_mcp_functionality())