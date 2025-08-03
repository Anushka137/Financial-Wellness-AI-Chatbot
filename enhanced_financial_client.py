#!/usr/bin/env python3
"""
Enhanced Financial Wellness Client
Integrates with the Financial MCP Server to provide comprehensive financial analysis
"""

import json
import asyncio
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from financial_mcp_server import FinancialMCPServer

class EnhancedFinancialClient:
    def __init__(self, api_key: str):
        self.mcp_server = FinancialMCPServer()
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Initialize conversation history
        self.conversation_history = []
        
    def get_available_tools(self) -> List[Dict]:
        """Get list of available MCP tools"""
        return self.mcp_server.list_tools()
    
    def call_mcp_tool(self, tool_name: str, args: Dict = None) -> Dict:
        """Call MCP server tool"""
        return self.mcp_server.call_tool(tool_name, args or {})
    
    def analyze_query(self, user_query: str) -> Dict:
        """Analyze user query to determine appropriate MCP tools to call"""
        query_lower = user_query.lower()
        
        # Define query patterns and corresponding tools
        query_patterns = {
            'transactions': ['transaction', 'purchase', 'expense', 'income', 'spending'],
            'spending_analysis': ['spending analysis', 'spending breakdown', 'category breakdown', 'how much spent'],
            'budget_analysis': ['budget', 'budget analysis', 'over budget', 'under budget', 'budget status'],
            'recommendations': ['recommendation', 'advice', 'suggestion', 'improve', 'save money'],
            'merchant_analysis': ['merchant', 'store', 'where spent', 'top merchants'],
            'trend_analysis': ['trend', 'over time', 'monthly', 'weekly', 'daily trend'],
            'charts': ['chart', 'graph', 'visualization', 'plot', 'pie chart', 'bar chart']
        }
        
        # Determine which tools to call based on query
        tools_to_call = []
        
        # Priority handling for chart requests
        if any(pattern in query_lower for pattern in ['chart', 'graph', 'visualization', 'plot']):
            # Determine specific chart type based on query
            if any(pattern in query_lower for pattern in ['trend', 'spending trend', 'daily trend', 'weekly trend', 'monthly trend']):
                tools_to_call.append('generate_chart')
                # Add chart type specification
                return {
                    'tools': tools_to_call,
                    'date_filters': self.extract_date_filters(user_query),
                    'query_type': 'financial_analysis',
                    'chart_type': 'spending_trend'
                }
            elif any(pattern in query_lower for pattern in ['category', 'breakdown', 'pie']):
                tools_to_call.append('generate_chart')
                return {
                    'tools': tools_to_call,
                    'date_filters': self.extract_date_filters(user_query),
                    'query_type': 'financial_analysis',
                    'chart_type': 'category_breakdown'
                }
            elif any(pattern in query_lower for pattern in ['budget', 'actual', 'comparison']):
                tools_to_call.append('generate_chart')
                return {
                    'tools': tools_to_call,
                    'date_filters': self.extract_date_filters(user_query),
                    'query_type': 'financial_analysis',
                    'chart_type': 'budget_vs_actual'
                }
            elif any(pattern in query_lower for pattern in ['merchant', 'store', 'top merchants']):
                tools_to_call.append('generate_chart')
                return {
                    'tools': tools_to_call,
                    'date_filters': self.extract_date_filters(user_query),
                    'query_type': 'financial_analysis',
                    'chart_type': 'merchant_analysis'
                }
            else:
                # Default chart type
                tools_to_call.append('generate_chart')
                return {
                    'tools': tools_to_call,
                    'date_filters': self.extract_date_filters(user_query),
                    'query_type': 'financial_analysis',
                    'chart_type': 'category_breakdown'
                }
        
        # Regular analysis for non-chart queries
        for tool_category, patterns in query_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                if tool_category == 'transactions':
                    tools_to_call.append('get_transactions')
                elif tool_category == 'spending_analysis':
                    tools_to_call.append('get_spending_analysis')
                elif tool_category == 'budget_analysis':
                    tools_to_call.append('get_budget_analysis')
                elif tool_category == 'recommendations':
                    tools_to_call.append('get_spending_recommendations')
                elif tool_category == 'merchant_analysis':
                    tools_to_call.append('get_merchant_analysis')
                elif tool_category == 'trend_analysis':
                    tools_to_call.append('get_trend_analysis')
        
        # Extract date filters from query
        date_filters = self.extract_date_filters(user_query)
        
        return {
            'tools': tools_to_call,
            'date_filters': date_filters,
            'query_type': 'financial_analysis'
        }
    
    def extract_date_filters(self, query: str) -> Dict:
        """Extract date filters from natural language query"""
        query_lower = query.lower()
        date_filters = {}
        
        # Common date patterns
        if 'this month' in query_lower or 'current month' in query_lower:
            start_date = datetime.now().replace(day=1)
            date_filters['start_date'] = start_date.strftime('%Y-%m-%d')
        elif 'last month' in query_lower:
            last_month = datetime.now().replace(day=1) - timedelta(days=1)
            start_date = last_month.replace(day=1)
            end_date = datetime.now().replace(day=1) - timedelta(days=1)
            date_filters['start_date'] = start_date.strftime('%Y-%m-%d')
            date_filters['end_date'] = end_date.strftime('%Y-%m-%d')
        elif 'this week' in query_lower:
            start_date = datetime.now() - timedelta(days=datetime.now().weekday())
            date_filters['start_date'] = start_date.strftime('%Y-%m-%d')
        elif 'last week' in query_lower:
            start_date = datetime.now() - timedelta(days=datetime.now().weekday() + 7)
            end_date = datetime.now() - timedelta(days=datetime.now().weekday() + 1)
            date_filters['start_date'] = start_date.strftime('%Y-%m-%d')
            date_filters['end_date'] = end_date.strftime('%Y-%m-%d')
        elif 'last 30 days' in query_lower or 'past month' in query_lower:
            start_date = datetime.now() - timedelta(days=30)
            date_filters['start_date'] = start_date.strftime('%Y-%m-%d')
        elif 'last 7 days' in query_lower or 'past week' in query_lower:
            start_date = datetime.now() - timedelta(days=7)
            date_filters['start_date'] = start_date.strftime('%Y-%m-%d')
        
        return date_filters
    
    def format_financial_response(self, tool_results: Dict, user_query: str) -> str:
        """Format MCP tool results into a natural language response"""
        if not tool_results:
            return "I couldn't find any relevant financial data to answer your question."
        
        response_parts = []
        
        for tool_name, result in tool_results.items():
            if not result.get('success'):
                continue
                
            data = result.get('data', {})
            
            if tool_name == 'get_transactions':
                response_parts.append(self._format_transactions_response(data, user_query))
            elif tool_name == 'get_spending_analysis':
                response_parts.append(self._format_spending_analysis_response(data, user_query))
            elif tool_name == 'get_budget_analysis':
                response_parts.append(self._format_budget_analysis_response(data, user_query))
            elif tool_name == 'get_spending_recommendations':
                response_parts.append(self._format_recommendations_response(data, user_query))
            elif tool_name == 'get_merchant_analysis':
                response_parts.append(self._format_merchant_analysis_response(data, user_query))
            elif tool_name == 'get_trend_analysis':
                response_parts.append(self._format_trend_analysis_response(data, user_query))
            elif tool_name == 'generate_chart':
                response_parts.append(self._format_chart_response(data, user_query))
        
        return '\n\n'.join(response_parts) if response_parts else "I couldn't find any relevant financial data to answer your question."
    
    def _format_transactions_response(self, data: Dict, user_query: str) -> str:
        """Format transactions data into natural language"""
        transactions = data.get('transactions', [])
        total_count = data.get('total_count', 0)
        total_amount = data.get('total_amount', 0)
        
        if not transactions:
            return "No transactions found matching your criteria."
        
        response = f"I found {total_count} transactions totaling ${total_amount:,.2f}.\n\n"
        
        # Show top 5 transactions by amount
        sorted_transactions = sorted(transactions, key=lambda x: x['amount'], reverse=True)[:5]
        
        response += "**Top 5 Transactions:**\n"
        for i, tx in enumerate(sorted_transactions, 1):
            response += f"{i}. {tx['merchant']} - ${tx['amount']:.2f} ({tx['category']}) - {tx['date']}\n"
        
        return response
    
    def _format_spending_analysis_response(self, data: Dict, user_query: str) -> str:
        """Format spending analysis data into natural language"""
        summary = data.get('summary', {})
        category_breakdown = data.get('category_breakdown', [])
        
        response = f"**Spending Summary:**\n"
        response += f"• Total Expenses: ${summary.get('total_expenses', 0):,.2f}\n"
        response += f"• Total Income: ${summary.get('total_income', 0):,.2f}\n"
        response += f"• Net Income: ${summary.get('net_income', 0):,.2f}\n\n"
        
        response += "**Spending by Category:**\n"
        for category in category_breakdown[:5]:  # Top 5 categories
            response += f"• {category['category']}: ${category['total_amount']:,.2f} ({category['transaction_count']} transactions)\n"
        
        return response
    
    def _format_budget_analysis_response(self, data: Dict, user_query: str) -> str:
        """Format budget analysis data into natural language"""
        budget_analysis = data.get('budget_analysis', [])
        
        response = "**Budget Analysis:**\n\n"
        
        over_budget_categories = []
        under_budget_categories = []
        
        for category in budget_analysis:
            if category['status'] == 'over_budget':
                over_budget_categories.append(category)
            elif category['status'] == 'under_budget':
                under_budget_categories.append(category)
        
        if over_budget_categories:
            response += "**⚠️ Over Budget Categories:**\n"
            for category in over_budget_categories:
                response += f"• {category['category']}: ${category['spent']:.2f} spent vs ${category['budget']:.2f} budget (${category['spent'] - category['budget']:.2f} over)\n"
            response += "\n"
        
        if under_budget_categories:
            response += "**✅ Under Budget Categories:**\n"
            for category in under_budget_categories[:3]:  # Top 3
                response += f"• {category['category']}: ${category['spent']:.2f} spent vs ${category['budget']:.2f} budget (${category['budget'] - category['spent']:.2f} remaining)\n"
        
        return response
    
    def _format_recommendations_response(self, data: Dict, user_query: str) -> str:
        """Format recommendations data into natural language"""
        recommendations = data.get('recommendations', [])
        
        if not recommendations:
            return "Great job! Your spending patterns look healthy. Keep up the good work!"
        
        response = "**💡 Personalized Recommendations:**\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            response += f"{i}. **{rec['type'].replace('_', ' ').title()}:**\n"
            response += f"   {rec['message']}\n"
            response += f"   💡 {rec['suggestion']}\n\n"
        
        return response
    
    def _format_merchant_analysis_response(self, data: Dict, user_query: str) -> str:
        """Format merchant analysis data into natural language"""
        merchant_analysis = data.get('merchant_analysis', [])
        
        if not merchant_analysis:
            return "No merchant data available for the specified period."
        
        response = "**🏪 Top Merchants by Spending:**\n\n"
        
        for i, merchant in enumerate(merchant_analysis[:10], 1):
            response += f"{i}. {merchant['merchant']}: ${merchant['total_spent']:,.2f} ({merchant['transaction_count']} transactions)\n"
        
        return response
    
    def _format_trend_analysis_response(self, data: Dict, user_query: str) -> str:
        """Format trend analysis data into natural language"""
        trend_metrics = data.get('trend_metrics', {})
        
        response = "**📈 Spending Trends:**\n\n"
        response += f"• Average Daily Spending: ${trend_metrics.get('avg_daily_spending', 0):.2f}\n"
        response += f"• Average Weekly Spending: ${trend_metrics.get('avg_weekly_spending', 0):.2f}\n"
        response += f"• Average Monthly Spending: ${trend_metrics.get('avg_monthly_spending', 0):.2f}\n"
        response += f"• Monthly Growth Rate: {trend_metrics.get('avg_monthly_growth', 0):.1%}\n"
        response += f"• Spending Volatility: ${trend_metrics.get('spending_volatility', 0):.2f}\n"
        
        return response
    
    def _format_chart_response(self, data: Dict, user_query: str) -> str:
        """Format chart generation response"""
        chart_path = data.get('chart_path', '')
        chart_type = data.get('chart_type', '')
        
        response = f"📊 I've generated a {chart_type.replace('_', ' ')} chart for you!\n"
        response += f"The chart has been saved to: {chart_path}\n"
        
        return response
    
    async def process_query(self, user_query: str) -> str:
        """Process user query and return comprehensive financial analysis"""
        try:
            # Add query to conversation history
            self.conversation_history.append({"role": "user", "content": user_query})
            
            # Analyze query to determine tools to call
            analysis = self.analyze_query(user_query)
            
            # Call appropriate MCP tools
            tool_results = {}
            for tool_name in analysis['tools']:
                args = analysis.get('date_filters', {})
                
                # Handle chart generation with specific chart type
                if tool_name == 'generate_chart' and 'chart_type' in analysis:
                    args['chart_type'] = analysis['chart_type']
                
                result = self.call_mcp_tool(tool_name, args)
                tool_results[tool_name] = result
            
            # Format response
            response = self.format_financial_response(tool_results, user_query)
            
            # Add response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_response = f"I encountered an error while processing your request: {str(e)}"
            self.conversation_history.append({"role": "assistant", "content": error_response})
            return error_response
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.conversation_history:
            return "No conversation history available."
        
        summary = "**Conversation Summary:**\n\n"
        for i, message in enumerate(self.conversation_history[-6:], 1):  # Last 6 messages
            role = "👤 You" if message['role'] == 'user' else "🤖 Assistant"
            summary += f"{i}. {role}: {message['content'][:100]}{'...' if len(message['content']) > 100 else ''}\n\n"
        
        return summary

async def main():
    """Main function to run the enhanced financial client"""
    # Load configuration
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        api_key = config.get('GOOGLE_API_KEY')
    except FileNotFoundError:
        print("Error: config.json not found. Please create it with your Google API key.")
        return
    except KeyError:
        print("Error: GOOGLE_API_KEY not found in config.json")
        return
    
    if not api_key:
        print("Error: No API key provided")
        return
    
    # Initialize client
    client = EnhancedFinancialClient(api_key)
    
    print("🤖 Enhanced Financial Wellness AI Chatbot")
    print("=" * 50)
    print("Ask me anything about your finances! Examples:")
    print("• 'How much did I spend this month?'")
    print("• 'Show me my spending by category'")
    print("• 'Am I over budget in any categories?'")
    print("• 'Give me spending recommendations'")
    print("• 'What are my top merchants?'")
    print("• 'Generate a spending trend chart'")
    print("• 'Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🤖 Assistant: Thank you for using the Financial Wellness AI Chatbot! Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\n🤖 Assistant: Analyzing your financial data...")
            response = await client.process_query(user_input)
            print(f"\n{response}")
            
        except KeyboardInterrupt:
            print("\n\n🤖 Assistant: Goodbye!")
            break
        except Exception as e:
            print(f"\n🤖 Assistant: I encountered an error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 