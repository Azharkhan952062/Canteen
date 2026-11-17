import os
import tempfile
import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Ensure Matplotlib uses a writable temporary cache directory on Windows
os.environ.setdefault('MPLCONFIGDIR', tempfile.gettempdir())

# Page configuration
st.set_page_config(
    page_title="Canteen Food Demand & Waste Tracker",
    page_icon="🍛",
    layout="wide"
)

DATA_COLUMNS = [
    "Date",
    "Food_Item",
    "Quantity_Prepared",
    "Quantity_Sold",
    "Quantity_Remaining",
    "Selling_Price"
]

DATA_PATH = "data.csv"

def load_data(filepath_or_buffer):
    """Load data from CSV file and sanitize column headers."""
    try:
        df = pd.read_csv(filepath_or_buffer)
        df.columns = [col.strip() for col in df.columns]
        return df
    except Exception as error:
        st.error(f"Error loading data file: {error}")
        return pd.DataFrame(columns=DATA_COLUMNS)

def validate_and_clean_data(df):
    """
    Validate data structure, cast numerical fields, and calculate:
    - Quantity_Remaining = Quantity_Prepared - Quantity_Sold
    - Revenue = Quantity_Sold * Selling_Price
    """
    warnings = []
    
    if df.empty or len(df) == 0:
        return df, ["The dataset contains no records."]
    
    missing_cols = [c for c in DATA_COLUMNS if c not in df.columns]
    if missing_cols:
        warnings.append(f"Missing required column(s): {', '.join(missing_cols)}")
        return df, warnings

    cleaned_df = df.copy().dropna(how='all')

    numeric_cols = ["Quantity_Prepared", "Quantity_Sold", "Selling_Price"]
    for col in numeric_cols:
        cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce').fillna(0)

    # Derived business metrics
    cleaned_df["Quantity_Remaining"] = cleaned_df["Quantity_Prepared"] - cleaned_df["Quantity_Sold"]
    cleaned_df["Revenue"] = cleaned_df["Quantity_Sold"] * cleaned_df["Selling_Price"]

    # Integrity checks for data anomalies
    sold_exceeds_prep = cleaned_df[cleaned_df["Quantity_Sold"] > cleaned_df["Quantity_Prepared"]]
    if not sold_exceeds_prep.empty:
        warnings.append(f"{len(sold_exceeds_prep)} record(s) where Quantity Sold exceeds Quantity Prepared.")

    negatives = cleaned_df[(cleaned_df["Quantity_Prepared"] < 0) | (cleaned_df["Quantity_Sold"] < 0)]
    if not negatives.empty:
        warnings.append(f"{len(negatives)} record(s) contain negative quantity values.")

    cleaned_df["Date"] = pd.to_datetime(cleaned_df["Date"], errors='coerce')
    invalid_dates = cleaned_df[cleaned_df["Date"].isna()]
    if not invalid_dates.empty:
        warnings.append(f"{len(invalid_dates)} record(s) have unparseable dates.")

    cleaned_df = cleaned_df.sort_values(by=["Date", "Food_Item"], ascending=True)
    return cleaned_df, warnings

def append_record(date, item, prepared, sold, price, filepath=DATA_PATH):
    """Append a newly observed daily operational record to data.csv."""
    remaining = prepared - sold
    new_row = pd.DataFrame([{
        "Date": date.strftime("%Y-%m-%d"),
        "Food_Item": item.strip(),
        "Quantity_Prepared": int(prepared),
        "Quantity_Sold": int(sold),
        "Quantity_Remaining": int(remaining),
        "Selling_Price": float(price)
    }])
    
    if not os.path.exists(filepath) or os.stat(filepath).st_size == 0:
        new_row.to_csv(filepath, index=False, columns=DATA_COLUMNS)
    else:
        new_row.to_csv(filepath, mode='a', header=False, index=False, columns=DATA_COLUMNS)

# Sidebar controls
st.sidebar.title("🍱 Canteen Tracker")
st.sidebar.caption("Fieldwork Problem-Solving Tool")

source_choice = st.sidebar.radio(
    "Data Source:",
    ("Primary Dataset (data.csv)", "Upload Custom CSV"),
    index=0
)

uploaded_file = None
if source_choice == "Upload Custom CSV":
    uploaded_file = st.sidebar.file_uploader("Upload Canteen CSV", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Canteen Fieldwork Context")
st.sidebar.info(
    """
    **Field Problem:**
    The canteen sometimes prepares more Biryani than actual customer demand.
    Unsold Biryani risks spoilage, creating financial loss and food waste.
    
    **Menu Tracked:**
    - Biryani Half (₹90)
    - Biryani Full (₹150)
    - Chicken Roll (₹60)
    """
)

# Load selected dataset
if source_choice == "Primary Dataset (data.csv)":
    raw_df = load_data(DATA_PATH)
else:
    raw_df = load_data(uploaded_file) if uploaded_file is not None else pd.DataFrame(columns=DATA_COLUMNS)

df, validation_warnings = validate_and_clean_data(raw_df)

# Application Header
st.title("🍛 Canteen Food Demand & Waste Tracker")
st.markdown(
    "*A practical analytics tool helping campus canteen owners understand customer demand patterns, "
    "monitor unsold stock, and plan daily food preparation to minimize waste.*"
)

if validation_warnings:
    with st.expander("⚠️ Data Validation Notices", expanded=False):
        for warning in validation_warnings:
            st.warning(warning)

if df.empty:
    st.error("No records loaded. Please verify that `data.csv` exists or upload a valid CSV file.")
    st.stop()

# Feature tabs
tab_overview, tab_demand, tab_waste, tab_planning, tab_management = st.tabs([
    "📊 Dashboard",
    "📈 Food Demand Analysis",
    "🗑️ Food Waste Analysis",
    "🎯 Preparation Planning",
    "📁 Data Management & Entry"
])

# Tab 1: Executive Dashboard
with tab_overview:
    st.header("Executive Summary")
    st.caption("Aggregated totals and high-level performance metrics across all collected records.")
    
    total_prepared = int(df["Quantity_Prepared"].sum())
    total_sold = int(df["Quantity_Sold"].sum())
    total_remaining = int(df["Quantity_Remaining"].sum())
    total_revenue = float(df["Revenue"].sum())
    unsold_percentage = (total_remaining / total_prepared * 100) if total_prepared > 0 else 0.0

    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    col_m1.metric("Total Prepared", f"{total_prepared} units")
    col_m2.metric("Total Sold", f"{total_sold} units")
    col_m3.metric("Total Remaining", f"{total_remaining} units")
    col_m4.metric("Unsold Rate", f"{unsold_percentage:.1f}%")
    col_m5.metric("Total Revenue", f"₹{total_revenue:,.2f}")

    st.markdown("---")
    st.subheader("Item-Wise Sales & Revenue Summary")

    item_summary = df.groupby("Food_Item").agg(
        Prepared=("Quantity_Prepared", "sum"),
        Sold=("Quantity_Sold", "sum"),
        Remaining=("Quantity_Remaining", "sum"),
        Price=("Selling_Price", "first"),
        Revenue=("Revenue", "sum")
    ).reset_index()

    item_summary["Unsold %"] = (item_summary["Remaining"] / item_summary["Prepared"] * 100).round(1)

    c_bhalf, c_bfull, c_roll = st.columns(3)
    
    bh_row = item_summary[item_summary["Food_Item"] == "Biryani Half"]
    with c_bhalf:
        st.markdown("#### 🍚 Biryani Half (₹90)")
        if not bh_row.empty:
            sold_bh = int(bh_row["Sold"].values[0])
            rev_bh = float(bh_row["Revenue"].values[0])
            rem_bh = int(bh_row["Remaining"].values[0])
            st.metric("Total Sold", f"{sold_bh} portions", f"₹{rev_bh:,.2f}")
            st.write(f"- **Prepared:** {int(bh_row['Prepared'].values[0])} portions")
            st.write(f"- **Remaining:** {rem_bh} portions ({bh_row['Unsold %'].values[0]}%)")

    bf_row = item_summary[item_summary["Food_Item"] == "Biryani Full"]
    with c_bfull:
        st.markdown("#### 🍲 Biryani Full (₹150)")
        if not bf_row.empty:
            sold_bf = int(bf_row["Sold"].values[0])
            rev_bf = float(bf_row["Revenue"].values[0])
            rem_bf = int(bf_row["Remaining"].values[0])
            st.metric("Total Sold", f"{sold_bf} portions", f"₹{rev_bf:,.2f}")
            st.write(f"- **Prepared:** {int(bf_row['Prepared'].values[0])} portions")
            st.write(f"- **Remaining:** {rem_bf} portions ({bf_row['Unsold %'].values[0]}%)")

    cr_row = item_summary[item_summary["Food_Item"] == "Chicken Roll"]
    with c_roll:
        st.markdown("#### 🌯 Chicken Roll (₹60)")
        if not cr_row.empty:
            sold_cr = int(cr_row["Sold"].values[0])
            rev_cr = float(cr_row["Revenue"].values[0])
            rem_cr = int(cr_row["Remaining"].values[0])
            st.metric("Total Sold", f"{sold_cr} units", f"₹{rev_cr:,.2f}")
            st.write(f"- **Prepared:** {int(cr_row['Prepared'].values[0])} units")
            st.write(f"- **Remaining:** {rem_cr} units ({cr_row['Unsold %'].values[0]}%)")

# Tab 2: Food Demand Analysis
with tab_demand:
    st.header("Food Demand Analysis")
    st.caption("Comparison of sales volume and daily demand trends across all tracked menu items.")

    top_item_row = item_summary.sort_values(by="Sold", ascending=False).iloc[0]
    st.success(
        f"🏆 **Highest Demand Item:** **{top_item_row['Food_Item']}** with **{int(top_item_row['Sold'])}** units sold "
        f"and total revenue of **₹{float(top_item_row['Revenue']):,.2f}**."
    )

    st.markdown("---")
    st.subheader("Daily Sales Trends (Combined Comparison)")

    pivot_sold = df.pivot_table(
        index=df["Date"].dt.strftime("%Y-%m-%d"),
        columns="Food_Item",
        values="Quantity_Sold",
        aggfunc="sum"
    ).fillna(0)

    fig_sales, ax_sales = plt.subplots(figsize=(10, 4.5))
    colors = {"Biryani Half": "#d95f02", "Biryani Full": "#7570b3", "Chicken Roll": "#1b9e77"}
    
    for col in pivot_sold.columns:
        ax_sales.plot(
            pivot_sold.index, 
            pivot_sold[col], 
            marker='o', 
            linewidth=2.2, 
            label=col,
            color=colors.get(col, None)
        )

    ax_sales.set_title("Daily Units Sold Comparison", fontsize=13, fontweight='bold', pad=12)
    ax_sales.set_xlabel("Date", fontsize=10, labelpad=8)
    ax_sales.set_ylabel("Portions Sold", fontsize=10, labelpad=8)
    ax_sales.grid(True, linestyle="--", alpha=0.5)
    ax_sales.legend(title="Food Item", frameon=True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig_sales)

    st.markdown("---")
    st.subheader("Separate Demand Charts (Prepared vs. Sold per Item)")

    chart_col1, chart_col2, chart_col3 = st.columns(3)
    items_list = ["Biryani Half", "Biryani Full", "Chicken Roll"]

    for target_item, target_col in zip(items_list, [chart_col1, chart_col2, chart_col3]):
        with target_col:
            sub_df = df[df["Food_Item"] == target_item].copy()
            sub_df["DateStr"] = sub_df["Date"].dt.strftime("%d %b")
            
            fig_sub, ax_sub = plt.subplots(figsize=(5, 3.8))
            ax_sub.bar(sub_df["DateStr"], sub_df["Quantity_Prepared"], color="#cbd5e1", label="Prepared")
            ax_sub.bar(sub_df["DateStr"], sub_df["Quantity_Sold"], color=colors.get(target_item, "#3b82f6"), label="Sold")
            ax_sub.set_title(f"{target_item}", fontsize=11, fontweight='bold')
            ax_sub.set_ylabel("Units", fontsize=9)
            ax_sub.grid(axis='y', linestyle="--", alpha=0.5)
            ax_sub.legend(loc="upper right", fontsize=8)
            plt.xticks(rotation=45, fontsize=8)
            plt.tight_layout()
            st.pyplot(fig_sub)

# Tab 3: Food Waste Analysis
with tab_waste:
    st.header("Food Waste & Unsold Stock Analysis")
    st.caption("Monitoring unsold food quantities, identifying peak over-preparation days, and tracking waste trends.")

    st.info(
        "💡 **Fieldwork Observation Note on Spoilage vs. Remaining:**\n\n"
        "This tool distinguishes between **remaining unsold food** at closing time and **confirmed spoiled food**. "
        "Because cooked Biryani is perishable and quality degrades overnight, unsold quantities represent a critical risk of "
        "direct food and financial waste unless safely repurposed. Tracking remaining portions helps the kitchen calibrate "
        "daily batch sizes."
    )

    w_col1, w_col2 = st.columns([3, 2])

    with w_col1:
        st.subheader("Daily Unsold Quantities by Item")
        pivot_rem = df.pivot_table(
            index=df["Date"].dt.strftime("%Y-%m-%d"),
            columns="Food_Item",
            values="Quantity_Remaining",
            aggfunc="sum"
        ).fillna(0)

        fig_rem, ax_rem = plt.subplots(figsize=(8, 4.5))
        pivot_rem.plot(kind="bar", stacked=True, ax=ax_rem, color=["#d95f02", "#7570b3", "#1b9e77"])
        ax_rem.set_title("Unsold Quantities at Day Close", fontsize=12, fontweight='bold', pad=10)
        ax_rem.set_xlabel("Date", fontsize=10)
        ax_rem.set_ylabel("Unsold Portions", fontsize=10)
        ax_rem.grid(axis='y', linestyle="--", alpha=0.5)
        ax_rem.legend(title="Food Item")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig_rem)

    with w_col2:
        st.subheader("Days with Highest Unsold Food")
        daily_waste = df.groupby(df["Date"].dt.strftime("%Y-%m-%d")).agg(
            Prepared=("Quantity_Prepared", "sum"),
            Sold=("Quantity_Sold", "sum"),
            Remaining=("Quantity_Remaining", "sum")
        ).reset_index().sort_values(by="Remaining", ascending=False)

        daily_waste["Unsold %"] = (daily_waste["Remaining"] / daily_waste["Prepared"] * 100).round(1)

        for _, row in daily_waste.head(4).iterrows():
            st.warning(
                f"📅 **{row['Date']}**\n\n"
                f"- **Unsold Quantity:** {int(row['Remaining'])} portions ({row['Unsold %']} % of prepared)\n"
                f"- **Prepared:** {int(row['Prepared'])} | **Sold:** {int(row['Sold'])}"
            )

# Tab 4: Preparation Planning
with tab_planning:
    st.header("Daily Preparation Planning & Guidance")
    st.caption("Statistical estimation to guide morning food preparation based on historical sales.")

    st.write(
        """
        The suggestions below are calculated from the average daily customer demand across all recorded dates. 
        Using these averages helps avoid cooking excess portions on normal operating days.
        """
    )

    distinct_days = df["Date"].nunique()
    plan_c1, plan_c2, plan_c3 = st.columns(3)

    for target_item, col_target in zip(["Biryani Half", "Biryani Full", "Chicken Roll"], [plan_c1, plan_c2, plan_c3]):
        with col_target:
            item_df = df[df["Food_Item"] == target_item]
            sales = item_df["Quantity_Sold"]
            
            avg_sold = sales.mean() if not sales.empty else 0
            min_sold = sales.min() if not sales.empty else 0
            max_sold = sales.max() if not sales.empty else 0
            suggested_prep = round(avg_sold)

            st.markdown(f"### {target_item}")
            st.metric("Avg Daily Demand", f"{avg_sold:.1f} units")
            st.metric("Recommended Daily Prep", f"{suggested_prep} units", help="Derived from historical average daily sales.")
            st.write(f"- **Lowest Recorded Sales:** {int(min_sold)} units")
            st.write(f"- **Highest Recorded Sales:** {int(max_sold)} units")
            st.write(f"- **Historical Days Observed:** {distinct_days} days")

    st.markdown("---")
    st.warning(
        "⚠️ **Disclaimer & Limitations of Estimates:**\n\n"
        "- These suggestions are mathematical averages derived strictly from the supplied historical observations.\n"
        "- They are **estimates, not guaranteed future demand**.\n"
        "- A dataset of 10 days provides a helpful baseline for regular weekdays, but external factors such as "
        "college examinations, holidays, weather changes, or student timetables will directly influence actual demand. "
        "The canteen owner should use these numbers as a reference rather than an absolute rule."
    )

# Tab 5: Data Management & Entry
with tab_management:
    st.header("Data Management")
    st.caption("Inspect verified records, export data, or record a new daily observation.")

    m_tab1, m_tab2 = st.tabs(["📋 View & Download Records", "➕ Log New Daily Record"])

    with m_tab1:
        st.subheader("Current Dataset Records")
        st.write(f"Total Records: **{len(df)}** entries across **{distinct_days}** operating days.")
        
        display_df = df.copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(
            display_df[[
                "Date", "Food_Item", "Quantity_Prepared", "Quantity_Sold", 
                "Quantity_Remaining", "Selling_Price", "Revenue"
            ]],
            use_container_width=True
        )

        csv_export = display_df[[
            "Date", "Food_Item", "Quantity_Prepared", "Quantity_Sold", 
            "Quantity_Remaining", "Selling_Price"
        ]].to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Download Data as CSV",
            data=csv_export,
            file_name="canteen_processed_records.csv",
            mime="text/csv"
        )

    with m_tab2:
        st.subheader("Log a New Daily Field Observation")
        st.write("Enter daily numbers to append directly to `data.csv`. `Quantity_Remaining` is calculated automatically.")

        with st.form("new_record_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            
            with f_col1:
                entry_date = st.date_input("Date", value=datetime.date.today())
                entry_item = st.selectbox("Food Item", ["Biryani Half", "Biryani Full", "Chicken Roll"])
                default_price = 90.0 if entry_item == "Biryani Half" else (150.0 if entry_item == "Biryani Full" else 60.0)
                entry_price = st.number_input("Selling Price (₹)", min_value=1.0, value=default_price, step=5.0)

            with f_col2:
                entry_prep = st.number_input("Quantity Prepared", min_value=0, max_value=500, value=25, step=1)
                entry_sold = st.number_input("Quantity Sold", min_value=0, max_value=500, value=20, step=1)
                calc_rem = entry_prep - entry_sold
                st.info(f"Calculated Remaining Quantity: **{calc_rem}** units")

            submit_btn = st.form_submit_button("💾 Save Record to data.csv")

            if submit_btn:
                if entry_sold > entry_prep:
                    st.error("Validation Error: Quantity Sold cannot exceed Quantity Prepared.")
                else:
                    append_record(entry_date, entry_item, entry_prep, entry_sold, entry_price, DATA_PATH)
                    st.success(f"✅ Record for {entry_item} on {entry_date} successfully added to `data.csv`!")
                    st.rerun()
