#!/bin/bash

# MCP Database Server - Docker Registry Publishing Script
# Usage: ./publish-docker.sh [version] [dockerhub-username]

set -e

VERSION=${1:-"1.0.0"}
DOCKERHUB_USER=${2:-"souhardyak"}
IMAGE_NAME="mcp-database-server"
FULL_IMAGE="$DOCKERHUB_USER/$IMAGE_NAME"

echo "🚀 Publishing MCP Database Server to Docker Registry"
echo "Version: $VERSION"
echo "Docker Hub User: $DOCKERHUB_USER"
echo "Full Image Name: $FULL_IMAGE"

# Ensure we're in the correct directory
if [ ! -f "mcp_server.py" ]; then
    echo "❌ Error: mcp_server.py not found. Please run from project root."
    exit 1
fi

# Build the image
echo "📦 Building Docker image..."
docker build -t $IMAGE_NAME:latest .
docker build -t $IMAGE_NAME:$VERSION .

# Tag for Docker Hub
echo "🏷️  Tagging images..."
docker tag $IMAGE_NAME:latest $FULL_IMAGE:latest
docker tag $IMAGE_NAME:$VERSION $FULL_IMAGE:$VERSION

# Test the image
echo "🧪 Testing the image..."
docker run --rm $FULL_IMAGE:latest python -c "
import sys
sys.path.insert(0, 'app')
from mcp_server import initialize_database
print('✅ Image test passed!')
"

# Login to Docker Hub (interactive)
echo "🔐 Please login to Docker Hub..."
docker login

# Push to Docker Hub
echo "📤 Pushing to Docker Hub..."
docker push $FULL_IMAGE:latest
docker push $FULL_IMAGE:$VERSION

# Verify the push
echo "✅ Verifying pushed images..."
docker run --rm $FULL_IMAGE:latest python mcp_server.py --help

echo "🎉 Successfully published to Docker Hub!"
echo "📋 Image Details:"
echo "   - $FULL_IMAGE:latest"
echo "   - $FULL_IMAGE:$VERSION"
echo ""
echo "🔗 Next Steps:"
echo "1. Update your GitHub repository"
echo "2. Submit to MCP Registry: https://github.com/modelcontextprotocol/registry"
echo "3. Add to Docker Hub description and README"
echo ""
echo "📝 Claude Desktop Config:"
echo '{
  "mcpServers": {
    "database-server": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--volume", "/path/to/data:/data",
        "'$FULL_IMAGE:latest'",
        "--database-url", "sqlite+aiosqlite:///data/your_db.db"
      ]
    }
  }
}'