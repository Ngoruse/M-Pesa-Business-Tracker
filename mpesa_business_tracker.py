import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="M-Pesa Business Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading ---
@st.cache_data
def load_data():
    df = pd.read_csv("mpesa_statement.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    # Ensure Sunday transactions are handled correctly by pandas
    df["DayOfWeek"] = df["Date"].dt.day_name()
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file not found. Please check your source or file spelling.")
    st.stop()

# --- Sidebar Filters (Designed for Non-Technical Users) ---
st.sidebar.header("🔍 Filter Your View")
st.sidebar.markdown("Use these options to focus on specific transactions.")

# Filter 1: Transaction Type
tx_types = ["All Types"] + sorted(df["Transaction Type"].unique().tolist())
selected_type = st.sidebar.selectbox("Transaction Type", tx_types)

# Filter 2: Date Range (Focus on recent performance)
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

# Default to the last 30 days of available data for a "recent view"
default_start = (df["Date"].max() - pd.Timedelta(days=30)).date()
default_end = max_date

date_range = st.sidebar.date_input(
    "Date Range",
    value=(default_start, default_end),
    min_value=min_date,
    max_value=max_date,
    help="Select the period you want to analyze."
)

# Apply Filters
filtered_df = df.copy()
if selected_type != "All Types":
    filtered_df = filtered_df[filtered_df["Transaction Type"] == selected_type]

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date) & 
        (filtered_df["Date"].dt.date <= end_date)
    ]

# --- Main Dashboard Area ---
st.title("📊 M-Pesa Business Tracker")
st.caption("A clear view of your daily revenue, top transaction types, and weekly trends. Last updated: Today")

# --- KPI Row (Big numbers for quick health check) ---
total_revenue = filtered_df["Amount (KES)"].sum()
total_transactions = len(filtered_df)
avg_transaction = filtered_df["Amount (KES)"].mean() if total_transactions > 0 else 0

k1, k2, k3 = st.columns(3)
k1.metric("Total Revenue (KES)", f"{total_revenue:,.0f}", help="Total money received in the selected period.")
k2.metric("Total Transactions", f"{total_transactions:,}", help="Number of transactions processed.")
k3.metric("Avg Transaction (KES)", f"{avg_transaction:,.0f}", help="Average amount per transaction.")

st.divider()

# --- Charts Section ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Daily Revenue Trend")
    st.markdown("This chart shows how your daily sales are moving. Look for peaks (good days) and dips (slow days).")
    
    # Prepare daily data
    daily_revenue = filtered_df.groupby(filtered_df["Date"].dt.date)["Amount (KES)"].sum().reset_index()
    daily_revenue.columns = ["Date", "Revenue"]
    
    if not daily_revenue.empty:
        fig_trend = px.line(
            daily_revenue, 
            x="Date", 
            y="Revenue",
            markers=True,
            labels={"Revenue": "Revenue (KES)", "Date": "Date"}
        )
        fig_trend.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title=None,
            yaxis_title="Revenue (KES)"
        )
        fig_trend.update_traces(line_color="#2E8B57", marker=dict(size=6))
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No transactions found for the selected filters.")

with col2:
    st.subheader("💰 Top Transaction Types")
    st.markdown("Which services are generating the most money for you?")
    
    type_revenue = filtered_df.groupby("Transaction Type")["Amount (KES)"].sum().reset_index()
    
    if not type_revenue.empty:
        fig_pie = px.pie(
            type_revenue, 
            values="Amount (KES)", 
            names="Transaction Type",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig_pie.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No data available.")

# --- Weekly Trend Chart (Full Width) ---
st.subheader("📅 Weekly Sales Pattern")
st.markdown("See which days of the week are your busiest. This helps with staffing and planning.")

# Prepare weekly data
weekly_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekly_revenue = filtered_df.groupby("DayOfWeek")["Amount (KES)"].sum().reindex(weekly_order).reset_index()

if not weekly_revenue.empty and weekly_revenue["Amount (KES)"].sum() > 0:
    fig_bar = px.bar(
        weekly_revenue,
        x="DayOfWeek",
        y="Amount (KES)",
        labels={"Amount (KES)": "Total Revenue (KES)", "DayOfWeek": "Day of the Week"},
        color="Amount (KES)",
        color_continuous_scale="Greens"
    )
    fig_bar.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title=None,
        yaxis_title="Revenue (KES)",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("No weekly data available for the selected filters.")

# --- Footer / Data Table (Optional for power users) ---
with st.expander("🔎 View Detailed Transaction List"):
    st.markdown("Click to see the raw data for the selected period.")
    st.dataframe(
        filtered_df[["Date", "Transaction Code", "Transaction Type", "Counterparty", "Amount (KES)"]],
        use_container_width=True,
        hide_index=True
    )