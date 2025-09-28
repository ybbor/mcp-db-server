#!/usr/bin/env python3
"""
Simple test to verify the MCP server async fix
"""

import asyncio
import os

# Test the exact problematic line that was fixed
async def test_async_fix():
    """Test that we can call non-async method without await"""
    
    # Set up the environment
    os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///test.db'
    
    # Import after setting environment
    import sys
    sys.path.insert(0, 'app')
    
    from nl_to_sql import NLToSQLConverter
    from db import DatabaseManager
    
    print("🧪 Testing Async Fix")
    print("=" * 30)
    
    # Initialize components
    nl_converter = NLToSQLConverter()
    db_manager = DatabaseManager()
    
    # Test database connection
    connection_ok = await db_manager.test_connection()
    print(f"Database connection: {'✅ OK' if connection_ok else '❌ Failed'}")
    
    # Get table schemas
    tables = await db_manager.list_tables()
    table_schemas = {}
    for table in tables:
        columns = await db_manager.describe_table(table['table_name'])
        table_schemas[table['table_name']] = columns
    
    print(f"Found {len(tables)} tables: {[t['table_name'] for t in tables]}")
    
    # Test the FIXED line (no await on non-async method)
    try:
        query = "show me all customers"
        print(f"\n🔍 Testing: '{query}'")
        
        # This is the line that was causing the error before the fix
        sql_query = nl_converter.convert_to_sql(query, table_schemas)  # ✅ Fixed: No await
        
        print(f"✅ SQL Generated: {sql_query}")
        
        # Test query execution
        results = await db_manager.execute_safe_query(sql_query, limit=3)
        print(f"✅ Query Executed: {len(results)} rows returned")
        
        if results:
            print(f"✅ Sample Data: {results[0]}")
        
        print(f"\n🎉 Async Fix Successful! No 'str can't be used in await' error!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"❌ Error Type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(test_async_fix())