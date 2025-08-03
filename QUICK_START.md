# 🚀 Quick Start Guide - Financial Wellness AI Chatbot

Get up and running with the enhanced financial analysis system in 5 minutes!

## ⚡ Quick Setup

### 1. Install Dependencies
```bash
pip3 install pandas matplotlib seaborn numpy google-generativeai
```

### 2. Verify Configuration
Make sure your `config.json` has your Google API key:
```json
{
  "GOOGLE_API_KEY": "your-actual-gemini-api-key",
  "API_KEY": "your-api-key-here",
  "API_URL": "http://localhost:8000"
}
```

### 3. Run the Demo
```bash
python3 demo_financial_analysis.py
```

### 4. Start the Chatbot
```bash
python3 enhanced_financial_client.py
```

## 💬 Try These Queries

### Basic Analysis
- "How much did I spend this month?"
- "Show me my spending by category"
- "What are my top 5 transactions?"

### Budget Analysis
- "Am I over budget in any categories?"
- "Show me my budget status"
- "Which categories am I under budget in?"

### Recommendations
- "Give me spending recommendations"
- "How can I save money?"
- "What should I improve in my spending?"

### Merchant Analysis
- "What are my top merchants?"
- "Where do I spend the most money?"
- "Show me my spending at Amazon"

### Charts
- "Generate a spending category chart"
- "Create a budget vs actual chart"
- "Show me a merchant analysis chart"

## 📊 What You'll See

### Demo Output
```
🚀 Financial Wellness AI Chatbot - Comprehensive Demo
============================================================
📊 Initializing Financial MCP Server...
Loaded 95 transactions from daily_transactions.csv

✅ Found 95 transactions totaling $14,515.99
✅ Spending Summary:
  • Total Expenses: $11,515.99
  • Total Income: $2,500.00
  • Net Income: -$9,015.99
```

### Chatbot Interaction
```
🤖 Enhanced Financial Wellness AI Chatbot
==================================================
Ask me anything about your finances!

👤 You: How much did I spend this month?
🤖 Assistant: Analyzing your financial data...

**Spending Summary:**
• Total Expenses: $11,515.99
• Total Income: $2,500.00
• Net Income: -$9,015.99
```

## 📈 Generated Charts

After running the demo, check the `charts/` folder for:
- `category_breakdown.png` - Spending by category pie chart
- `spending_trend.png` - Daily spending trend line chart
- `budget_vs_actual.png` - Budget comparison bar chart
- `merchant_analysis.png` - Top merchants horizontal bar chart

## 🔧 Direct API Usage

```python
from financial_mcp_server import FinancialMCPServer

# Initialize server
server = FinancialMCPServer()

# Get spending analysis
result = server.get_spending_analysis()
print(f"Total expenses: ${result['data']['summary']['total_expenses']:,.2f}")

# Generate chart
chart_result = server.generate_chart({'chart_type': 'category_breakdown'})
print(f"Chart saved to: {chart_result['data']['chart_path']}")
```

## 🎯 Key Features

✅ **95 Realistic Transactions** - Comprehensive financial dataset
✅ **7 Analysis Tools** - Complete financial analysis capabilities
✅ **Natural Language Queries** - Ask questions in plain English
✅ **AI Recommendations** - Personalized financial advice
✅ **Professional Charts** - High-quality visualizations
✅ **Budget Tracking** - Real-time budget vs actual comparison
✅ **Trend Analysis** - Spending patterns over time
✅ **Merchant Analysis** - Top spending locations

## 🚨 Troubleshooting

### Common Issues

1. **"Module not found" error**
   ```bash
   pip3 install pandas matplotlib seaborn numpy google-generativeai
   ```

2. **"API key not found" error**
   - Check your `config.json` file
   - Verify your Google Gemini API key is correct

3. **"No transactions found" error**
   - Ensure `daily_transactions.csv` exists in the project directory
   - The file should contain 95 transactions

4. **Chart generation fails**
   - Check if `charts/` directory exists
   - Ensure matplotlib is properly installed

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📋 Sample Data Overview

The system includes 95 realistic transactions covering:
- **10 Categories**: Groceries, Food & Dining, Transportation, Entertainment, Shopping, Healthcare, Utilities, Rent, Savings, Income
- **50+ Merchants**: Realistic merchant names like Whole Foods, Amazon, Uber, etc.
- **31 Days**: January 2024 transaction data
- **Multiple Types**: Income, expenses, and transfers

## 🎉 Success Indicators

You'll know everything is working when you see:
- ✅ "Loaded 95 transactions from daily_transactions.csv"
- ✅ Demo runs without errors
- ✅ Charts are generated in the `charts/` folder
- ✅ Chatbot responds to natural language queries
- ✅ All 9 demo sections complete successfully

## 🚀 Next Steps

1. **Try the Interactive Chatbot**: Ask questions about your finances
2. **Explore the Charts**: View the generated visualizations
3. **Run Custom Analysis**: Use the MCP server directly
4. **Modify the Data**: Update `daily_transactions.csv` with your own data
5. **Extend Functionality**: Add new analysis tools or chart types

---

**🎯 Ready to analyze your finances? Start with the demo and then dive into the interactive chatbot!** 