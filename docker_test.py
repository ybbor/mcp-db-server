#!/usr/bin/env python3
"""Docker container test script"""

import asyncio
import sys
import os

sys.path.insert(0, 'app')

async def test_container():
    from db import DatabaseManager
    
    print("=== Docker Container Database Test ===")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Database URL: {os.getenv('DATABASE_URL', 'Not set')}")
    
    dm = DatabaseManager()
    print(f"Database type: {dm.database_type}")
    
    # Test connection
    result = await dm.test_connection()
    print(f"Connection test: {'PASS' if result else 'FAIL'}")
    
    if result:
        # Test basic operations
        try:
            tables = await dm.list_tables()
            print(f"Tables found: {len(tables)}")
            print("Basic operations: PASS")
        except Exception as e:
            print(f"Basic operations: FAIL - {e}")
    
    # Cleanup
    if dm.engine:
        await dm.engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_container())