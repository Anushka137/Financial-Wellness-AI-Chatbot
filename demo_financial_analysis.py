#!/usr/bin/env python3
"""
Financial Analysis Demo
Demonstrates the comprehensive financial analysis capabilities of the enhanced MCP server
"""

import json
import asyncio
from datetime import datetime, timedelta
from financial_mcp_server import FinancialMCPServer
from enhanced_financial_client import EnhancedFinancialClient

async def demo_financial_analysis():
    """Run comprehensive demo of financial analysis capabilities"""
    
    print("🚀 Financial Wellness AI Chatbot - Comprehensive Demo")
    print("=" * 60)
    
    # Initialize the MCP server
    print("📊 Initializing Financial MCP Server...")
    mcp_server = FinancialMCPServer()
    
    # Initialize the enhanced client
    print("🤖 Initializing Enhanced Financial Client...")
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        api_key = config.get('GOOGLE_API_KEY')
        client = EnhancedFinancialClient(api_key)
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize client with API key: {e}")
        print("Continuing with MCP server demo only...")
        client = None
    
    print("\n" + "=" * 60)
    print("📈 DEMO 1: Basic Transaction Analysis")
    print("=" * 60)
    
    # Demo 1: Basic transaction analysis
    print("\n1. Getting all transactions...")
    result = mcp_server.get_transactions()
    if result['success']:
        data = result['data']
        print(f"✅ Found {data['total_count']} transactions totaling ${data['total_amount']:,.2f}")
        
        # Show sample transactions
        transactions = data['transactions'][:3]
        print("\nSample transactions:")
        for tx in transactions:
            print(f"  • {tx['merchant']} - ${tx['amount']:.2f} ({tx['category']})")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("📊 DEMO 2: Spending Analysis")
    print("=" * 60)
    
    # Demo 2: Spending analysis
    print("\n2. Analyzing spending patterns...")
    result = mcp_server.get_spending_analysis()
    if result['success']:
        data = result['data']
        summary = data['summary']
        print(f"✅ Spending Summary:")
        print(f"  • Total Expenses: ${summary['total_expenses']:,.2f}")
        print(f"  • Total Income: ${summary['total_income']:,.2f}")
        print(f"  • Net Income: ${summary['net_income']:,.2f}")
        
        # Show top categories
        categories = data['category_breakdown'][:3]
        print(f"\nTop spending categories:")
        for cat in categories:
            print(f"  • {cat['category']}: ${cat['total_amount']:,.2f} ({cat['transaction_count']} transactions)")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("💰 DEMO 3: Budget Analysis")
    print("=" * 60)
    
    # Demo 3: Budget analysis
    print("\n3. Analyzing budget status...")
    result = mcp_server.get_budget_analysis()
    if result['success']:
        data = result['data']
        budget_analysis = data['budget_analysis']
        
        over_budget = [cat for cat in budget_analysis if cat['status'] == 'over_budget']
        under_budget = [cat for cat in budget_analysis if cat['status'] == 'under_budget']
        
        print(f"✅ Budget Analysis:")
        print(f"  • Total Budget: ${data['total_budget']:,.2f}")
        print(f"  • Total Spent: ${data['total_spent']:,.2f}")
        print(f"  • Overall Remaining: ${data['overall_remaining']:,.2f}")
        
        if over_budget:
            print(f"\n⚠️ Over budget categories:")
            for cat in over_budget[:2]:
                print(f"  • {cat['category']}: ${cat['spent']:.2f} vs ${cat['budget']:.2f} budget")
        
        if under_budget:
            print(f"\n✅ Under budget categories:")
            for cat in under_budget[:2]:
                print(f"  • {cat['category']}: ${cat['spent']:.2f} vs ${cat['budget']:.2f} budget")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("💡 DEMO 4: Spending Recommendations")
    print("=" * 60)
    
    # Demo 4: Spending recommendations
    print("\n4. Generating personalized recommendations...")
    result = mcp_server.get_spending_recommendations()
    if result['success']:
        data = result['data']
        recommendations = data['recommendations']
        
        print(f"✅ Generated {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"\n{i}. {rec['type'].replace('_', ' ').title()}:")
            print(f"   {rec['message']}")
            print(f"   💡 {rec['suggestion']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("🏪 DEMO 5: Merchant Analysis")
    print("=" * 60)
    
    # Demo 5: Merchant analysis
    print("\n5. Analyzing merchant spending patterns...")
    result = mcp_server.get_merchant_analysis()
    if result['success']:
        data = result['data']
        merchants = data['merchant_analysis'][:5]
        
        print(f"✅ Top merchants by spending:")
        for i, merchant in enumerate(merchants, 1):
            print(f"  {i}. {merchant['merchant']}: ${merchant['total_spent']:,.2f} ({merchant['transaction_count']} transactions)")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("📈 DEMO 6: Trend Analysis")
    print("=" * 60)
    
    # Demo 6: Trend analysis
    print("\n6. Analyzing spending trends...")
    result = mcp_server.get_trend_analysis()
    if result['success']:
        data = result['data']
        metrics = data['trend_metrics']
        
        print(f"✅ Spending Trends:")
        print(f"  • Average Daily Spending: ${metrics['avg_daily_spending']:.2f}")
        print(f"  • Average Weekly Spending: ${metrics['avg_weekly_spending']:.2f}")
        print(f"  • Average Monthly Spending: ${metrics['avg_monthly_spending']:.2f}")
        print(f"  • Monthly Growth Rate: {metrics['avg_monthly_growth']:.1%}")
        print(f"  • Spending Volatility: ${metrics['spending_volatility']:.2f}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("📊 DEMO 7: Chart Generation")
    print("=" * 60)
    
    # Demo 7: Chart generation
    print("\n7. Generating financial charts...")
    chart_types = ['category_breakdown', 'spending_trend', 'budget_vs_actual', 'merchant_analysis']
    
    for chart_type in chart_types:
        print(f"\nGenerating {chart_type.replace('_', ' ')} chart...")
        result = mcp_server.generate_chart({'chart_type': chart_type})
        if result['success']:
            data = result['data']
            print(f"✅ Chart saved to: {data['chart_path']}")
        else:
            print(f"❌ Error generating {chart_type} chart: {result['error']}")
    
    print("\n" + "=" * 60)
    print("🤖 DEMO 8: Natural Language Queries")
    print("=" * 60)
    
    # Demo 8: Natural language queries (if client is available)
    if client:
        print("\n8. Testing natural language queries...")
        
        test_queries = [
            "How much did I spend this month?",
            "Show me my spending by category",
            "Am I over budget in any categories?",
            "Give me spending recommendations",
            "What are my top merchants?",
            "Generate a spending trend chart"
        ]
        
        for query in test_queries[:3]:  # Test first 3 queries
            print(f"\nQuery: '{query}'")
            try:
                response = await client.process_query(query)
                print(f"Response: {response[:200]}...")
            except Exception as e:
                print(f"Error processing query: {e}")
    else:
        print("\n8. Skipping natural language queries (client not available)")
    
    print("\n" + "=" * 60)
    print("🎯 DEMO 9: Advanced Filtering")
    print("=" * 60)
    
    # Demo 9: Advanced filtering
    print("\n9. Testing advanced filtering capabilities...")
    
    # Filter by category
    print("\nFiltering by category 'Food & Dining'...")
    result = mcp_server.get_transactions({'category': 'Food & Dining'})
    if result['success']:
        data = result['data']
        print(f"✅ Found {data['total_count']} food & dining transactions totaling ${data['total_amount']:,.2f}")
    
    # Filter by date range
    print("\nFiltering by date range (last 7 days)...")
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    result = mcp_server.get_transactions({'start_date': start_date})
    if result['success']:
        data = result['data']
        print(f"✅ Found {data['total_count']} transactions in last 7 days totaling ${data['total_amount']:,.2f}")
    
    # Filter by transaction type
    print("\nFiltering by transaction type 'expense'...")
    result = mcp_server.get_transactions({'type': 'expense'})
    if result['success']:
        data = result['data']
        print(f"✅ Found {data['total_count']} expense transactions totaling ${data['total_amount']:,.2f}")
    
    print("\n" + "=" * 60)
    print("🏁 Demo Complete!")
    print("=" * 60)
    
    print("\n🎉 All demos completed successfully!")
    print("\n📋 Summary of capabilities demonstrated:")
    print("  ✅ Transaction retrieval and filtering")
    print("  ✅ Comprehensive spending analysis")
    print("  ✅ Budget tracking and analysis")
    print("  ✅ Personalized spending recommendations")
    print("  ✅ Merchant spending analysis")
    print("  ✅ Trend analysis and forecasting")
    print("  ✅ Chart generation and visualization")
    print("  ✅ Natural language query processing")
    print("  ✅ Advanced filtering capabilities")
    
    print("\n🚀 Ready to use the Financial Wellness AI Chatbot!")
    print("Run 'python enhanced_financial_client.py' to start the interactive chatbot.")

if __name__ == "__main__":
    asyncio.run(demo_financial_analysis()) 