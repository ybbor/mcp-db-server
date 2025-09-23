# MCP Database Server - Docker Registry Publishing Script (PowerShell)
# Usage: .\publish-docker.ps1 [version] [dockerhub-username]

param(
    [string]$Version = "1.0.0",
    [string]$DockerHubUser = "souhardyak"
)

$ImageName = "mcp-database-server"
$FullImage = "$DockerHubUser/$ImageName"

Write-Host "🚀 Publishing MCP Database Server to Docker Registry" -ForegroundColor Green
Write-Host "Version: $Version" -ForegroundColor Cyan
Write-Host "Docker Hub User: $DockerHubUser" -ForegroundColor Cyan
Write-Host "Full Image Name: $FullImage" -ForegroundColor Cyan

# Ensure we're in the correct directory
if (-not (Test-Path "mcp_server.py")) {
    Write-Host "❌ Error: mcp_server.py not found. Please run from project root." -ForegroundColor Red
    exit 1
}

# Build the image
Write-Host "📦 Building Docker image..." -ForegroundColor Yellow
docker build -t "${ImageName}:latest" .
docker build -t "${ImageName}:${Version}" .

# Tag for Docker Hub
Write-Host "🏷️  Tagging images..." -ForegroundColor Yellow
docker tag "${ImageName}:latest" "${FullImage}:latest"
docker tag "${ImageName}:${Version}" "${FullImage}:${Version}"

# Test the image
Write-Host "🧪 Testing the image..." -ForegroundColor Yellow
docker run --rm "${FullImage}:latest" python -c "
import sys
sys.path.insert(0, 'app')
from mcp_server import initialize_database
print('✅ Image test passed!')
"

# Login to Docker Hub (interactive)
Write-Host "🔐 Please login to Docker Hub..." -ForegroundColor Yellow
docker login

# Push to Docker Hub
Write-Host "📤 Pushing to Docker Hub..." -ForegroundColor Yellow
docker push "${FullImage}:latest"
docker push "${FullImage}:${Version}"

# Verify the push
Write-Host "✅ Verifying pushed images..." -ForegroundColor Green
docker run --rm "${FullImage}:latest" python mcp_server.py --help

Write-Host "🎉 Successfully published to Docker Hub!" -ForegroundColor Green
Write-Host "📋 Image Details:" -ForegroundColor Cyan
Write-Host "   - ${FullImage}:latest" -ForegroundColor White
Write-Host "   - ${FullImage}:${Version}" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Update your GitHub repository" -ForegroundColor White
Write-Host "2. Submit to MCP Registry: https://github.com/modelcontextprotocol/registry" -ForegroundColor White
Write-Host "3. Add to Docker Hub description and README" -ForegroundColor White
Write-Host ""
Write-Host "📝 Claude Desktop Config:" -ForegroundColor Cyan
$claudeConfig = @"
{
  "mcpServers": {
    "database-server": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--volume", "/path/to/data:/data",
        "${FullImage}:latest",
        "--database-url", "sqlite+aiosqlite:///data/your_db.db"
      ]
    }
  }
}
"@
Write-Host $claudeConfig -ForegroundColor White