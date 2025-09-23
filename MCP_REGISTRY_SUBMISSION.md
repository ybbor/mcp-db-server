# MCP Registry Submission Guide

## Option 1: Official MCP Registry (Anthropic/Claude)

### Requirements:
- Public GitHub repository ✅
- Proper MCP server implementation ✅
- Documentation and examples ✅
- Docker image published ✅

### Submission Process:
1. **Visit:** https://github.com/modelcontextprotocol/servers
2. **Fork the repository**
3. **Add your server to the registry:**
   - Create entry in `src/servers.json`
   - Add documentation in `src/content/servers/`
4. **Submit Pull Request**

### Registry Entry Format:
```json
{
  "name": "database-server",
  "displayName": "Database Server",
  "description": "Multi-database MCP server with natural language SQL queries",
  "author": "Souhardya Kundu",
  "homepage": "https://github.com/Souhar-dya/mcp-db-server",
  "sourceUrl": "https://github.com/Souhar-dya/mcp-db-server",
  "npmPackage": null,
  "pythonPackage": null,
  "dockerImage": "souhardyak/mcp-db-server",
  "capabilities": ["database", "natural-language", "multi-database"],
  "categories": ["database", "productivity"],
  "keywords": ["database", "sql", "postgresql", "mysql", "sqlite", "natural-language"],
  "configuration": {
    "required": ["DATABASE_URL"],
    "optional": ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"]
  }
}
```

## Option 2: Community Docker Registries

### MCPHub (Community Registry)
- **Website:** https://mcphub.io (if exists)
- **Process:** Submit via web form or GitHub issue

### Docker Hub Official Images
- **Requirements:** Very strict, high usage
- **Process:** Submit to https://github.com/docker-library/official-images

## Option 3: Self-Hosted Registry

### Create Your Own MCP Registry
```yaml
# registry.yml
servers:
  - name: "mcp-db-server"
    image: "souhardyak/mcp-db-server:latest"
    description: "Database server with natural language queries"
    capabilities: ["database", "natural-language"]
```

## Recommended Submission Strategy

1. **Start with Docker Hub** (automatic via GitHub Actions)
2. **Submit to Official MCP Registry** (for maximum visibility)
3. **Consider community registries** (for additional exposure)

## Docker Hub Publishing Commands (Manual)

If you want to publish manually:

```bash
# Build and tag
docker build -t souhardyak/mcp-db-server:latest .
docker build -t souhardyak/mcp-db-server:v1.0.0 .

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push souhardyak/mcp-db-server:latest
docker push souhardyak/mcp-db-server:v1.0.0
```

## Usage Examples for Registry

### Docker Compose
```yaml
version: '3.8'
services:
  mcp-db-server:
    image: souhardyak/mcp-db-server:latest
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    ports:
      - "3000:3000"
```

### Claude Desktop Configuration
```json
{
  "mcpServers": {
    "database-server": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "DATABASE_URL=sqlite:///data/my.db",
        "souhardyak/mcp-db-server:latest"
      ]
    }
  }
}
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-db-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mcp-db-server
  template:
    metadata:
      labels:
        app: mcp-db-server
    spec:
      containers:
      - name: mcp-db-server
        image: souhardyak/mcp-db-server:latest
        env:
        - name: DATABASE_URL
          value: "postgresql://user:pass@db:5432/mydb"
        ports:
        - containerPort: 3000
```

## Next Steps

1. ✅ Add GitHub Secrets for Docker Hub
2. ✅ Automatic Docker publishing will start
3. 📝 Prepare official MCP registry submission
4. 🌟 Promote your server in MCP community