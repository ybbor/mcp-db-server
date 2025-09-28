#!/usr/bin/env python3
"""Test database type detection without initializing engines"""

def test_detection(url):
    """Test database type detection logic"""
    # Parse the URL scheme to determine database type
    url_lower = url.lower()
    
    # Extract the scheme part (before ://)
    if '://' in url_lower:
        scheme = url_lower.split('://')[0]
    else:
        scheme = url_lower
    
    # Check scheme for database type
    if scheme.startswith('postgresql') or scheme.startswith('postgres'):
        return "postgresql"
    elif scheme.startswith('mysql'):
        return "mysql"
    elif scheme.startswith('sqlite'):
        return "sqlite"
    else:
        # Fallback: check for keywords in scheme only (not filename)
        if 'postgresql' in scheme or 'postgres' in scheme:
            return "postgresql"
        elif 'mysql' in scheme:
            return "mysql"
        elif 'sqlite' in scheme:
            return "sqlite"
        else:
            return "postgresql"  # Default fallback

# Test cases
test_urls = [
    'postgresql://user:password@localhost:5432/testdb',
    'postgres://user:password@localhost:5432/testdb', 
    'postgresql+asyncpg://user:password@localhost:5432/testdb',
    'mysql+aiomysql://user:password@localhost:3306/testdb',
    'mysql://user:password@localhost:3306/testdb',
    'sqlite:///test.db',
    'sqlite+aiosqlite:///test.db',
    'sqlite+aiosqlite:///test_postgresql_fix.db',  # This was our problematic case
]

print("Database Type Detection Test:")
print("=" * 50)

for url in test_urls:
    detected_type = test_detection(url)
    print(f"URL: {url}")
    print(f"  -> Detected: {detected_type}")
    print()