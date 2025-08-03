from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from dateutil.relativedelta import relativedelta
import uuid

app = FastAPI(
    title="Financial Wellness API",
    description="AI-powered financial wellness platform with MCP integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Transaction(BaseModel):
    id: Optional[int] = None
    date: str
    amount: float
    category: str
    description: str
    type: str  # "expense" or "income"
    tags: List[str] = []

class SavingsGoal(BaseModel):
    id: Optional[int] = None
    name: str
    target_amount: float
    current_amount: float
    deadline: str
    description: str
    priority: str = "medium"

class Budget(BaseModel):
    category: str
    monthly_limit: float
    current_spent: float
    remaining: float

class UserProfile(BaseModel):
    name: str
    email: str
    currency: str = "USD"
    monthly_income: float
    preferred_categories: List[str] = []
    financial_goals: List[str] = []

# Global data storage
DATA_FILE = "financial_data.json"

def load_data():
    """Load financial data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "transactions": [],
        "budgets": {},
        "savings_goals": [],
        "user_profile": {},
        "analytics": {}
    }

def save_data(data):
    """Save financial data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def update_analytics(data):
    """Update analytics based on current data"""
    transactions = data.get("transactions", [])
    
    if not transactions:
        data["analytics"] = {
            "total_income": 0,
            "total_expenses": 0,
            "net_savings": 0,
            "savings_rate": 0,
            "top_spending_categories": [],
            "monthly_trends": {"income": [], "expenses": [], "savings": []}
        }
        return
    
    # Calculate totals
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    net_savings = total_income - total_expenses
    savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0
    
    # Top spending categories
    expense_transactions = [t for t in transactions if t["type"] == "expense"]
    category_totals = {}
    for t in expense_transactions:
        category = t["category"]
        category_totals[category] = category_totals.get(category, 0) + t["amount"]
    
    top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    top_spending_categories = [{"category": cat, "amount": amt} for cat, amt in top_categories]
    
    # Monthly trends (simplified)
    current_month = datetime.now().month
    monthly_income = sum(t["amount"] for t in transactions 
                        if t["type"] == "income" and datetime.strptime(t["date"], "%Y-%m-%d").month == current_month)
    monthly_expenses = sum(t["amount"] for t in transactions 
                          if t["type"] == "expense" and datetime.strptime(t["date"], "%Y-%m-%d").month == current_month)
    
    data["analytics"] = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings,
        "savings_rate": round(savings_rate, 2),
        "top_spending_categories": top_spending_categories,
        "monthly_trends": {
            "income": [monthly_income],
            "expenses": [monthly_expenses],
            "savings": [monthly_income - monthly_expenses]
        }
    }

def update_budgets(data):
    """Update budget calculations based on current transactions"""
    transactions = data.get("transactions", [])
    budgets = data.get("budgets", {})
    
    # Calculate current spending by category
    category_spending = {}
    for transaction in transactions:
        if transaction["type"] == "expense":
            category = transaction["category"]
            category_spending[category] = category_spending.get(category, 0) + transaction["amount"]
    
    # Update budget remaining amounts
    for category, budget_info in budgets.items():
        current_spent = category_spending.get(category, 0)
        budget_info["current_spent"] = current_spent
        budget_info["remaining"] = budget_info["monthly_limit"] - current_spent
    
    data["budgets"] = budgets

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Financial Wellness API",
        "version": "1.0.0",
        "endpoints": {
            "transactions": "/transactions",
            "budgets": "/budget",
            "savings_goals": "/savings-goals",
            "analytics": "/analytics",
            "charts": "/charts/{chart_type}"
        }
    }

@app.get("/transactions")
async def get_transactions(
    category: Optional[str] = Query(None, description="Filter by category"),
    type: Optional[str] = Query(None, description="Filter by type (expense/income)"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get all transactions with optional filtering"""
    data = load_data()
    transactions = data.get("transactions", [])
    
    # Apply filters
    if category:
        transactions = [t for t in transactions if t["category"] == category]
    if type:
        transactions = [t for t in transactions if t["type"] == type]
    if start_date:
        transactions = [t for t in transactions if t["date"] >= start_date]
    if end_date:
        transactions = [t for t in transactions if t["date"] <= end_date]
    
    return {"transactions": transactions}

@app.post("/transactions")
async def add_transaction(transaction: Transaction):
    """Add a new transaction"""
    data = load_data()
    
    # Generate ID if not provided
    if transaction.id is None:
        transaction.id = max([t["id"] for t in data.get("transactions", [])], default=0) + 1
    
    # Convert to dict and add
    transaction_dict = transaction.dict()
    data["transactions"].append(transaction_dict)
    
    # Update analytics and budgets
    update_analytics(data)
    update_budgets(data)
    
    save_data(data)
    return {"message": "Transaction added successfully", "transaction": transaction_dict}

@app.get("/budget")
async def get_budget_status():
    """Get current budget status"""
    data = load_data()
    return {"budgets": data.get("budgets", {})}

@app.post("/budget")
async def create_budget(budget: Budget):
    """Create or update a budget category"""
    data = load_data()
    
    data["budgets"][budget.category] = {
        "monthly_limit": budget.monthly_limit,
        "current_spent": budget.current_spent,
        "remaining": budget.remaining
    }
    
    save_data(data)
    return {"message": "Budget created successfully", "budget": budget.dict()}

@app.get("/savings-goals")
async def get_savings_goals():
    """Get all savings goals"""
    data = load_data()
    return {"savings_goals": data.get("savings_goals", [])}

@app.post("/savings-goals")
async def create_savings_goal(goal: SavingsGoal):
    """Create a new savings goal"""
    data = load_data()
    
    # Generate ID if not provided
    if goal.id is None:
        goal.id = max([g["id"] for g in data.get("savings_goals", [])], default=0) + 1
    
    goal_dict = goal.dict()
    data["savings_goals"].append(goal_dict)
    
    save_data(data)
    return {"message": "Savings goal created successfully", "goal": goal_dict}

@app.put("/savings-goals/{goal_id}")
async def update_savings_goal(goal_id: int, goal: SavingsGoal):
    """Update a savings goal"""
    data = load_data()
    goals = data.get("savings_goals", [])
    
    for i, existing_goal in enumerate(goals):
        if existing_goal["id"] == goal_id:
            goal.id = goal_id
            goals[i] = goal.dict()
            save_data(data)
            return {"message": "Savings goal updated successfully", "goal": goal.dict()}
    
    raise HTTPException(status_code=404, detail="Savings goal not found")

@app.get("/analytics")
async def get_analytics():
    """Get financial analytics"""
    data = load_data()
    return {"analytics": data.get("analytics", {})}

@app.get("/spending-analysis")
async def get_spending_analysis(
    days: int = Query(30, description="Number of days to analyze")
):
    """Get detailed spending analysis"""
    data = load_data()
    transactions = data.get("transactions", [])
    
    # Filter transactions by date
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_transactions = [
        t for t in transactions 
        if datetime.strptime(t["date"], "%Y-%m-%d") >= cutoff_date
    ]
    
    # Category analysis
    category_totals = {}
    daily_spending = {}
    
    for transaction in recent_transactions:
        if transaction["type"] == "expense":
            category = transaction["category"]
            amount = transaction["amount"]
            date = transaction["date"]
            
            category_totals[category] = category_totals.get(category, 0) + amount
            daily_spending[date] = daily_spending.get(date, 0) + amount
    
    # Calculate insights
    total_spent = sum(category_totals.values())
    avg_daily_spending = total_spent / days if days > 0 else 0
    top_category = max(category_totals.items(), key=lambda x: x[1]) if category_totals else None
    
    return {
        "period_days": days,
        "total_spent": total_spent,
        "average_daily_spending": round(avg_daily_spending, 2),
        "category_breakdown": category_totals,
        "daily_spending": daily_spending,
        "top_spending_category": top_category,
        "transaction_count": len(recent_transactions)
    }

@app.get("/charts/{chart_type}")
async def generate_chart(chart_type: str):
    """Generate various financial charts"""
    data = load_data()
    transactions = data.get("transactions", [])
    
    if not transactions:
        raise HTTPException(status_code=404, detail="No data available for charts")
    
    # Create charts directory if it doesn't exist
    os.makedirs("client/generated_graphs", exist_ok=True)
    
    if chart_type == "spending_by_category":
        # Pie chart of spending by category
        expense_transactions = [t for t in transactions if t["type"] == "expense"]
        category_totals = {}
        for t in expense_transactions:
            category = t["category"]
            category_totals[category] = category_totals.get(category, 0) + t["amount"]
        
        fig = px.pie(
            values=list(category_totals.values()),
            names=list(category_totals.keys()),
            title="Spending by Category"
        )
        fig.write_image("client/generated_graphs/spending_by_category.png")
        return FileResponse("client/generated_graphs/spending_by_category.png")
    
    elif chart_type == "monthly_trends":
        # Line chart of income vs expenses over time
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        monthly_data = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        
        fig = px.line(
            monthly_data,
            title="Monthly Income vs Expenses",
            labels={'value': 'Amount ($)', 'month': 'Month'}
        )
        fig.write_image("client/generated_graphs/monthly_trends.png")
        return FileResponse("client/generated_graphs/monthly_trends.png")
    
    elif chart_type == "budget_vs_actual":
        # Bar chart comparing budget vs actual spending
        budgets = data.get("budgets", {})
        categories = list(budgets.keys())
        budgeted = [budgets[cat]["monthly_limit"] for cat in categories]
        actual = [budgets[cat]["current_spent"] for cat in categories]
        
        fig = go.Figure(data=[
            go.Bar(name='Budgeted', x=categories, y=budgeted),
            go.Bar(name='Actual', x=categories, y=actual)
        ])
        fig.update_layout(title="Budget vs Actual Spending", barmode='group')
        fig.write_image("client/generated_graphs/budget_vs_actual.png")
        return FileResponse("client/generated_graphs/budget_vs_actual.png")
    
    elif chart_type == "savings_progress":
        # Progress bars for savings goals
        goals = data.get("savings_goals", [])
        if not goals:
            raise HTTPException(status_code=404, detail="No savings goals found")
        
        names = [g["name"] for g in goals]
        current = [g["current_amount"] for g in goals]
        target = [g["target_amount"] for g in goals]
        progress = [c/t*100 for c, t in zip(current, target)]
        
        fig = go.Figure(data=[
            go.Bar(name='Current', x=names, y=current),
            go.Bar(name='Target', x=names, y=target)
        ])
        fig.update_layout(title="Savings Goals Progress", barmode='group')
        fig.write_image("client/generated_graphs/savings_progress.png")
        return FileResponse("client/generated_graphs/savings_progress.png")
    
    else:
        raise HTTPException(status_code=400, detail=f"Unknown chart type: {chart_type}")

@app.get("/recommendations")
async def get_recommendations():
    """Get personalized financial recommendations"""
    data = load_data()
    transactions = data.get("transactions", [])
    budgets = data.get("budgets", {})
    goals = data.get("savings_goals", [])
    
    recommendations = []
    
    # Analyze spending patterns
    expense_transactions = [t for t in transactions if t["type"] == "expense"]
    category_totals = {}
    for t in expense_transactions:
        category = t["category"]
        category_totals[category] = category_totals.get(category, 0) + t["amount"]
    
    # Budget recommendations
    for category, budget_info in budgets.items():
        if budget_info["current_spent"] > budget_info["monthly_limit"] * 0.8:
            recommendations.append({
                "type": "budget_warning",
                "category": category,
                "message": f"You're approaching your {category} budget limit. Consider reducing spending in this category.",
                "severity": "medium"
            })
    
    # Savings recommendations
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    savings_rate = (total_income - total_expenses) / total_income if total_income > 0 else 0
    
    if savings_rate < 0.2:
        recommendations.append({
            "type": "savings_advice",
            "message": "Your savings rate is below 20%. Consider setting up automatic savings transfers.",
            "severity": "high"
        })
    
    # Goal recommendations
    for goal in goals:
        days_remaining = (datetime.strptime(goal["deadline"], "%Y-%m-%d") - datetime.now()).days
        if days_remaining > 0:
            needed_per_month = (goal["target_amount"] - goal["current_amount"]) / (days_remaining / 30)
            if needed_per_month > total_income * 0.3:
                recommendations.append({
                    "type": "goal_alert",
                    "goal": goal["name"],
                    "message": f"To reach your {goal['name']} goal, you need to save ${needed_per_month:.2f} per month.",
                    "severity": "high"
                })
    
    return {"recommendations": recommendations}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 