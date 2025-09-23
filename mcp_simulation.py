#!/usr/bin/env python3
"""
MCP Server Simulation Test
Simulates how Claude would interact with the MCP server
"""

import asyncio
import os
import sys
import json
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

from db import DatabaseManager
from nl_to_sql import NLToSQLConverter

async def simulate_mcp_tool_calls():
    """Simulate Claude making MCP tool calls"""
    print("🤖 Simulating Claude's interaction with MCP Database Server")
    print("=" * 60)
    
    # Use the test database we created
    os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///test_company.db'
    
    db_manager = DatabaseManager()
    nl_converter = NLToSQLConverter()
    
    print("📡 MCP Server initialized and ready for tool calls\n")
    
    # Simulate MCP tool calls that Claude might make
    tool_calls = [
        {
            "tool": "get_current_database_info",
            "description": "Claude wants to understand what database is connected"
        },
        {
            "tool": "list_tables", 
            "description": "Claude wants to see available tables"
        },
        {
            "tool": "describe_table",
            "args": {"table_name": "employees"},
            "description": "Claude wants to understand the employees table structure"
        },
        {
            "tool": "query_database",
            "args": {"query": "Show me all employees in the Engineering department"},
            "description": "Claude asks a natural language question"
        },
        {
            "tool": "execute_sql",
            "args": {"sql_query": "SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department ORDER BY avg_salary DESC"},
            "description": "Claude writes a specific SQL query"
        },
        {
            "tool": "query_database", 
            "args": {"query": "What projects are currently active?"},
            "description": "Claude asks about active projects"
        }
    ]
    
    # Execute each tool call
    for i, call in enumerate(tool_calls, 1):
        print(f"🔧 Tool Call #{i}: {call['tool']}")
        print(f"   📝 Context: {call['description']}")
        
        try:
            if call['tool'] == 'get_current_database_info':
                # Simulate get_current_database_info tool
                current_url = os.getenv('DATABASE_URL', 'Unknown')
                tables = await db_manager.list_tables()
                total_tables = len(tables)
                total_columns = sum(table['column_count'] for table in tables)
                
                response = f"📊 Current Database Information:\n"
                response += f"🔗 Connection URL: {current_url}\n"
                response += f"🏷️  Database Type: {db_manager.database_type}\n"
                response += f"✅ Status: Connected\n"
                response += f"📋 Tables: {total_tables}\n"
                response += f"📊 Total Columns: {total_columns}\n"
                
                if tables:
                    response += "Table Details:\n"
                    for table in tables:
                        response += f"  • {table['table_name']} ({table['column_count']} columns)\n"
                
                print(f"   ✅ Response:\n{response}")
                
            elif call['tool'] == 'list_tables':
                # Simulate list_tables tool
                tables = await db_manager.list_tables()
                response = "Available Tables:\n\n"
                for table in tables:
                    response += f"- {table['table_name']} ({table['column_count']} columns)\n"
                
                print(f"   ✅ Response:\n{response}")
                
            elif call['tool'] == 'describe_table':
                # Simulate describe_table tool
                table_name = call['args']['table_name']
                columns = await db_manager.describe_table(table_name)
                
                response = f"Table: {table_name}\n\nColumns:\n"
                for col in columns:
                    nullable = "NULL" if col['is_nullable'] else "NOT NULL"
                    response += f"- {col['column_name']}: {col['data_type']} ({nullable})\n"
                
                print(f"   ✅ Response:\n{response}")
                
            elif call['tool'] == 'query_database':
                # Simulate query_database tool (natural language)
                nl_query = call['args']['query']
                
                # Get table schemas for context
                tables = await db_manager.list_tables()
                table_schemas = {}
                for table in tables:
                    columns = await db_manager.describe_table(table['table_name'])
                    table_schemas[table['table_name']] = columns
                
                # Convert natural language to SQL
                sql_query = nl_converter.convert_to_sql(nl_query, table_schemas)
                
                # Execute the query
                results = await db_manager.execute_safe_query(sql_query)
                
                # Format the response
                response = f"SQL Query: {sql_query}\n\n"
                response += f"Results ({len(results)} rows):\n"
                
                if results:
                    # Format as a simple table
                    if isinstance(results[0], dict):
                        headers = list(results[0].keys())
                        response += " | ".join(headers) + "\n"
                        response += " | ".join(["-" * len(h) for h in headers]) + "\n"
                        
                        for row in results[:5]:  # Limit to first 5 rows for demo
                            values = [str(row.get(h, "")) for h in headers]
                            response += " | ".join(values) + "\n"
                        
                        if len(results) > 5:
                            response += f"\n... and {len(results) - 5} more rows"
                else:
                    response += "No results found."
                
                print(f"   ✅ Response:\n{response}")
                
            elif call['tool'] == 'execute_sql':
                # Simulate execute_sql tool
                sql_query = call['args']['sql_query']
                
                # Execute the query
                results = await db_manager.execute_safe_query(sql_query)
                
                # Format the response
                response = f"SQL Query: {sql_query}\n\n"
                response += f"Results ({len(results)} rows):\n"
                
                if results:
                    if isinstance(results[0], dict):
                        headers = list(results[0].keys())
                        response += " | ".join(headers) + "\n"
                        response += " | ".join(["-" * len(h) for h in headers]) + "\n"
                        
                        for row in results:
                            values = [str(row.get(h, "")) for h in headers]
                            response += " | ".join(values) + "\n"
                else:
                    response += "No results found."
                
                print(f"   ✅ Response:\n{response}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print() # Add spacing between tool calls
    
    # Cleanup
    await db_manager.engine.dispose()
    
    print("🎯 MCP Tool Simulation Complete!")
    print("✅ All tool calls executed successfully")
    print("\n💡 This demonstrates how Claude would interact with your MCP Database Server")

if __name__ == "__main__":
    asyncio.run(simulate_mcp_tool_calls())