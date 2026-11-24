# M-Pesa Business Tracker 📊

A client-ready, interactive Streamlit dashboard that visualizes M-Pesa business transactions. It tracks **daily revenue**, **top transaction types**, and **weekly sales patterns** — designed for a non-technical business owner who wants a clear, at-a-glance view of their mobile money performance.

---

## ⚠️ Disclaimer

> **The data used in this project is entirely synthetic and randomly generated for demonstration purposes only.** It does **not** reflect the true status, volumes, values, or trends of the mobile money industry in Kenya or anywhere else. Names, transaction codes, amounts, counterparties, and dates are fictional and were produced by a script (`generate_data.py`) solely to illustrate dashboard functionality. No real customer, business, or M-Pesa statement data is included. Do not use this dataset for financial, regulatory, research, or decision-making purposes.

---

## ✨ Features

- **Plain-language UI** built for non-technical users.
- **Two interactive filters** in the sidebar:
  - Transaction Type (Buy Goods, Pay Bill, Send Money, Receive Money, Withdraw)
  - Date Range (defaults to the last 30 days)
- **Three core charts**:
  1. **Daily Revenue Trend** – line chart of revenue over time.
  2. **Top Transaction Types** – donut chart of revenue share by type.
  3. **Weekly Sales Pattern** – bar chart by day of week, **including Sundays**.
- **KPI cards** – Total Revenue, Total Transactions, Average Transaction Value.
- **Expandable transaction table** for users who want to drill into raw records.

---

## 📁 Project Structure

```text
mpesa-tracker/
├── mpesa_business_tracker.py                  # The Streamlit dashboard
├── generate_data.py        # Script that creates the synthetic dataset
├── mpesa_statement.csv     # Generated sample data (do not edit manually)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/mpesa-tracker.git
cd mpesa-tracker
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate the sample data

```bash
python generate_data.py
```

This creates `mpesa_statement.csv` with 2,500 synthetic transactions spanning 2025-01-01 to 2025-12-31.

### 5. Launch the dashboard

```bash
streamlit run app.py
```

Open the URL shown in your terminal.
