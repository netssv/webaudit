#!/bin/bash

# Streamlit Troubleshooting Script
# Diagnoses and fixes common Streamlit startup issues

echo "🔧 Streamlit Troubleshooting Tool"
echo "================================="
echo ""

# Function to check system resources
check_system() {
    echo "💻 System Check:"
    echo "----------------"
    echo "OS: $(uname -a)"
    echo "Python: $(python3 --version 2>/dev/null || echo 'Not found')"
    echo "Memory: $(free -h | grep '^Mem:' | awk '{print $3 "/" $2}' || echo 'Unknown')"
    echo "Disk: $(df -h . | tail -1 | awk '{print $3 "/" $2 " (" $5 " used)"}' || echo 'Unknown')"
    echo ""
}

# Function to check ports
check_ports() {
    echo "🌐 Port Check:"
    echo "--------------"
    for port in 8501 8502 8503; do
        if ss -tulpn 2>/dev/null | grep -q ":$port "; then
            echo "❌ Port $port is in use"
        else
            echo "✅ Port $port is available"
        fi
    done
    echo ""
}

# Function to check Python environment
check_python_env() {
    echo "🐍 Python Environment:"
    echo "----------------------"
    
    # Check Python executable
    PYTHON_PATH=$(which python3)
    echo "Python path: $PYTHON_PATH"
    
    # Check pip
    PIP_PATH=$(which pip3 || which pip)
    echo "Pip path: $PIP_PATH"
    
    # Check virtual environment
    if [ ! -z "$VIRTUAL_ENV" ]; then
        echo "Virtual env: $VIRTUAL_ENV"
    else
        echo "Virtual env: Not active"
    fi
    
    # Check if local web_audit_env exists
    if [ -d "web_audit_env" ]; then
        echo "Local env: web_audit_env found"
        echo "  Python: $(web_audit_env/bin/python3 --version 2>/dev/null || echo 'Not working')"
        echo "  Streamlit: $(web_audit_env/bin/streamlit version 2>/dev/null || echo 'Not installed')"
    else
        echo "Local env: web_audit_env not found"
    fi
    echo ""
}

# Function to check Streamlit installation
check_streamlit() {
    echo "📱 Streamlit Check:"
    echo "------------------"
    
    if command -v streamlit &> /dev/null; then
        echo "✅ Streamlit command found: $(which streamlit)"
        echo "✅ Version: $(streamlit version)"
        
        # Test import
        if python3 -c "import streamlit" 2>/dev/null; then
            echo "✅ Streamlit import successful"
        else
            echo "❌ Streamlit import failed"
        fi
    else
        echo "❌ Streamlit command not found"
        echo "💡 Try: pip3 install streamlit"
    fi
    echo ""
}

# Function to check dependencies
check_dependencies() {
    echo "📦 Dependencies Check:"
    echo "---------------------"
    
    MODULES=("streamlit" "pandas" "plotly" "requests" "beautifulsoup4" "dnspython" "ssl")
    
    for module in "${MODULES[@]}"; do
        if python3 -c "import $module" 2>/dev/null; then
            echo "✅ $module"
        else
            echo "❌ $module (missing)"
        fi
    done
    echo ""
}

# Function to check project files
check_project_files() {
    echo "📁 Project Files Check:"
    echo "----------------------"
    
    REQUIRED_FILES=(
        "streamlit_web_audit.py"
        "streamlit_web_audit_ultra_optimized.py"
        "web_auditor.py"
        "requirements.txt"
    )
    
    OPTIONAL_FILES=(
        "ui/styling.py"
        "ui/core_components.py"
        "ui/optimized_displays.py"
        "utils/shared_components.py"
    )
    
    echo "Required files:"
    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$file" ]; then
            echo "✅ $file"
        else
            echo "❌ $file (missing)"
        fi
    done
    
    echo ""
    echo "Optional files:"
    for file in "${OPTIONAL_FILES[@]}"; do
        if [ -f "$file" ]; then
            echo "✅ $file"
        else
            echo "⚠️  $file (missing - affects optimized version)"
        fi
    done
    echo ""
}

# Function to provide solutions
provide_solutions() {
    echo "🔧 Common Solutions:"
    echo "-------------------"
    echo ""
    
    echo "1️⃣  If Streamlit won't start:"
    echo "   • Kill existing processes: pkill -f 'streamlit'"
    echo "   • Try different port: streamlit run app.py --server.port 8502"
    echo "   • Check permissions: chmod +x *.py"
    echo ""
    
    echo "2️⃣  If modules are missing:"
    echo "   • Install requirements: pip3 install -r requirements.txt"
    echo "   • Update pip: pip3 install --upgrade pip"
    echo "   • Use virtual environment: python3 -m venv web_audit_env"
    echo ""
    
    echo "3️⃣  If import errors occur:"
    echo "   • Check Python path: echo \$PYTHONPATH"
    echo "   • Add current directory: export PYTHONPATH=\$PYTHONPATH:."
    echo "   • Verify file structure: ls -la"
    echo ""
    
    echo "4️⃣  If performance issues:"
    echo "   • Clear Streamlit cache: rm -rf ~/.streamlit"
    echo "   • Restart browser"
    echo "   • Check system resources"
    echo ""
}

# Function to run automated fixes
run_automated_fixes() {
    echo "🤖 Automated Fixes:"
    echo "-------------------"
    
    read -p "Apply automated fixes? [y/N]: " apply_fixes
    
    if [[ $apply_fixes =~ ^[Yy]$ ]]; then
        echo "🔄 Applying fixes..."
        
        # Kill existing Streamlit processes
        echo "🛑 Stopping existing Streamlit processes..."
        pkill -f "streamlit run" 2>/dev/null || true
        sleep 2
        
        # Clear Streamlit cache
        echo "🗑️  Clearing Streamlit cache..."
        rm -rf ~/.streamlit/cache 2>/dev/null || true
        
        # Fix file permissions
        echo "🔐 Fixing file permissions..."
        chmod +x *.sh 2>/dev/null || true
        chmod 644 *.py 2>/dev/null || true
        
        # Install missing dependencies
        echo "📦 Installing/updating dependencies..."
        if [ -f "requirements.txt" ]; then
            pip3 install -r requirements.txt --user --quiet
        else
            pip3 install streamlit pandas plotly requests beautifulsoup4 dnspython --user --quiet
        fi
        
        echo "✅ Automated fixes completed!"
    else
        echo "⏭️  Skipped automated fixes"
    fi
    echo ""
}

# Main function
main() {
    echo "🎯 Running comprehensive diagnostics..."
    echo ""
    
    check_system
    check_ports
    check_python_env
    check_streamlit
    check_dependencies
    check_project_files
    provide_solutions
    run_automated_fixes
    
    echo "🎉 Diagnostics complete!"
    echo ""
    echo "🚀 Ready to launch? Try:"
    echo "   ./launch_robust.sh"
    echo "   or"
    echo "   streamlit run streamlit_web_audit_ultra_optimized.py"
}

# Run main function
main "$@"
