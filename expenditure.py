import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json
import os
from collections import defaultdict, Counter
import math

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="Expense Manager Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------
# Premium CSS Styling
# ----------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');
        
        * {
            font-family: 'DM Sans', sans-serif;
        }
        
        /* Sophisticated Dark Theme Background */
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 50%, #16213e 100%);
            min-height: 100vh;
        }
        
        /* Animated Grid Background */
        .main::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(0deg, transparent 24%, rgba(255, 255, 255, 0.02) 25%, rgba(255, 255, 255, 0.02) 26%, transparent 27%, transparent 74%, rgba(255, 255, 255, 0.02) 75%, rgba(255, 255, 255, 0.02) 76%, transparent 77%, transparent),
                linear-gradient(90deg, transparent 24%, rgba(255, 255, 255, 0.02) 25%, rgba(255, 255, 255, 0.02) 26%, transparent 27%, transparent 74%, rgba(255, 255, 255, 0.02) 75%, rgba(255, 255, 255, 0.02) 76%, transparent 77%, transparent);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: -1;
        }
        
        /* Premium Card */
        .expense-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 24px;
            margin: 14px 0;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .expense-card::before {
            content: '';
            position: absolute;
            top: -1px;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
        }
        
        .expense-card:hover {
            transform: translateY(-8px);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.3);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.08));
        }
        
        /* Category Colors */
        .category-food { border-left: 4px solid #ff6b6b; }
        .category-transport { border-left: 4px solid #4ecdc4; }
        .category-entertainment { border-left: 4px solid #a29bfe; }
        .category-utilities { border-left: 4px solid #fab1a0; }
        .category-health { border-left: 4px solid #81ecec; }
        .category-shopping { border-left: 4px solid #fdcb6e; }
        .category-education { border-left: 4px solid #55efc4; }
        .category-savings { border-left: 4px solid #74b9ff; }
        .category-other { border-left: 4px solid #b8bfff; }
        
        /* Amount Display */
        .amount-display {
            font-family: 'Syne', sans-serif;
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Header */
        .header-section {
            margin-bottom: 40px;
            animation: fadeInDown 0.8s ease-out;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .main-title {
            font-family: 'Syne', sans-serif;
            font-size: 56px;
            font-weight: 800;
            color: #fff;
            margin-bottom: 8px;
            letter-spacing: -1.5px;
        }
        
        .subtitle-text {
            font-size: 16px;
            color: rgba(255, 255, 255, 0.6);
            font-weight: 400;
            letter-spacing: 0.5px;
        }
        
        /* Stat Cards */
        .stat-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 28px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
            position: relative;
            overflow: hidden;
            text-align: center;
        }
        
        .stat-card::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.08), transparent 70%);
            border-radius: 50%;
            transform: translate(50%, -50%);
        }
        
        .stat-card:hover {
            transform: translateY(-8px);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        .stat-number {
            font-family: 'Syne', sans-serif;
            font-size: 42px;
            font-weight: 700;
            color: #00d4ff;
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
        }
        
        .stat-label {
            font-size: 13px;
            color: rgba(255, 255, 255, 0.6);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            position: relative;
            z-index: 1;
        }
        
        /* Input Section */
        .input-section {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 32px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            animation: slideUp 0.8s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .section-title {
            font-family: 'Syne', sans-serif;
            font-size: 26px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 28px;
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: -0.5px;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select,
        .stDateInput > div > div > input {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            color: #fff !important;
            font-weight: 500;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input::placeholder,
        .stNumberInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.4) !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stDateInput > div > div > input:focus {
            border-color: #00d4ff !important;
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1) !important;
            background: rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Buttons */
        .stButton > button {
            font-weight: 700;
            border-radius: 10px;
            padding: 12px 24px !important;
            transition: all 0.3s ease !important;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-size: 13px !important;
            border: 1px solid rgba(0, 212, 255, 0.3) !important;
            background: linear-gradient(135deg, #00d4ff, #0099ff) !important;
            color: #0f172a !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(0, 212, 255, 0.3) !important;
        }
        
        /* Category Badge */
        .category-badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.1);
            color: #00d4ff;
            border: 1px solid rgba(0, 212, 255, 0.3);
        }
        
        /* Date Badge */
        .date-badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.08);
            color: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }
        
        /* Amount Badge */
        .amount-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 700;
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(0, 153, 255, 0.2));
            color: #00d4ff;
            border: 1px solid rgba(0, 212, 255, 0.3);
            font-family: 'Syne', sans-serif;
        }
        
        /* Divider */
        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            margin: 30px 0;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.8), rgba(26, 31, 58, 0.8)) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        
        /* Chart Container */
        .chart-container {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 28px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            margin: 20px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 80px 20px;
            animation: fadeIn 0.8s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .empty-icon {
            font-size: 72px;
            margin-bottom: 20px;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        /* Text Colors */
        .text-primary { color: #fff; }
        .text-secondary { color: rgba(255, 255, 255, 0.7); }
        .text-accent { color: #00d4ff; }
        
        /* Expense List Meta */
        .expense-meta {
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
            margin-top: 12px;
        }
        
        .expense-name {
            font-size: 18px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 10px;
            letter-spacing: -0.3px;
        }
        
        /* Info Box */
        .info-box {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.08), rgba(0, 153, 255, 0.08));
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 10px;
            padding: 12px 16px;
            font-size: 12px;
            color: #00d4ff;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# Storage Configuration
# ----------------------------------------
STORAGE_DIR = os.path.expanduser("~/.expense_manager_data")
STORAGE_FILE = os.path.join(STORAGE_DIR, "expenses.json")

os.makedirs(STORAGE_DIR, exist_ok=True)

# ----------------------------------------
# Initialize Session State
# ----------------------------------------
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# ----------------------------------------
# Storage Functions
# ----------------------------------------
def loadExpensesFromStorage():
    """Load expenses from persistent JSON storage"""
    try:
        if os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, 'r') as f:
                st.session_state.expenses = json.load(f)
                return True
        return False
    except Exception as e:
        st.error(f"Error loading expenses: {str(e)}")
        return False

def saveExpensesToStorage():
    """Save expenses to persistent JSON storage"""
    try:
        # Custom JSON encoder to handle date objects
        class DateTimeEncoder(json.JSONEncoder):
            def default(self, obj):
                if hasattr(obj, 'isoformat'):
                    return obj.isoformat()
                return super().default(obj)
        
        # Ensure all dates are strings before saving
        clean_expenses = []
        for expense in st.session_state.expenses:
            clean_expense = expense.copy()
            if isinstance(clean_expense.get('date'), str):
                pass  # Already a string
            else:
                clean_expense['date'] = str(clean_expense.get('date', ''))
            clean_expenses.append(clean_expense)
        
        with open(STORAGE_FILE, 'w') as f:
            json.dump(clean_expenses, f, indent=2, cls=DateTimeEncoder)
        return True
    except Exception as e:
        st.error(f"Error saving expenses: {str(e)}")
        return False

def addExpense(description, amount, category, date, notes=""):
    """Add a new expense"""
    if not description.strip():
        return False, "Description cannot be empty"
    
    try:
        amount_float = float(amount)
        if amount_float <= 0:
            return False, "Amount must be greater than 0"
    except ValueError:
        return False, "Invalid amount format"
    
    # Convert date to string if it's a date object
    if hasattr(date, 'strftime'):
        date_str = date.strftime("%Y-%m-%d")
    else:
        date_str = str(date)
    
    expense = {
        'id': len(st.session_state.expenses) + 1,
        'description': description,
        'amount': amount_float,
        'category': category,
        'date': date_str,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'notes': notes
    }
    
    st.session_state.expenses.append(expense)
    
    if saveExpensesToStorage():
        return True, f"Expense added: ₹{amount_float:.2f} ✓"
    else:
        return False, "Expense added but could not save to storage"

def deleteExpense(expense_id):
    """Delete an expense by ID"""
    st.session_state.expenses = [e for e in st.session_state.expenses if e['id'] != expense_id]
    saveExpensesToStorage()

def getCategoryEmoji(category):
    """Get emoji for category"""
    emojis = {
        'Food & Dining': '🍔',
        'Transport': '🚗',
        'Entertainment': '🎬',
        'Utilities': '💡',
        'Health': '🏥',
        'Shopping': '🛍️',
        'Education': '📚',
        'Savings': '💳',
        'Other': '📌'
    }
    return emojis.get(category, '📌')

def getCategoryColor(category):
    """Get color class for category"""
    colors = {
        'Food & Dining': 'category-food',
        'Transport': 'category-transport',
        'Entertainment': 'category-entertainment',
        'Utilities': 'category-utilities',
        'Health': 'category-health',
        'Shopping': 'category-shopping',
        'Education': 'category-education',
        'Savings': 'category-savings',
        'Other': 'category-other'
    }
    return colors.get(category, 'category-other')

def exportExpensesToCSV():
    """Export expenses to CSV"""
    if not st.session_state.expenses:
        return None
    
    df = pd.DataFrame(st.session_state.expenses)
    return df.to_csv(index=False).encode('utf-8')

# Load expenses when app starts
if not st.session_state.expenses:
    loadExpensesFromStorage()

# ----------------------------------------
# Sidebar Settings
# ----------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings & Export")
    st.markdown("---")
    
    st.markdown(f"""
        <div class='info-box'>
        💾 Data saved locally
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save", use_container_width=True):
            if saveExpensesToStorage():
                st.success("Saved! ✓")
            else:
                st.error("Save failed")
    
    with col2:
        if st.button("🔄 Reload", use_container_width=True):
            if loadExpensesFromStorage():
                st.success("Reloaded!")
                st.rerun()
            else:
                st.info("No data found")
    
    st.markdown("---")
    
    # Date Range Filter
    st.markdown("#### 📅 Filter by Date Range")
    date_range = st.selectbox("Select Range:", ["All Time", "This Month", "Last 30 Days", "This Week", "Custom"])
    
    if date_range == "Custom":
        start_date = st.date_input("From:", value=datetime(2024, 1, 1))
        end_date = st.date_input("To:", value=datetime.now())
    
    st.markdown("---")
    
    if st.session_state.expenses:
        csv_data = exportExpensesToCSV()
        st.download_button(
            label="📊 Export as CSV",
            data=csv_data,
            file_name=f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Danger Zone
    st.markdown("#### ⚠️ Danger Zone")
    if st.button("🗑️ Clear All", use_container_width=True):
        if st.button("⚠️ Confirm?", use_container_width=True, key="confirm_delete"):
            st.session_state.expenses = []
            saveExpensesToStorage()
            st.success("Cleared! 🧹")
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
        <div style='font-size: 11px; color: #00d4ff; text-align: center;'>
        💰 Expense Manager Pro<br>
        <strong>v1.0</strong><br>
        <br>
        ✅ Zero Tracking<br>
        🔐 100% Private<br>
        📱 Always Available
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------
# Main Header
# ----------------------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
        <div class='header-section'>
            <div class='main-title'>💰 Expense Manager</div>
            <div class='subtitle-text'>Track spending, manage budgets, achieve financial goals</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style='text-align: right; padding-top: 20px;'>
            <div style='font-size: 14px; color: rgba(255,255,255,0.8);'>
                {datetime.now().strftime('%a, %b %d')}
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------
# Statistics Section
# ----------------------------------------
if st.session_state.expenses:
    # Filter expenses by date range
    filtered_expenses = st.session_state.expenses.copy()
    
    if date_range == "This Month":
        today = datetime.now()
        start = today.replace(day=1)
        end = today
        filtered_expenses = [e for e in filtered_expenses if start.strftime("%Y-%m") <= e['date'][:7] <= end.strftime("%Y-%m")]
    elif date_range == "Last 30 Days":
        cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        filtered_expenses = [e for e in filtered_expenses if e['date'] >= cutoff]
    elif date_range == "This Week":
        cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        filtered_expenses = [e for e in filtered_expenses if e['date'] >= cutoff]
    elif date_range == "Custom":
        filtered_expenses = [e for e in filtered_expenses if start_date.strftime("%Y-%m-%d") <= e['date'] <= end_date.strftime("%Y-%m-%d")]
    
    total_spent = sum(e['amount'] for e in filtered_expenses)
    avg_spent = total_spent / len(filtered_expenses) if filtered_expenses else 0
    max_expense = max((e['amount'] for e in filtered_expenses), default=0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>₹{total_spent:.0f}</div>
                <div class='stat-label'>Total Spent</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>{len(filtered_expenses)}</div>
                <div class='stat-label'>Transactions</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>₹{avg_spent:.0f}</div>
                <div class='stat-label'>Average</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>₹{max_expense:.0f}</div>
                <div class='stat-label'>Largest</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("📊 Spending by Category")
        category_spending = defaultdict(float)
        for e in filtered_expenses:
            category_spending[e['category']] += e['amount']
        
        if category_spending:
            df_category = pd.DataFrame({
                'Category': list(category_spending.keys()),
                'Amount': list(category_spending.values())
            }).sort_values('Amount', ascending=False)
            st.bar_chart(df_category.set_index('Category'))
        else:
            st.info("No expenses in this period")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("📈 Trend Over Time")
        daily_spending = defaultdict(float)
        for e in filtered_expenses:
            daily_spending[e['date']] += e['amount']
        
        if daily_spending:
            df_daily = pd.DataFrame({
                'Date': sorted(daily_spending.keys()),
                'Amount': [daily_spending[d] for d in sorted(daily_spending.keys())]
            })
            st.line_chart(df_daily.set_index('Date'))
        else:
            st.info("No expenses in this period")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")

# ----------------------------------------
# Add Expense Section
# ----------------------------------------
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>➕ Add New Expense</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    description = st.text_input("📝 Description", placeholder="What did you spend on?")

with col2:
    amount = st.number_input("💵 Amount (₹)", min_value=0.0, step=1.0, placeholder="0.00")

with col3:
    category = st.selectbox("🏷️ Category", [
        'Food & Dining', 'Transport', 'Entertainment', 'Utilities',
        'Health', 'Shopping', 'Education', 'Savings', 'Other'
    ])

with col4:
    expense_date = st.date_input("📅 Date", value=datetime.now())

col1, col2 = st.columns([3, 1])

with col1:
    notes = st.text_input("📌 Notes (Optional)", placeholder="Add any additional details...")

with col2:
    if st.button("✨ Add Expense", use_container_width=True, key="add_expense_btn"):
        success, message = addExpense(description, amount, category, expense_date, notes)
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------
# Display Expenses Section
# ----------------------------------------
if st.session_state.expenses:
    st.markdown("<div class='section-title'>📋 Expense History</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([e['category'] for e in st.session_state.expenses])))
    with col2:
        search_term = st.text_input("🔍 Search", placeholder="Find expense...")
    
    # Filter
    filtered_list = st.session_state.expenses.copy()
    
    if filter_category != "All":
        filtered_list = [e for e in filtered_list if e['category'] == filter_category]
    
    if search_term:
        filtered_list = [e for e in filtered_list if search_term.lower() in e['description'].lower()]
    
    # Sort by date descending
    filtered_list.sort(key=lambda x: x['date'], reverse=True)
    
    if filtered_list:
        for expense in filtered_list:
            emoji = getCategoryEmoji(expense['category'])
            color_class = getCategoryColor(expense['category'])
            
            col1, col2, col3 = st.columns([4, 0.8, 0.2])
            
            with col1:
                st.markdown(f"""
                    <div class='expense-card {color_class}'>
                        <div class='expense-name'>{emoji} {expense['description']}</div>
                        <div class='expense-meta'>
                            <span class='category-badge'>{expense['category']}</span>
                            <span class='date-badge'>📅 {expense['date']}</span>
                            <span class='amount-badge'>₹{expense['amount']:.2f}</span>
                        </div>
                        {f"<div style='margin-top: 12px; color: rgba(255,255,255,0.6); font-size: 13px;'>📌 {expense['notes']}</div>" if expense.get('notes') else ""}
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.write("")
            
            with col3:
                if st.button("🗑", key=f"delete_{expense['id']}", help="Delete"):
                    deleteExpense(expense['id'])
                    st.rerun()
    else:
        st.info("🎯 No expenses match your filters")

else:
    st.markdown("""
        <div class='empty-state'>
            <div class='empty-icon'>💸</div>
            <h2 style='color: #fff; font-weight: 700;'>No Expenses Yet</h2>
            <p style='color: rgba(255, 255, 255, 0.8); font-size: 16px;'>Start tracking your spending above! 📊</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------
# Footer
# ----------------------------------------
st.markdown("""
    <div style='text-align: center; color: rgba(255, 255, 255, 0.5); font-size: 12px; padding: 30px 20px;'>
        <strong>Expense Manager Pro v1.0</strong> • Built with 💙 using Streamlit<br>
        🔐 Your data stays private • 📱 Always accessible • ⚡ Lightning fast<br>
        <span style='font-size: 10px;'>© 2025 • Zero tracking overhead</span>
    </div>
""", unsafe_allow_html=True)
