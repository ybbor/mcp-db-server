# 🚀 Dynamic Database Connection Guide for Claude

With the enhanced MCP Database Server, you can now connect to any database directly through Claude prompts - no configuration files needed!

## 🎯 Quick Start

### Step 1: Use the Default Configuration

Copy this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dynamic-database": {
      "command": "C:\\path\\to\\python.exe",
      "args": [
        "C:\\path\\to\\mcp_server.py",
        "--database-url",
        "sqlite+aiosqlite:///default.db"
      ]
    }
  }
}
```

### Step 2: Connect to Any Database via Claude Prompts

## 💬 Claude Prompts for Database Operations

### Connect to a New Database

```
Connect me to a SQLite database at path C:/data/students.db

Connect to database: sqlite+aiosqlite:///my_school.db

Connect to PostgreSQL: postgresql+asyncpg://user:password@localhost:5432/students

Switch to database: mysql+aiomysql://admin:pass@myserver:3306/school_data
```

### Get Connection Examples

```
Show me database connection examples

What are the supported database URL formats?

How do I connect to PostgreSQL?
```

### Check Current Connection

```
What database am I currently connected to?

Show current database information

What tables are available in the current database?
```

### Query After Connection

```
After connecting to your database, you can ask:

"List all tables"
"How many students are in the database?"
"Show me sample data from the users table"
"What's the average age of customers?"
```

## 🔗 Database URL Examples

### SQLite (Recommended for Testing)

```
sqlite+aiosqlite:///students.db
sqlite+aiosqlite:///C:/data/school.db
sqlite+aiosqlite:///./local_database.db
```

### PostgreSQL

```
postgresql+asyncpg://username:password@localhost:5432/database_name
postgresql+asyncpg://postgres:admin@127.0.0.1:5432/students_db
postgresql+asyncpg://user:pass@cloud-host.com:5432/production_db
```

### MySQL

```
mysql+aiomysql://username:password@localhost:3306/database_name
mysql+aiomysql://root:admin@mysql-server:3306/students_db
```

## 🎪 Complete Usage Examples

### Example 1: Student Database

```
User: "Connect me to sqlite+aiosqlite:///students.db"
Claude: ✅ Successfully connected! Found 3 tables: students, courses, enrollments

User: "How many students are enrolled?"
Claude: [Executes query and shows results]

User: "Show me students with GPA above 3.5"
Claude: [Shows filtered student data]
```

### Example 2: Multiple Database Switching

```
User: "Show current database info"
Claude: Connected to students.db with 3 tables

User: "Connect to postgresql+asyncpg://admin:pass@server:5432/sales"
Claude: ✅ Connected to PostgreSQL! Found 5 tables: customers, orders, products...

User: "What's the total sales this month?"
Claude: [Queries the sales database]

User: "Switch back to sqlite+aiosqlite:///students.db"
Claude: ✅ Back to student database!
```

### Example 3: Database Exploration

```
User: "Connect to my database at C:/data/company.db"
Claude: ✅ Connected! Found tables: employees, departments, projects

User: "Describe the employees table"
Claude: [Shows table structure with columns and types]

User: "Show me the top 5 highest paid employees"
Claude: [Executes query and formats results]
```

## 🛠️ Available Tools

The MCP server provides these tools for Claude:

1. **`connect_to_database`** - Connect to any database dynamically
2. **`get_connection_examples`** - Show database URL examples
3. **`get_current_database_info`** - Check current connection status
4. **`query_database`** - Natural language queries
5. **`list_tables`** - Show all tables
6. **`describe_table`** - Get table structure
7. **`execute_sql`** - Run direct SQL queries

## 🔒 Security Features

- ✅ **Read-only by default** - No DELETE/DROP operations
- ✅ **Connection validation** - Tests before switching
- ✅ **Error handling** - Graceful failure recovery
- ✅ **URL validation** - Checks supported formats

## 🚨 Common Use Cases

### For Students/Learning

```
"Connect to sqlite+aiosqlite:///practice.db"
"Create a simple query to practice SQL"
"Show me how to join tables"
```

### For Development

```
"Connect to my local development database"
"Check if my new table was created properly"
"Test this query on my database"
```

### For Data Analysis

```
"Connect to the analytics database"
"What's the trend in user signups this month?"
"Show me the correlation between age and purchases"
```

### For Database Administration

```
"Connect to the production database (read-only)"
"Check table sizes and row counts"
"Verify data integrity across tables"
```

## 💡 Tips

1. **Start with SQLite** for testing - no server setup needed
2. **Use full paths** for SQLite files on Windows
3. **Test connection** before running complex queries
4. **Switch databases** as needed during analysis
5. **Ask for examples** if you're unsure about URL format

## 🔧 Troubleshooting

### Connection Issues

```
User: "I can't connect to my database"
Claude: Let me show you connection examples and help debug the URL format
```

### Wrong Database

```
User: "This isn't the right database"
Claude: Let me show you current connection info and help you switch
```

### Query Errors

```
User: "My query isn't working"
Claude: Let me check the current tables and help fix the query
```

---

**🎉 Result: No more config file editing! Just tell Claude which database to connect to and start querying immediately!**
