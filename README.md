# 🏦 Enhanced Financial Wellness AI Chatbot

A comprehensive AI-powered financial analysis system that provides intelligent insights into your spending patterns, budget tracking, and financial recommendations using advanced MCP (Model Context Protocol) integration and Google Gemini AI.

![Financial Analysis Demo](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python Version](https://img.shields.io/badge/Python-3.8+-blue)
![AI Integration](https://img.shields.io/badge/AI-Gemini%20Pro-orange)

## 🎯 **Project Overview**

This project has evolved from a basic financial chatbot to a **comprehensive AI-powered financial analysis platform** with enhanced MCP integration. The system processes real transaction data, provides intelligent insights, and generates professional visualizations.

### **Key Features**
- 🤖 **AI-Powered Analysis** - Google Gemini Pro integration for natural language processing
- 📊 **7 Comprehensive Tools** - Complete financial analysis toolkit
- 📈 **Professional Charts** - 4 types of financial visualizations
- 💾 **Real Transaction Data** - 95 realistic financial transactions
- 🎯 **Smart Recommendations** - AI-powered financial advice
- 📱 **Interactive Interface** - Natural language chatbot interface

---

## 🏗️ **Project Structure**

```
mcp_ai_chatbot/
├── 📁 **CORE SYSTEM** (Current - Enhanced)
│   ├── financial_mcp_server.py          # 🆕 Enhanced MCP server (29KB, 659 lines)
│   ├── enhanced_financial_client.py     # 🆕 AI-powered client (19KB, 402 lines)
│   ├── daily_transactions.csv           # 🆕 Transaction dataset (8KB, 95 transactions)
│   └── demo_financial_analysis.py       # 🆕 Comprehensive demo (10KB, 257 lines)
│
├── 📁 **TESTING & DEBUG** (Current - New)
│   ├── test_chart_generation.py         # 🆕 Chart testing (2.3KB)
│   ├── debug_chart_generation.py        # 🆕 Debug script (2.7KB)
│   └── show_charts.py                   # 🆕 Chart status (3.1KB)
│
├── 📁 **DOCUMENTATION** (Current - Enhanced)
│   ├── ENHANCED_README.md               # 🆕 Comprehensive guide (13KB)
│   ├── IMPLEMENTATION_SUMMARY.md        # 🆕 Implementation details (10KB)
│   └── QUICK_START.md                   # 🆕 Quick start guide (5KB)
│
├── 📁 **GENERATED ASSETS** (Current - Auto-generated)
│   └── charts/                          # 🆕 Financial charts
│       ├── category_breakdown.png       # 🆕 Spending categories (180KB)
│       ├── spending_trend.png           # 🆕 Daily trends (202KB)
│       ├── budget_vs_actual.png         # 🆕 Budget comparison (145KB)
│       └── merchant_analysis.png        # 🆕 Merchant analysis (113KB)
│
├── 📁 **CONFIGURATION** (Current - Shared)
│   ├── config.json                      # ✅ API configuration (138B)
│   ├── requirements.txt                 # ✅ Dependencies (337B)
│   └── venv/                           # ✅ Virtual environment
│
└── 📁 **LEGACY SYSTEM** (Old - Deprecated)
    ├── api_server.py                    # ❌ Old FastAPI server (16KB)
    ├── client/                          # ❌ Old client directory
    ├── financial_data.json              # ❌ Old sample data (5.4KB)
    └── [other deprecated files...]      # ❌ Old documentation & tests
```

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8 or higher
- Google Gemini API key
- Required Python packages (see `requirements.txt`)

### **Installation**

1. **Clone the repository**
```bash
git clone <repository-url>
cd mcp_ai_chatbot
```

2. **Install dependencies**
```bash
pip3 install -r requirements.txt
```

3. **Configure API key**
```bash
# Edit config.json with your Google Gemini API key
{
  "GOOGLE_API_KEY": "your-gemini-api-key-here"
}
```

### **Running the System**

#### **Option 1: Interactive AI Chatbot** (Recommended)
```bash
python3 enhanced_financial_client.py
```

**Example Interaction:**
```
🤖 Enhanced Financial Wellness AI Chatbot
Loaded 95 transactions from daily_transactions.csv

Ask me anything about your finances! Examples:
• 'How much did I spend this month?'
• 'Show me my spending by category'
• 'Am I over budget in any categories?'
• 'Give me spending recommendations'
• 'What are my top merchants?'
• 'Generate a spending trend chart'
• Type 'quit' to exit

You: Show me my spending by category

Assistant: Analyzing your financial data...
I found 95 transactions totaling $14,515.99.

**Top 5 Transactions:**
1. Employer Inc - $2500.00 (Income) - 2024-01-01
2. Property Management - $1200.00 (Rent) - 2024-01-08
3. Internal Transfer - $500.00 (Savings) - 2024-01-05
4. Micro Center - $500.00 (Shopping) - 2024-01-28
5. Best Buy - $450.00 (Shopping) - 2024-01-24
```

#### **Option 2: Comprehensive Demo**
```bash
python3 demo_financial_analysis.py
```

#### **Option 3: Direct MCP Server Usage**
```python
from financial_mcp_server import FinancialMCPServer

server = FinancialMCPServer()
result = server.get_spending_analysis()
print(result)
```

---

## 🔧 **System Architecture**

### **Core Components**

#### **1. Financial MCP Server** (`financial_mcp_server.py`)
- **Size**: 29KB (659 lines)
- **Purpose**: Core financial analysis engine
- **Features**:
  - 7 comprehensive analysis tools
  - Real-time transaction processing
  - Professional chart generation
  - Budget tracking and analysis
  - Advanced filtering capabilities

#### **2. Enhanced Financial Client** (`enhanced_financial_client.py`)
- **Size**: 19KB (402 lines)
- **Purpose**: AI-powered interactive interface
- **Features**:
  - Natural language query processing
  - Google Gemini AI integration
  - Smart date extraction and filtering
  - Conversation memory
  - Intelligent response formatting

#### **3. Transaction Dataset** (`daily_transactions.csv`)
- **Size**: 8KB (95 transactions)
- **Features**:
  - 95 realistic financial transactions
  - 10 spending categories
  - 50+ unique merchants
  - 31 days of transaction data
  - Multiple transaction types

### **Available Analysis Tools**

| Tool | Description | Example Query |
|------|-------------|---------------|
| `get_transactions()` | Filter and retrieve transactions | "Show me all grocery transactions" |
| `get_spending_analysis()` | Comprehensive spending breakdown | "How much did I spend this month?" |
| `get_budget_analysis()` | Budget vs actual comparison | "Am I over budget?" |
| `get_spending_recommendations()` | AI-powered financial advice | "Give me spending recommendations" |
| `get_merchant_analysis()` | Merchant spending patterns | "What are my top merchants?" |
| `get_trend_analysis()` | Time-based trend analysis | "Show me spending trends" |
| `generate_chart()` | Professional chart generation | "Generate a spending trend chart" |

### **Chart Generation Types**

1. **Category Breakdown** - Pie chart of spending categories
2. **Spending Trend** - Line chart of daily spending trends
3. **Budget vs Actual** - Bar chart comparing budget to actual spending
4. **Merchant Analysis** - Bar chart of top merchants by spending

---

## 📊 **Data Processing Pipeline**

```
CSV Data → Pandas DataFrame → Filtering/Analysis → JSON Response → Chart Generation → File Storage
```

### **Natural Language Processing Flow**
```
User Query → Query Analysis → Tool Selection → MCP Tool Call → Response Formatting → AI Enhancement → Final Response
```

### **Chart Generation Process**
```
Chart Request → Data Filtering → Visualization Creation → File Saving → Path Return
```

---

## 🎨 **Generated Visualizations**

The system automatically generates 4 types of professional financial charts:

### **1. Category Breakdown Chart**
- **File**: `charts/category_breakdown.png`
- **Type**: Pie chart
- **Purpose**: Shows spending distribution across categories

### **2. Spending Trend Chart**
- **File**: `charts/spending_trend.png`
- **Type**: Line chart with markers
- **Purpose**: Displays daily spending patterns over time
- **Features**: 
  - Date range: January 1 - February 1, 2024
  - Y-axis: Amount ($) from 0 to 1400
  - Shows spending volatility and trends

### **3. Budget vs Actual Chart**
- **File**: `charts/budget_vs_actual.png`
- **Type**: Bar chart
- **Purpose**: Compares budgeted vs actual spending

### **4. Merchant Analysis Chart**
- **File**: `charts/merchant_analysis.png`
- **Type**: Bar chart
- **Purpose**: Shows top merchants by spending amount

---

## 🔍 **Testing & Debugging**

### **Testing Tools**
```bash
# Test chart generation
python3 test_chart_generation.py

# Debug chart issues
python3 debug_chart_generation.py

# Show chart status
python3 show_charts.py
```

### **Common Issues & Solutions**

1. **ModuleNotFoundError: No module named 'plotly'**
   ```bash
   pip3 install plotly
   ```

2. **API Key Issues**
   - Ensure `config.json` contains valid Google Gemini API key
   - Check API key permissions and quotas

3. **Chart Generation Failures**
   - Verify `charts/` directory exists
   - Check write permissions
   - Ensure matplotlib/seaborn are installed

---

## 📈 **System Evolution**

### **Version History**
- **July 29, 2024**: Original basic system
- **July 31, 2024**: Major enhancement with MCP server and AI client
- **August 1, 2024**: Chart generation fixes and testing tools

### **Key Improvements**
- **Data Processing**: CSV dataset vs JSON sample data
- **Analysis Tools**: 7 comprehensive tools vs basic operations
- **User Interface**: Natural language processing vs structured queries
- **Visualization**: 4 professional chart types vs basic graphs
- **Documentation**: Comprehensive guides vs basic setup instructions

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### **Development Setup**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip3 install -r requirements.txt

# Run tests
python3 test_chart_generation.py
```

---

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 **Acknowledgments**

- **Google Gemini AI** - For natural language processing capabilities
- **MCP Protocol** - For standardized tool interface
- **Pandas & Matplotlib** - For data processing and visualization
- **FastAPI & Uvicorn** - For web server capabilities

---

## 📞 **Support**

For questions, issues, or contributions:
- Create an issue on GitHub
- Check the documentation in `ENHANCED_README.md`
- Review `IMPLEMENTATION_SUMMARY.md` for technical details

---

**🎉 Ready to transform your financial analysis with AI-powered insights!** 
