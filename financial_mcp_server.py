#!/usr/bin/env python3
"""
Enhanced Financial Wellness MCP Server
Provides comprehensive financial analysis tools using daily transactions dataset
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import os

class FinancialMCPServer:
    def __init__(self, csv_file_path: str = "daily_transactions.csv"):
        self.csv_file_path = csv_file_path
        self.transactions_df = None
        self.load_transactions()
        
        # Define spending categories and their typical budget allocations
        self.category_budgets = {
            'Groceries': 400,
            'Food & Dining': 300,
            'Transportation': 200,
            'Entertainment': 150,
            'Shopping': 250,
            'Healthcare': 100,
            'Utilities': 200,
            'Rent': 1200,
            'Savings': 500,
            'Income': 0  # Income doesn't have a budget limit
        }
        
    def load_transactions(self):
        """Load transactions from CSV file"""
        try:
            self.transactions_df = pd.read_csv(self.csv_file_path)
            self.transactions_df['date'] = pd.to_datetime(self.transactions_df['date'])
            self.transactions_df['amount'] = pd.to_numeric(self.transactions_df['amount'])
            print(f"Loaded {len(self.transactions_df)} transactions from {self.csv_file_path}")
        except Exception as e:
            print(f"Error loading transactions: {e}")
            # Create sample data if file doesn't exist
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample transaction data if CSV file doesn't exist"""
        sample_data = {
            'transaction_id': ['TXN001', 'TXN002', 'TXN003'],
            'date': ['2024-01-01', '2024-01-01', '2024-01-01'],
            'amount': [125.50, 45.00, 2500.00],
            'category': ['Groceries', 'Transportation', 'Income'],
            'description': ['Whole Foods Market purchase', 'Uber ride to airport', 'Salary deposit'],
            'transaction_type': ['expense', 'expense', 'income'],
            'merchant': ['Whole Foods Market', 'Uber', 'Employer Inc'],
            'account_type': ['checking', 'checking', 'checking']
        }
        self.transactions_df = pd.DataFrame(sample_data)
        self.transactions_df['date'] = pd.to_datetime(self.transactions_df['date'])
        self.transactions_df['amount'] = pd.to_numeric(self.transactions_df['amount'])
        print("Created sample transaction data")
    
    def get_transactions(self, args: Dict = None) -> Dict:
        """Get transactions with optional filtering"""
        try:
            df = self.transactions_df.copy()
            
            if args:
                if 'category' in args and args['category']:
                    df = df[df['category'].str.contains(args['category'], case=False, na=False)]
                
                if 'type' in args and args['type']:
                    df = df[df['transaction_type'] == args['type']]
                
                if 'start_date' in args and args['start_date']:
                    start_date = pd.to_datetime(args['start_date'])
                    df = df[df['date'] >= start_date]
                
                if 'end_date' in args and args['end_date']:
                    end_date = pd.to_datetime(args['end_date'])
                    df = df[df['date'] <= end_date]
                
                if 'merchant' in args and args['merchant']:
                    df = df[df['merchant'].str.contains(args['merchant'], case=False, na=False)]
            
            # Convert to list of dictionaries for JSON serialization
            transactions = df.to_dict('records')
            
            return {
                "success": True,
                "data": {
                    "transactions": transactions,
                    "total_count": len(transactions),
                    "total_amount": float(df['amount'].sum()),
                    "filters_applied": args or {}
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_spending_analysis(self, args: Dict = None) -> Dict:
        """Get comprehensive spending analysis"""
        try:
            df = self.transactions_df.copy()
            
            # Filter by date range if provided
            if args and 'start_date' in args and args['start_date']:
                start_date = pd.to_datetime(args['start_date'])
                df = df[df['date'] >= start_date]
            
            if args and 'end_date' in args and args['end_date']:
                end_date = pd.to_datetime(args['end_date'])
                df = df[df['date'] <= end_date]
            
            # Separate expenses and income
            expenses_df = df[df['transaction_type'] == 'expense']
            income_df = df[df['transaction_type'] == 'income']
            
            # Calculate key metrics
            total_expenses = float(expenses_df['amount'].sum())
            total_income = float(income_df['amount'].sum())
            net_income = total_income - total_expenses
            
            # Category analysis
            category_spending = expenses_df.groupby('category')['amount'].agg(['sum', 'count']).reset_index()
            category_spending.columns = ['category', 'total_amount', 'transaction_count']
            category_spending = category_spending.sort_values('total_amount', ascending=False)
            
            # Monthly spending trend
            monthly_spending = expenses_df.groupby(expenses_df['date'].dt.to_period('M'))['amount'].sum()
            
            # Top merchants
            top_merchants = expenses_df.groupby('merchant')['amount'].sum().sort_values(ascending=False).head(10)
            
            # Spending by account type
            account_spending = expenses_df.groupby('account_type')['amount'].sum()
            
            return {
                "success": True,
                "data": {
                    "summary": {
                        "total_expenses": total_expenses,
                        "total_income": total_income,
                        "net_income": net_income,
                        "expense_count": len(expenses_df),
                        "income_count": len(income_df)
                    },
                    "category_breakdown": category_spending.to_dict('records'),
                    "monthly_trend": {str(k): float(v) for k, v in monthly_spending.items()},
                    "top_merchants": {k: float(v) for k, v in top_merchants.items()},
                    "account_breakdown": {k: float(v) for k, v in account_spending.items()}
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_budget_analysis(self, args: Dict = None) -> Dict:
        """Analyze spending against budget categories"""
        try:
            df = self.transactions_df.copy()
            expenses_df = df[df['transaction_type'] == 'expense']
            
            # Filter by date range if provided
            if args and 'start_date' in args and args['start_date']:
                start_date = pd.to_datetime(args['start_date'])
                expenses_df = expenses_df[expenses_df['date'] >= start_date]
            
            if args and 'end_date' in args and args['end_date']:
                end_date = pd.to_datetime(args['end_date'])
                expenses_df = expenses_df[expenses_df['date'] <= end_date]
            
            # Calculate spending by category
            category_spending = expenses_df.groupby('category')['amount'].sum()
            
            # Compare with budgets
            budget_analysis = []
            for category, budget in self.category_budgets.items():
                if category in category_spending:
                    spent = float(category_spending[category])
                    remaining = budget - spent
                    percentage_used = (spent / budget * 100) if budget > 0 else 0
                    
                    budget_analysis.append({
                        "category": category,
                        "budget": budget,
                        "spent": spent,
                        "remaining": remaining,
                        "percentage_used": percentage_used,
                        "status": "over_budget" if spent > budget else "under_budget" if spent < budget * 0.8 else "on_track"
                    })
                else:
                    budget_analysis.append({
                        "category": category,
                        "budget": budget,
                        "spent": 0,
                        "remaining": budget,
                        "percentage_used": 0,
                        "status": "no_spending"
                    })
            
            return {
                "success": True,
                "data": {
                    "budget_analysis": budget_analysis,
                    "total_budget": sum(self.category_budgets.values()),
                    "total_spent": float(category_spending.sum()),
                    "overall_remaining": sum(self.category_budgets.values()) - float(category_spending.sum())
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_spending_recommendations(self, args: Dict = None) -> Dict:
        """Generate personalized spending recommendations"""
        try:
            df = self.transactions_df.copy()
            expenses_df = df[df['transaction_type'] == 'expense']
            
            # Filter by recent period (last 30 days if no date specified)
            if args and 'start_date' in args and args['start_date']:
                start_date = pd.to_datetime(args['start_date'])
            else:
                start_date = datetime.now() - timedelta(days=30)
            
            recent_expenses = expenses_df[expenses_df['date'] >= start_date]
            
            # Analyze spending patterns
            category_spending = recent_expenses.groupby('category')['amount'].sum()
            avg_daily_spending = float(recent_expenses['amount'].sum() / 30)
            
            recommendations = []
            
            # Check for overspending categories
            for category, spent in category_spending.items():
                if category in self.category_budgets:
                    budget = self.category_budgets[category]
                    if spent > budget:
                        recommendations.append({
                            "type": "overspending_alert",
                            "category": category,
                            "message": f"You've spent ${spent:.2f} on {category}, which is ${spent - budget:.2f} over your ${budget} budget.",
                            "suggestion": f"Consider reducing {category} spending by ${(spent - budget) / 30:.2f} per day to stay on track."
                        })
            
            # Check for high-frequency small purchases
            merchant_frequency = recent_expenses.groupby('merchant').size()
            frequent_merchants = merchant_frequency[merchant_frequency > 5]
            
            for merchant, count in frequent_merchants.items():
                total_spent = float(recent_expenses[recent_expenses['merchant'] == merchant]['amount'].sum())
                recommendations.append({
                    "type": "frequent_purchases",
                    "merchant": merchant,
                    "message": f"You've made {count} purchases at {merchant} totaling ${total_spent:.2f}.",
                    "suggestion": f"Consider bulk purchases or subscriptions to reduce frequent small transactions."
                })
            
            # General recommendations
            if avg_daily_spending > 100:
                recommendations.append({
                    "type": "high_daily_spending",
                    "message": f"Your average daily spending is ${avg_daily_spending:.2f}.",
                    "suggestion": "Consider tracking your daily expenses more closely and setting daily spending limits."
                })
            
            # Savings recommendations
            income_df = df[df['transaction_type'] == 'income']
            if len(income_df) > 0:
                total_income = float(income_df['amount'].sum())
                total_expenses = float(expenses_df['amount'].sum())
                savings_rate = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
                
                if savings_rate < 20:
                    recommendations.append({
                        "type": "low_savings_rate",
                        "message": f"Your savings rate is {savings_rate:.1f}% of your income.",
                        "suggestion": "Aim to save at least 20% of your income. Consider setting up automatic transfers to savings."
                    })
            
            return {
                "success": True,
                "data": {
                    "recommendations": recommendations,
                    "analysis_period": f"Last {len(recent_expenses)} days",
                    "total_recommendations": len(recommendations)
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_merchant_analysis(self, args: Dict = None) -> Dict:
        """Analyze spending patterns by merchant"""
        try:
            df = self.transactions_df.copy()
            expenses_df = df[df['transaction_type'] == 'expense']
            
            # Filter by date range if provided
            if args and 'start_date' in args and args['start_date']:
                start_date = pd.to_datetime(args['start_date'])
                expenses_df = expenses_df[expenses_df['date'] >= start_date]
            
            if args and 'end_date' in args and args['end_date']:
                end_date = pd.to_datetime(args['end_date'])
                expenses_df = expenses_df[expenses_df['date'] <= end_date]
            
            # Merchant analysis
            merchant_analysis = expenses_df.groupby('merchant').agg({
                'amount': ['sum', 'count', 'mean'],
                'category': 'first',
                'date': ['min', 'max']
            }).reset_index()
            
            merchant_analysis.columns = ['merchant', 'total_spent', 'transaction_count', 'avg_amount', 'category', 'first_transaction', 'last_transaction']
            merchant_analysis = merchant_analysis.sort_values('total_spent', ascending=False)
            
            # Convert to serializable format
            merchant_data = []
            for _, row in merchant_analysis.iterrows():
                merchant_data.append({
                    "merchant": row['merchant'],
                    "total_spent": float(row['total_spent']),
                    "transaction_count": int(row['transaction_count']),
                    "avg_amount": float(row['avg_amount']),
                    "category": row['category'],
                    "first_transaction": str(row['first_transaction']),
                    "last_transaction": str(row['last_transaction'])
                })
            
            return {
                "success": True,
                "data": {
                    "merchant_analysis": merchant_data,
                    "total_merchants": len(merchant_data),
                    "total_spent": float(merchant_analysis['total_spent'].sum())
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_trend_analysis(self, args: Dict = None) -> Dict:
        """Analyze spending trends over time"""
        try:
            df = self.transactions_df.copy()
            expenses_df = df[df['transaction_type'] == 'expense']
            
            # Filter by date range if provided
            if args and 'start_date' in args and args['start_date']:
                start_date = pd.to_datetime(args['start_date'])
                expenses_df = expenses_df[expenses_df['date'] >= start_date]
            
            if args and 'end_date' in args and args['end_date']:
                end_date = pd.to_datetime(args['end_date'])
                expenses_df = expenses_df[expenses_df['date'] <= end_date]
            
            # Daily spending trend
            daily_spending = expenses_df.groupby('date')['amount'].sum()
            
            # Weekly spending trend
            weekly_spending = expenses_df.groupby(expenses_df['date'].dt.to_period('W'))['amount'].sum()
            
            # Monthly spending trend
            monthly_spending = expenses_df.groupby(expenses_df['date'].dt.to_period('M'))['amount'].sum()
            
            # Category trends over time
            category_monthly = expenses_df.groupby([expenses_df['date'].dt.to_period('M'), 'category'])['amount'].sum().unstack(fill_value=0)
            
            # Calculate growth rates
            if len(monthly_spending) > 1:
                monthly_growth = monthly_spending.pct_change().dropna()
                avg_monthly_growth = float(monthly_growth.mean())
            else:
                avg_monthly_growth = 0
            
            return {
                "success": True,
                "data": {
                    "daily_trend": {str(k): float(v) for k, v in daily_spending.items()},
                    "weekly_trend": {str(k): float(v) for k, v in weekly_spending.items()},
                    "monthly_trend": {str(k): float(v) for k, v in monthly_spending.items()},
                    "category_trends": category_monthly.to_dict(),
                    "trend_metrics": {
                        "avg_daily_spending": float(daily_spending.mean()),
                        "avg_weekly_spending": float(weekly_spending.mean()),
                        "avg_monthly_spending": float(monthly_spending.mean()),
                        "avg_monthly_growth": avg_monthly_growth,
                        "spending_volatility": float(daily_spending.std())
                    }
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_chart(self, args: Dict) -> Dict:
        """Generate financial charts and save them"""
        try:
            chart_type = args.get('chart_type', 'category_breakdown')
            
            # Create charts directory if it doesn't exist
            os.makedirs('charts', exist_ok=True)
            
            if chart_type == 'category_breakdown':
                return self._generate_category_chart()
            elif chart_type == 'spending_trend':
                return self._generate_trend_chart()
            elif chart_type == 'budget_vs_actual':
                return self._generate_budget_chart()
            elif chart_type == 'merchant_analysis':
                return self._generate_merchant_chart()
            else:
                return {"success": False, "error": f"Unknown chart type: {chart_type}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_category_chart(self) -> Dict:
        """Generate category breakdown pie chart"""
        expenses_df = self.transactions_df[self.transactions_df['transaction_type'] == 'expense']
        category_spending = expenses_df.groupby('category')['amount'].sum()
        
        plt.figure(figsize=(10, 8))
        plt.pie(category_spending.values, labels=category_spending.index, autopct='%1.1f%%')
        plt.title('Spending by Category')
        plt.axis('equal')
        
        chart_path = 'charts/category_breakdown.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "success": True,
            "data": {
                "chart_path": chart_path,
                "chart_type": "category_breakdown",
                "total_categories": len(category_spending)
            }
        }
    
    def _generate_trend_chart(self) -> Dict:
        """Generate spending trend line chart"""
        expenses_df = self.transactions_df[self.transactions_df['transaction_type'] == 'expense']
        daily_spending = expenses_df.groupby('date')['amount'].sum()
        
        plt.figure(figsize=(12, 6))
        plt.plot(daily_spending.index, daily_spending.values, marker='o')
        plt.title('Daily Spending Trend')
        plt.xlabel('Date')
        plt.ylabel('Amount ($)')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        chart_path = 'charts/spending_trend.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "success": True,
            "data": {
                "chart_path": chart_path,
                "chart_type": "spending_trend",
                "data_points": len(daily_spending)
            }
        }
    
    def _generate_budget_chart(self) -> Dict:
        """Generate budget vs actual spending chart"""
        expenses_df = self.transactions_df[self.transactions_df['transaction_type'] == 'expense']
        category_spending = expenses_df.groupby('category')['amount'].sum()
        
        # Get budget data
        budget_data = []
        actual_data = []
        categories = []
        
        for category, budget in self.category_budgets.items():
            if category in category_spending:
                categories.append(category)
                budget_data.append(budget)
                actual_data.append(float(category_spending[category]))
        
        x = range(len(categories))
        width = 0.35
        
        plt.figure(figsize=(12, 8))
        plt.bar([i - width/2 for i in x], budget_data, width, label='Budget', alpha=0.8)
        plt.bar([i + width/2 for i in x], actual_data, width, label='Actual', alpha=0.8)
        
        plt.xlabel('Categories')
        plt.ylabel('Amount ($)')
        plt.title('Budget vs Actual Spending')
        plt.xticks(x, categories, rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        chart_path = 'charts/budget_vs_actual.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "success": True,
            "data": {
                "chart_path": chart_path,
                "chart_type": "budget_vs_actual",
                "categories_compared": len(categories)
            }
        }
    
    def _generate_merchant_chart(self) -> Dict:
        """Generate top merchants bar chart"""
        expenses_df = self.transactions_df[self.transactions_df['transaction_type'] == 'expense']
        merchant_spending = expenses_df.groupby('merchant')['amount'].sum().sort_values(ascending=False).head(10)
        
        plt.figure(figsize=(12, 8))
        plt.barh(merchant_spending.index, merchant_spending.values)
        plt.title('Top 10 Merchants by Spending')
        plt.xlabel('Amount ($)')
        plt.ylabel('Merchant')
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3)
        
        chart_path = 'charts/merchant_analysis.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "success": True,
            "data": {
                "chart_path": chart_path,
                "chart_type": "merchant_analysis",
                "merchants_shown": len(merchant_spending)
            }
        }
    
    def list_tools(self) -> List[Dict]:
        """List all available MCP tools"""
        return [
            {
                "name": "get_transactions",
                "description": "Get financial transactions with optional filtering by category, type, date range, or merchant",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Filter by transaction category"},
                        "type": {"type": "string", "description": "Filter by transaction type ('expense' or 'income')"},
                        "start_date": {"type": "string", "description": "Start date for filtering (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for filtering (YYYY-MM-DD format)"},
                        "merchant": {"type": "string", "description": "Filter by merchant name"}
                    }
                }
            },
            {
                "name": "get_spending_analysis",
                "description": "Get comprehensive spending analysis including category breakdown, monthly trends, and top merchants",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "start_date": {"type": "string", "description": "Start date for analysis (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for analysis (YYYY-MM-DD format)"}
                    }
                }
            },
            {
                "name": "get_budget_analysis",
                "description": "Analyze spending against predefined budget categories and identify overspending areas",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "start_date": {"type": "string", "description": "Start date for analysis (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for analysis (YYYY-MM-DD format)"}
                    }
                }
            },
            {
                "name": "get_spending_recommendations",
                "description": "Generate personalized spending recommendations based on spending patterns",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "start_date": {"type": "string", "description": "Start date for analysis (YYYY-MM-DD format)"}
                    }
                }
            },
            {
                "name": "get_merchant_analysis",
                "description": "Analyze spending patterns by merchant including frequency and amounts",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "start_date": {"type": "string", "description": "Start date for analysis (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for analysis (YYYY-MM-DD format)"}
                    }
                }
            },
            {
                "name": "get_trend_analysis",
                "description": "Analyze spending trends over time including daily, weekly, and monthly patterns",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "start_date": {"type": "string", "description": "Start date for analysis (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for analysis (YYYY-MM-DD format)"}
                    }
                }
            },
            {
                "name": "generate_chart",
                "description": "Generate financial charts including category breakdown, spending trends, budget analysis, and merchant analysis",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "chart_type": {
                            "type": "string",
                            "enum": ["category_breakdown", "spending_trend", "budget_vs_actual", "merchant_analysis"],
                            "description": "Type of chart to generate"
                        }
                    },
                    "required": ["chart_type"]
                }
            }
        ]
    
    def call_tool(self, tool_name: str, args: Dict = None) -> Dict:
        """Call the specified tool with given arguments"""
        args = args or {}
        
        if tool_name == "get_transactions":
            return self.get_transactions(args)
        elif tool_name == "get_spending_analysis":
            return self.get_spending_analysis(args)
        elif tool_name == "get_budget_analysis":
            return self.get_budget_analysis(args)
        elif tool_name == "get_spending_recommendations":
            return self.get_spending_recommendations(args)
        elif tool_name == "get_merchant_analysis":
            return self.get_merchant_analysis(args)
        elif tool_name == "get_trend_analysis":
            return self.get_trend_analysis(args)
        elif tool_name == "generate_chart":
            return self.generate_chart(args)
        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}

# Example usage
if __name__ == "__main__":
    server = FinancialMCPServer()
    
    # Example: Get all transactions
    result = server.get_transactions()
    print("Transactions:", json.dumps(result, indent=2))
    
    # Example: Get spending analysis
    result = server.get_spending_analysis()
    print("Spending Analysis:", json.dumps(result, indent=2))
    
    # Example: Generate a chart
    result = server.generate_chart({"chart_type": "category_breakdown"})
    print("Chart Generation:", json.dumps(result, indent=2)) 