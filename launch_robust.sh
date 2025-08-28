#!/bin/bash

# Robust Web Audit Tool Launcher
# Handles common Streamlit startup issues

echo "🌐 Web Audit Tool - Robust Launcher"
echo "===================================="

# Function to kill existing Streamlit processes
kill_streamlit() {
    echo "🔍 Checking for existing Streamlit processes..."
    STREAMLIT_PIDS=$(pgrep -f "streamlit run")
    if [ ! -z "$STREAMLIT_PIDS" ]; then
        echo "🛑 Found running Streamlit processes: $STREAMLIT_PIDS"
        echo "🔄 Stopping existing processes..."
        pkill -f "streamlit run"
        sleep 2
        echo "✅ Existing processes stopped"
    else
        echo "✅ No existing Streamlit processes found"
    fi
}

# Function to check dependencies
check_dependencies() {
    echo "🔍 Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 not found. Please install Python3."
        exit 1
    fi
    echo "✅ Python3 found: $(python3 --version)"
    
    # Check Streamlit
    if ! command -v streamlit &> /dev/null; then
        echo "❌ Streamlit not found. Installing..."
        pip3 install streamlit
    fi
    echo "✅ Streamlit found: $(streamlit version)"
    
    # Check required modules
    echo "🔍 Checking Python modules..."
    python3 -c "
import sys
sys.path.append('.')
missing = []
try:
    import streamlit
    print('✅ Streamlit module OK')
except ImportError:
    missing.append('streamlit')

try:
    import pandas
    print('✅ Pandas module OK')
except ImportError:
    missing.append('pandas')

try:
    import plotly
    print('✅ Plotly module OK')
except ImportError:
    missing.append('plotly')

try:
    from web_auditor import WebAuditor
    print('✅ WebAuditor module OK')
except ImportError as e:
    print(f'⚠️  WebAuditor import issue: {e}')

if missing:
    print(f'❌ Missing modules: {missing}')
    exit(1)
else:
    print('✅ All modules available')
" || exit 1
}

# Function to check file integrity
check_files() {
    echo "🔍 Checking file integrity..."
    
    FILES=("streamlit_web_audit.py" "streamlit_web_audit_ultra_optimized.py" "web_auditor.py")
    for file in "${FILES[@]}"; do
        if [ -f "$file" ]; then
            echo "✅ $file exists"
        else
            echo "❌ $file not found"
            exit 1
        fi
    done
    
    # Check if files can be imported
    echo "🔍 Testing file imports..."
    python3 -c "
import sys
sys.path.append('.')
try:
    import streamlit_web_audit
    print('✅ streamlit_web_audit.py can be imported')
except Exception as e:
    print(f'❌ Error importing streamlit_web_audit.py: {e}')
    
try:
    import streamlit_web_audit_ultra_optimized
    print('✅ streamlit_web_audit_ultra_optimized.py can be imported')
except Exception as e:
    print(f'❌ Error importing ultra-optimized version: {e}')
" 2>/dev/null || echo "⚠️  Import test completed with warnings (normal for Streamlit)"
}

# Function to start Streamlit
start_streamlit() {
    local file_to_run="$1"
    local port="${2:-8501}"
    
    echo "🚀 Starting Streamlit..."
    echo "📁 File: $file_to_run"
    echo "🌐 Port: $port"
    echo "📊 URL: http://localhost:$port"
    echo ""
    
    # Try different startup methods
    echo "🔄 Attempting to start Streamlit..."
    
    # Method 1: Standard startup
    if streamlit run "$file_to_run" --server.port="$port" --server.headless=false; then
        echo "✅ Streamlit started successfully"
    else
        echo "⚠️  Standard startup failed, trying alternative method..."
        
        # Method 2: With explicit configuration
        streamlit run "$file_to_run" \
            --server.port="$port" \
            --server.headless=false \
            --server.address=localhost \
            --server.enableCORS=false \
            --server.enableXsrfProtection=false
    fi
}

# Main execution
main() {
    echo "🎯 Starting Web Audit Tool diagnostic and launch sequence..."
    echo ""
    
    # Change to script directory
    cd "$(dirname "$0")" || exit 1
    echo "📁 Working directory: $(pwd)"
    echo ""
    
    # Run checks
    kill_streamlit
    check_dependencies
    check_files
    
    echo ""
    echo "🎯 All checks passed! Choose version to launch:"
    echo "1) Original version (streamlit_web_audit.py)"
    echo "2) Ultra-optimized version (streamlit_web_audit_ultra_optimized.py)"
    echo "3) Exit"
    echo ""
    
    read -p "Enter choice [1-3]: " choice
    
    case $choice in
        1)
            echo "🚀 Launching original version..."
            start_streamlit "streamlit_web_audit.py"
            ;;
        2)
            echo "🚀 Launching ultra-optimized version..."
            start_streamlit "streamlit_web_audit_ultra_optimized.py"
            ;;
        3)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Launching ultra-optimized version by default..."
            start_streamlit "streamlit_web_audit_ultra_optimized.py"
            ;;
    esac
}

# Handle script interruption
trap 'echo ""; echo "🛑 Interrupted. Cleaning up..."; kill_streamlit; exit 1' INT TERM

# Run main function
main "$@"
