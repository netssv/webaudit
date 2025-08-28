#!/bin/bash

# Web Audit Tool - Optimized Launch Script
# This script demonstrates the modular architecture improvements

echo "🌐 Web Audit Tool - Optimized Modular Version"
echo "=============================================="
echo ""

# Show file size comparison
echo "📊 File Size Comparison:"
echo "------------------------"
original_lines=$(wc -l < streamlit_web_audit.py)
optimized_lines=$(wc -l < streamlit_web_audit_optimized.py)
reduction_percent=$(( (original_lines - optimized_lines) * 100 / original_lines ))

echo "Original file:  $original_lines lines"
echo "Optimized file: $optimized_lines lines"
echo "Reduction:      $reduction_percent% smaller"
echo ""

# Show module structure
echo "🧩 Modular Structure:"
echo "---------------------"
echo "Main app:       streamlit_web_audit_optimized.py ($optimized_lines lines)"
echo "Styling:        ui/styling.py ($(wc -l < ui/styling.py) lines)"
echo "Core UI:        ui/core_components.py ($(wc -l < ui/core_components.py) lines)"
echo "AI Components:  ui/ai_components.py ($(wc -l < ui/ai_components.py) lines)"
echo "Displays:       ui/displays.py ($(wc -l < ui/displays.py) lines)"
echo ""

# Test module imports
echo "🔧 Testing Module Imports:"
echo "--------------------------"
if python3 -c "import ui.styling, ui.core_components, ui.ai_components; print('✅ All modules imported successfully')" 2>/dev/null; then
    echo "✅ All modules working correctly"
else
    echo "❌ Module import errors detected"
    exit 1
fi
echo ""

# Show available launch options
echo "🚀 Launch Options:"
echo "------------------"
echo "Option 1 - Optimized Version (Recommended):"
echo "  streamlit run streamlit_web_audit_optimized.py"
echo ""
echo "Option 2 - Original Version (For comparison):"
echo "  streamlit run streamlit_web_audit.py"
echo ""

# Offer to launch
read -p "Would you like to launch the optimized version now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌟 Launching optimized Web Audit Tool..."
    echo "The application will open in your default browser."
    echo "Press Ctrl+C to stop the application."
    echo ""
    streamlit run streamlit_web_audit_optimized.py
else
    echo "💡 To launch manually, run:"
    echo "   streamlit run streamlit_web_audit_optimized.py"
fi
