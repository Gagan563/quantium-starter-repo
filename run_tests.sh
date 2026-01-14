#!/bin/bash

# Pink Morsel Sales Analysis - Automated Test Suite Runner
# This script activates the virtual environment and runs the pytest test suite
# Exit codes: 0 = all tests passed, 1 = tests failed or error occurred

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the project directory
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Pink Morsel Sales Analysis - Test Suite"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found at venv/"
    echo "Please run: python -m venv venv"
    exit 1
fi

echo "📦 Activating virtual environment..."
source venv/bin/activate

# Verify pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ Error: pytest not found in virtual environment"
    echo "Please install it with: pip install pytest"
    deactivate
    exit 1
fi

echo "✓ Virtual environment activated"
echo ""

# Run the test suite
echo "🧪 Running test suite..."
echo ""

if pytest test_app.py -v --tb=short; then
    echo ""
    echo "=========================================="
    echo "✅ All tests passed!"
    echo "=========================================="
    deactivate
    exit 0
else
    TEST_EXIT_CODE=$?
    echo ""
    echo "=========================================="
    echo "❌ Tests failed with exit code: $TEST_EXIT_CODE"
    echo "=========================================="
    deactivate
    exit 1
fi
