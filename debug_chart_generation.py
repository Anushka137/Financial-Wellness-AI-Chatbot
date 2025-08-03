#!/usr/bin/env python3
"""
Debug script to test chart generation and identify issues
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
import sys
from financial_mcp_server import FinancialMCPServer

def test_chart_generation():
    """Test chart generation with detailed debugging"""
    
    print("🔍 Debugging Chart Generation")
    print("=" * 50)
    
    # Check if charts directory exists
    if not os.path.exists('charts'):
        print("Creating charts directory...")
        os.makedirs('charts')
    
    # Initialize server
    print("Initializing Financial MCP Server...")
    server = FinancialMCPServer()
    
    # Test each chart type
    chart_types = ['category_breakdown', 'spending_trend', 'budget_vs_actual', 'merchant_analysis']
    
    for chart_type in chart_types:
        print(f"\n📊 Testing {chart_type} chart generation...")
        
        try:
            # Generate chart
            result = server.generate_chart({'chart_type': chart_type})
            
            if result['success']:
                chart_path = result['data']['chart_path']
                print(f"✅ Chart generated successfully!")
                print(f"   Path: {chart_path}")
                
                # Check if file exists
                if os.path.exists(chart_path):
                    file_size = os.path.getsize(chart_path)
                    print(f"   File exists: Yes")
                    print(f"   File size: {file_size} bytes")
                    
                    if file_size > 0:
                        print(f"   ✅ Chart file is valid!")
                    else:
                        print(f"   ❌ Chart file is empty!")
                else:
                    print(f"   ❌ Chart file does not exist!")
            else:
                print(f"❌ Chart generation failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception during chart generation: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("📋 Summary of chart files:")
    
    if os.path.exists('charts'):
        files = os.listdir('charts')
        png_files = [f for f in files if f.endswith('.png')]
        
        if png_files:
            for file in png_files:
                file_path = os.path.join('charts', file)
                file_size = os.path.getsize(file_path)
                print(f"  📊 {file}: {file_size} bytes")
        else:
            print("  No PNG files found in charts directory")
    else:
        print("  Charts directory does not exist")

if __name__ == "__main__":
    test_chart_generation() 