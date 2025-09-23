#!/usr/bin/env python3
"""
Test script for unsafe database operations
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

from db import DatabaseManager

async def test_unsafe_operations():
    """Test unsafe database operations"""
    
    # Set up test database
    os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///C:/Users/kundu/Desktop/Projects/Proj/MCP/mcp-db-server/data/test_unsafe.db'
    
    db = DatabaseManager()
    
    print("🔧 Testing unsafe database operations...")
    
    try:
        # Test connection
        print("1. Testing connection...")
        assert await db.test_connection(), "Database connection failed"
        print("   ✅ Connected successfully")
        
        # Test CREATE TABLE
        print("\n2. Testing CREATE TABLE...")
        create_result = await db.execute_unsafe_query("""
            CREATE TABLE IF NOT EXISTS test_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print(f"   ✅ Create table result: {create_result}")
        
        # Test INSERT
        print("\n3. Testing INSERT...")
        insert_result = await db.execute_unsafe_query("""
            INSERT INTO test_users (name, email, age) 
            VALUES ('John Doe', 'john@example.com', 30)
        """)
        print(f"   ✅ Insert result: {insert_result}")
        
        # Test another INSERT
        insert_result2 = await db.execute_unsafe_query("""
            INSERT INTO test_users (name, email, age) 
            VALUES ('Jane Smith', 'jane@example.com', 25)
        """)
        print(f"   ✅ Insert result 2: {insert_result2}")
        
        # Test SELECT to verify data
        print("\n4. Testing SELECT...")
        select_result = await db.execute_unsafe_query("SELECT * FROM test_users")
        print(f"   ✅ Select result: {len(select_result)} rows found")
        for row in select_result:
            print(f"      - {row}")
        
        # Test UPDATE
        print("\n5. Testing UPDATE...")
        update_result = await db.execute_unsafe_query("""
            UPDATE test_users SET age = 31 WHERE name = 'John Doe'
        """)
        print(f"   ✅ Update result: {update_result}")
        
        # Test DELETE
        print("\n6. Testing DELETE...")
        delete_result = await db.execute_unsafe_query("""
            DELETE FROM test_users WHERE name = 'Jane Smith'
        """)
        print(f"   ✅ Delete result: {delete_result}")
        
        # Verify final state
        print("\n7. Verifying final state...")
        final_result = await db.execute_unsafe_query("SELECT * FROM test_users")
        print(f"   ✅ Final rows: {len(final_result)}")
        for row in final_result:
            print(f"      - {row}")
        
        print("\n🎉 All unsafe operations test passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_unsafe_operations())