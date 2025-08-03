# Enhanced Financial Wellness AI Chatbot

A comprehensive AI-powered financial analysis platform that uses daily transaction data to provide deep insights, spending analysis, and personalized recommendations. Built with an enhanced MCP (Model Context Protocol) server and Gemini AI integration.

## 🚀 Features

### 📊 **Comprehensive Financial Analysis**
- **Transaction Analysis**: Filter and analyze transactions by category, date, merchant, and type
- **Spending Breakdown**: Detailed category-wise spending analysis with percentages
- **Budget Tracking**: Real-time budget vs actual spending comparison
- **Merchant Analysis**: Top merchants by spending and transaction frequency
- **Trend Analysis**: Daily, weekly, and monthly spending patterns
- **Growth Metrics**: Spending growth rates and volatility analysis

### 🤖 **AI-Powered Insights**
- **Natural Language Queries**: Ask questions in plain English
- **Personalized Recommendations**: AI-generated spending advice
- **Smart Filtering**: Automatic date range detection from queries
- **Conversation Memory**: Maintains context across multiple queries
- **Intelligent Responses**: Formatted, easy-to-understand financial insights

### 📈 **Data Visualization**
- **Category Breakdown Charts**: Pie charts showing spending distribution
- **Spending Trend Charts**: Line charts tracking spending over time
- **Budget vs Actual Charts**: Bar charts comparing budget to actual spending
- **Merchant Analysis Charts**: Horizontal bar charts of top merchants
- **Auto-generated Visualizations**: Charts saved as high-quality PNG files

### 🔧 **Advanced MCP Integration**
- **7 Core Tools**: Comprehensive financial analysis capabilities
- **Flexible Filtering**: Multiple filter combinations for precise analysis
- **Real-time Processing**: Instant analysis of transaction data
- **Extensible Architecture**: Easy to add new analysis tools

## 📁 Project Structure

```
mcp_ai_chatbot/
├── daily_transactions.csv          # Daily transaction dataset (95 transactions)
├── financial_mcp_server.py         # Enhanced MCP server with analysis tools
├── enhanced_financial_client.py    # AI-powered client with natural language processing
├── demo_financial_analysis.py      # Comprehensive demo script
├── config.json                     # API keys and configuration
├── requirements.txt                # Python dependencies
├── charts/                         # Auto-generated financial charts
└── README.md                       # Original project documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Google Gemini API key
- Internet connection

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Create or update `config.json`:
```json
{
  "GOOGLE_API_KEY": "your-gemini-api-key-here",
  "API_KEY": "your-api-key-here",
  "API_URL": "http://localhost:8000"
}
```

### 3. Verify Dataset
The system includes a comprehensive daily transactions dataset with 95 realistic transactions covering:
- 10 spending categories (Groceries, Food & Dining, Transportation, etc.)
- Multiple merchants and transaction types
- Realistic amounts and dates
- Income and expense transactions

## 🚀 Quick Start

### Option 1: Interactive Chatbot
```bash
python enhanced_financial_client.py
```

### Option 2: Run Demo
```bash
python demo_financial_analysis.py
```

### Option 3: Direct MCP Server Usage
```python
from financial_mcp_server import FinancialMCPServer

# Initialize server
server = FinancialMCPServer()

# Get spending analysis
result = server.get_spending_analysis()
print(result)
```

## 💬 Example Queries

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

### Trend Analysis
- "Show me my spending trends"
- "How has my spending changed over time?"
- "What's my average daily spending?"

### Chart Generation
- "Generate a spending category chart"
- "Create a budget vs actual chart"
- "Show me a merchant analysis chart"

## 🔧 MCP Tools Available

### 1. `get_transactions`
**Purpose**: Retrieve and filter financial transactions
**Filters**: category, type, start_date, end_date, merchant
**Example**: Get all food & dining transactions from last month

### 2. `get_spending_analysis`
**Purpose**: Comprehensive spending breakdown and analysis
**Features**: Category breakdown, income vs expenses, top merchants
**Example**: Complete spending summary with category percentages

### 3. `get_budget_analysis`
**Purpose**: Compare actual spending against budget categories
**Features**: Over/under budget alerts, remaining amounts
**Example**: Identify categories exceeding budget limits

### 4. `get_spending_recommendations`
**Purpose**: AI-generated personalized financial advice
**Features**: Overspending alerts, savings suggestions, optimization tips
**Example**: Recommendations based on spending patterns

### 5. `get_merchant_analysis`
**Purpose**: Analyze spending patterns by merchant
**Features**: Top merchants, transaction frequency, spending amounts
**Example**: Identify most frequent and expensive merchants

### 6. `get_trend_analysis`
**Purpose**: Analyze spending trends over time
**Features**: Daily/weekly/monthly trends, growth rates, volatility
**Example**: Track spending patterns and identify trends

### 7. `generate_chart`
**Purpose**: Create visual representations of financial data
**Chart Types**: category_breakdown, spending_trend, budget_vs_actual, merchant_analysis
**Example**: Generate pie chart of spending categories

## 📊 Sample Data Analysis

The system includes a realistic dataset with the following characteristics:

### Transaction Categories
- **Groceries**: $1,245.50 (13 transactions)
- **Food & Dining**: $1,085.00 (17 transactions)
- **Shopping**: $3,675.00 (15 transactions)
- **Transportation**: $675.00 (15 transactions)
- **Entertainment**: $1,635.00 (12 transactions)
- **Healthcare**: $695.00 (7 transactions)
- **Utilities**: $560.00 (7 transactions)
- **Rent**: $1,200.00 (1 transaction)
- **Income**: $2,500.00 (1 transaction)

### Key Insights
- **Total Expenses**: $11,770.50
- **Total Income**: $2,500.00
- **Net Income**: -$9,270.50
- **Average Daily Spending**: $392.35
- **Most Expensive Category**: Shopping ($3,675.00)
- **Most Frequent Category**: Food & Dining (17 transactions)

## 🎯 Advanced Features

### Natural Language Processing
- **Query Understanding**: Automatically detects intent from natural language
- **Date Extraction**: Converts "this month", "last week" to actual dates
- **Context Awareness**: Maintains conversation context across queries
- **Smart Filtering**: Combines multiple filters intelligently

### Intelligent Recommendations
- **Overspending Detection**: Identifies categories exceeding budget
- **Frequent Purchase Analysis**: Highlights repetitive small transactions
- **Savings Rate Analysis**: Evaluates income vs spending ratio
- **Actionable Advice**: Provides specific, implementable suggestions

### Data Visualization
- **Professional Charts**: High-quality, publication-ready visualizations
- **Multiple Chart Types**: Pie, line, bar, and horizontal bar charts
- **Auto-save**: Charts automatically saved to `charts/` directory
- **Customizable**: Easy to modify chart styles and colors

## 🔍 Sample Output

### Spending Analysis Response
```
**Spending Summary:**
• Total Expenses: $11,770.50
• Total Income: $2,500.00
• Net Income: -$9,270.50

**Spending by Category:**
• Shopping: $3,675.00 (15 transactions)
• Entertainment: $1,635.00 (12 transactions)
• Groceries: $1,245.50 (13 transactions)
• Food & Dining: $1,085.00 (17 transactions)
• Transportation: $675.00 (15 transactions)
```

### Budget Analysis Response
```
**Budget Analysis:**

⚠️ Over Budget Categories:
• Shopping: $3,675.00 spent vs $250.00 budget ($3,425.00 over)
• Entertainment: $1,635.00 spent vs $150.00 budget ($1,485.00 over)

✅ Under Budget Categories:
• Healthcare: $695.00 spent vs $100.00 budget ($595.00 remaining)
• Utilities: $560.00 spent vs $200.00 budget ($240.00 remaining)
```

### Recommendations Response
```
💡 Personalized Recommendations:

1. Overspending Alert:
   You've spent $3,675.00 on Shopping, which is $3,425.00 over your $250 budget.
   💡 Consider reducing Shopping spending by $114.17 per day to stay on track.

2. Frequent Purchases:
   You've made 17 purchases at Food & Dining totaling $1,085.00.
   💡 Consider bulk purchases or subscriptions to reduce frequent small transactions.
```

## 🚀 Getting Started Examples

### 1. Basic Usage
```python
from enhanced_financial_client import EnhancedFinancialClient

# Initialize client
client = EnhancedFinancialClient("your-api-key")

# Ask questions
response = await client.process_query("How much did I spend this month?")
print(response)
```

### 2. Direct MCP Server Usage
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

### 3. Custom Analysis
```python
# Filter transactions by category
result = server.get_transactions({'category': 'Food & Dining'})

# Analyze specific date range
result = server.get_spending_analysis({
    'start_date': '2024-01-01',
    'end_date': '2024-01-15'
})

# Get merchant analysis
result = server.get_merchant_analysis()
```

## 🔧 Customization

### Adding New Categories
Edit the `category_budgets` dictionary in `financial_mcp_server.py`:
```python
self.category_budgets = {
    'Groceries': 400,
    'Food & Dining': 300,
    'Transportation': 200,
    # Add your custom categories here
    'Custom Category': 150,
}
```

### Modifying Budget Amounts
Update budget amounts in the same dictionary:
```python
'Groceries': 500,  # Increased from 400
'Entertainment': 200,  # Increased from 150
```

### Adding New Chart Types
Extend the `generate_chart` method in `financial_mcp_server.py`:
```python
elif chart_type == 'custom_chart':
    return self._generate_custom_chart()
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Error**: Verify your Google API key in `config.json`
   ```json
   {
     "GOOGLE_API_KEY": "your-actual-api-key"
   }
   ```

3. **Chart Generation Error**: Ensure matplotlib is properly installed
   ```bash
   pip install matplotlib seaborn
   ```

4. **Data Loading Error**: Check if `daily_transactions.csv` exists
   ```bash
   ls -la daily_transactions.csv
   ```

### Debug Mode
Enable debug output by modifying the server initialization:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance

### Dataset Size
- **Transactions**: 95 realistic transactions
- **Categories**: 10 spending categories
- **Merchants**: 50+ unique merchants
- **Time Period**: January 2024 (31 days)

### Processing Speed
- **Transaction Analysis**: < 100ms
- **Spending Analysis**: < 200ms
- **Chart Generation**: < 500ms
- **Natural Language Processing**: < 1s

## 🔮 Future Enhancements

### Planned Features
- **Real-time Bank Integration**: Connect to actual bank accounts
- **Machine Learning Predictions**: Predict future spending patterns
- **Multi-currency Support**: Handle different currencies
- **Export Functionality**: Export reports to PDF/Excel
- **Mobile App Integration**: Native mobile application
- **Advanced Gamification**: Rewards and challenges

### Extensibility
- **Plugin System**: Easy addition of new analysis tools
- **Custom Data Sources**: Support for different data formats
- **API Endpoints**: RESTful API for external integrations
- **Web Dashboard**: Web-based user interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For technical support or questions:
1. Check the troubleshooting section
2. Review the demo script for examples
3. Examine the source code for implementation details
4. Create an issue on the repository

---

**Ready to take control of your finances? Start with the Enhanced Financial Wellness AI Chatbot today!** 🚀 