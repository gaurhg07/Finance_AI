import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="FinanceTracker AI",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("💰 FinanceTracker AI")
st.sidebar.write("Personal Finance Analytics Dashboard")

# -----------------------------------
# MAIN TITLE
# -----------------------------------

st.title("💰 FinanceTracker AI")
st.write("Upload any finance CSV file and analyze expenses.")

# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# -----------------------------------
# PROCESS FILE
# -----------------------------------

if uploaded_file is not None:

    try:

        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Show available columns
        st.subheader("📌 Available Columns")

        st.write(df.columns.tolist())

        # -----------------------------------
        # COLUMN SELECTION
        # -----------------------------------

        st.subheader("🛠 Select Columns")

        columns = df.columns.tolist()

        date_column = st.selectbox(
            "Select Date Column",
            columns,
            key="date"
        )

        category_column = st.selectbox(
            "Select Category Column",
            columns,
            key="category"
        )

        amount_column = st.selectbox(
            "Select Amount Column",
            columns,
            key="amount"
        )

        # -----------------------------------
        # CREATE CLEAN DATAFRAME
        # -----------------------------------

        clean_df = pd.DataFrame()

        clean_df["Date"] = df[date_column]

        clean_df["Category"] = df[category_column]

        clean_df["Amount"] = df[amount_column]

        # -----------------------------------
        # DATA CLEANING
        # -----------------------------------

        clean_df["Date"] = pd.to_datetime(
            clean_df["Date"],
            errors="coerce"
        )

        clean_df["Amount"] = pd.to_numeric(
            clean_df["Amount"],
            errors="coerce"
        )

        clean_df.dropna(inplace=True)

        # -----------------------------------
        # DATA PREVIEW
        # -----------------------------------

        st.subheader("📄 Dataset Preview")

        st.dataframe(clean_df.head())

        # -----------------------------------
        # TOTAL EXPENSES
        # -----------------------------------

        total_expense = clean_df["Amount"].sum()

        st.subheader("💸 Total Expenses")

        st.metric(
            label="Total Spending",
            value=f"₹{total_expense:,.2f}"
        )

        # -----------------------------------
        # CATEGORY ANALYSIS
        # -----------------------------------

        st.subheader("📊 Category-wise Expenses")

        category_expense = (
            clean_df.groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.dataframe(category_expense)

        # -----------------------------------
        # PIE CHART
        # -----------------------------------

        st.subheader("🥧 Expense Distribution")

        fig1, ax1 = plt.subplots(figsize=(8, 8))

        category_expense.plot.pie(
            autopct="%1.1f%%",
            ax=ax1
        )

        ax1.set_ylabel("")

        st.pyplot(fig1)

        # -----------------------------------
        # BAR CHART
        # -----------------------------------

        st.subheader("📈 Expense Comparison")

        fig2, ax2 = plt.subplots(figsize=(10, 5))

        sns.barplot(
            x=category_expense.index,
            y=category_expense.values,
            ax=ax2
        )

        plt.xticks(rotation=45)

        ax2.set_xlabel("Category")

        ax2.set_ylabel("Amount")

        st.pyplot(fig2)

        # -----------------------------------
        # MONTHLY ANALYSIS
        # -----------------------------------

        st.subheader("📅 Monthly Expenses")

        clean_df["Month"] = (
            clean_df["Date"]
            .dt.month_name()
        )

        monthly_expense = (
            clean_df.groupby("Month")["Amount"]
            .sum()
        )

        st.line_chart(monthly_expense)

        # -----------------------------------
        # DAILY TREND
        # -----------------------------------

        st.subheader("📉 Daily Spending Trend")

        daily_expense = (
            clean_df.groupby("Date")["Amount"]
            .sum()
        )

        st.line_chart(daily_expense)

        # -----------------------------------
        # SAVINGS CALCULATOR
        # -----------------------------------

        st.subheader("💰 Savings Calculator")

        income = st.number_input(
            "Enter Monthly Income (₹)",
            min_value=0.0,
            value=50000.0
        )

        savings = income - total_expense

        st.metric(
            label="Estimated Savings",
            value=f"₹{savings:,.2f}"
        )

        # -----------------------------------
        # SAVINGS MESSAGE
        # -----------------------------------

        if savings > 0:

            st.success(
                "Great! You are saving money."
            )

        elif savings == 0:

            st.warning(
                "Your expenses equal your income."
            )

        else:

            st.error(
                "Warning! Your expenses exceed income."
            )

        # -----------------------------------
        # TOP CATEGORY
        # -----------------------------------

        top_category = category_expense.idxmax()

        top_amount = category_expense.max()

        st.subheader("🏆 Highest Spending Category")

        st.info(
            f"You spent the most on "
            f"{top_category} "
            f"(₹{top_amount:,.2f})"
        )

        # -----------------------------------
        # SUMMARY
        # -----------------------------------

        st.subheader("📋 Statistical Summary")

        st.write(clean_df.describe())

        # -----------------------------------
        # DOWNLOAD BUTTON
        # -----------------------------------

        st.subheader("⬇ Download Processed Dataset")

        csv = clean_df.to_csv(index=False)

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="clean_finance_data.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error(f"Error: {e}")

else:

    st.info(
        "Please upload a CSV file to begin analysis."
    )
