#!/bin/bash

cd "$(dirname "$0")/../../../.."
source env/bin/activate

echo "🧪 Running imguploader tests..."
echo ""

python -m pytest tests/utest/utilities/imguploader/ -v --tb=short

echo ""
echo "✅ Tests completed!"

