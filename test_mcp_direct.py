#!/usr/bin/env python3
"""
Test MCP server NLP functionality directly (not via HTTP)
"""

import asyncio
import os
import sys
import logging

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from db import DatabaseManager
from nl_to_sql import NLToSQLConverter

# Set up logging
logging.basicConfig(level=logging.INFO)

async def test_mcp_nlp_functionality():
    """Test the MCP server NLP functionality directly"""
    print("🧪 Testing MCP Server NLP Functionality (Direct)")
    print("=" * 50)
    
    # Set database URL
    os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///test.db'
    
    try:
        # Initialize components like in MCP server
        print("🔧 Initializing database manager...")
        db_manager = DatabaseManager()
        await db_manager.test_connection()
        print("✅ Database connection successful")
        
        print("🔧 Initializing NL converter...")
        nl_converter = NLToSQLConverter()
        print("✅ NL converter initialized")
        
        # Test the exact same logic as in the MCP server
        print("\n🧪 Testing NLP Query Processing")
        print("-" * 30)
        
        test_queries = [
            "show me all customers",
            "count all orders", 
            "list the products",
            "show top 5 customers"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\nTest {i}: '{query}'")
            try:
                # Get table schemas for context (same as MCP server)
                tables = await db_manager.list_tables()
                table_schemas = {}
                for table in tables:
                    columns = await db_manager.describe_table(table['table_name'])
                    table_schemas[table['table_name']] = columns
                
                # Convert natural language to SQL (FIXED: no await)
                sql_query = nl_converter.convert_to_sql(query, table_schemas)
                
                # Execute the query
                results = await db_manager.execute_safe_query(sql_query)
                
                print(f"   ✅ Success!")
                print(f"   ➜ Generated SQL: {sql_query}")
                print(f"   ➜ Row Count: {len(results)}")
                
                # Show first few results
                if results and len(results) > 0:
                    print(f"   ➜ Sample Result: {results[0]}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print(f"   ➜ Exception Type: {type(e).__name__}")
    
    except Exception as e:
        print(f"❌ Setup Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_nlp_functionality())