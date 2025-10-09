#!/bin/bash
# Setup script for dbconnect-example-app

set -e

echo "🚀 Setting up dbconnect-example-app..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ uv found"

# Install dependencies
echo "📦 Installing dependencies..."
uv sync

# Check if databricks CLI is installed
if ! command -v databricks &> /dev/null; then
    echo "⚠️  databricks CLI is not installed."
    echo "   Install it with: pip install databricks-cli"
    echo "   Then run: databricks auth login --profile DEFAULT --host https://your-workspace.databricks.com"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Authenticate with Databricks (if not already done):"
echo "   databricks auth login --profile DEFAULT --host https://your-workspace.databricks.com"
echo ""
echo "2. Run the application:"
echo "   uv run src/main.py"
echo ""
echo "3. Run tests:"
echo "   uv run pytest tests/"

