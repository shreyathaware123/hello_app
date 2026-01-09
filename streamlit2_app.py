import streamlit as st
import pandas as pd

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="OLA Ride Analytics Dashboard", layout="wide")

# ---------------------- LOAD DATA ----------------------


@st.cache_data
def load_data():
    df = pd.read_csv("OLA_Ride_Cleaned_file.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


df = load_data()
# ---------------------- DARK THEME CSS ----------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0B0F14;
    color: white;
}

.stSidebar {
    background-color: #0E1117 !important;
}

.stSidebar label,
.stSidebar span,
.stSidebar div {
    color: white !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #121821 !important;
    color: white !important;
    border: 1px solid #2A2F3A !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

/* Dropdown */
ul[role="listbox"] {
    background-color: #121821 !important;
    border: 1px solid #2A2F3A !important;
}

li[role="option"] {
    background-color: #121821 !important;
    color: white !important;
}

li[role="option"]:hover,
li[aria-selected="true"] {
    background-color: #1F2633 !important;
    color: white !important;
}

/* KPI Cards */
.stMetric {
    background-color: #121821;
    border: 1px solid #2A2F3A;
    border-radius: 14px;
    padding: 18px;
}

.stMetric label {
    color: #C9D1D9 !important;
}

.stMetric div {
    color: white !important;
    font-weight: 600;
}

h1, h2, h3, h4 {
    color: white;
}
</style>
""", unsafe_allow_html=True)


# ---------------------- SIDEBAR ----------------------
st.sidebar.title("🔍 Filters")

page = st.sidebar.radio(
    "Navigation",
    ["Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings"]
)

booking_status = ["All"] + \
    sorted(df["Booking_Status"].dropna().unique().tolist())
vehicle_type = ["All"] + sorted(df["Vehicle_Type"].dropna().unique().tolist())
payment_method = ["All"] + \
    sorted(df["Payment_Method"].dropna().unique().tolist())

bs = st.sidebar.selectbox("Booking Status", booking_status)
vt = st.sidebar.selectbox("Vehicle Type", vehicle_type)
pm = st.sidebar.selectbox("Payment Method", payment_method)

# ---------------------- FILTER DATA ----------------------
filtered_df = df.copy()

if bs != "All":
    filtered_df = filtered_df[filtered_df["Booking_Status"] == bs]
if vt != "All":
    filtered_df = filtered_df[filtered_df["Vehicle_Type"] == vt]
if pm != "All":
    filtered_df = filtered_df[filtered_df["Payment_Method"] == pm]

# ---------------------- TITLE ----------------------
st.title("🚖 OLA Ride Analytics Dashboard 🚖")

# ====================== OVERALL PAGE ======================
if page == "Overall":

    st.subheader("Key Metrics")
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("TOTAL RIDES", len(filtered_df))
    c2.metric("TOTAL REVENUE (₹)",
              f"{filtered_df['Booking_Value'].sum():,.0f}")
    c3.metric("AVG CUSTOMER RATING", round(
        filtered_df["Customer_Rating"].mean(), 2))
    c4.metric("TOTAL RIDE DISTANCE (KM)", round(
        filtered_df["Ride_Distance"].sum(), 2))

    st.markdown("### Ride Volume Over Time")
    rides_over_time = (
        filtered_df.groupby("Date")
        .size()
        .reset_index(name="Rides")
        .set_index("Date")
    )
    st.line_chart(rides_over_time)

    st.markdown("### Booking Status Breakdown")
    status_df = (
        filtered_df.groupby("Booking_Status")
        .size()
        .reset_index(name="Count")
        .set_index("Booking_Status")
    )
    st.bar_chart(status_df)

# ====================== VEHICLE TYPE PAGE ======================
elif page == "Vehicle Type":

    st.markdown("### Top 5 Vehicle Types by Ride Distance")
    vehicle_df = (
        filtered_df.groupby("Vehicle_Type")["Ride_Distance"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    st.bar_chart(vehicle_df)

# ====================== REVENUE PAGE ======================
elif page == "Revenue":

    st.markdown("### Revenue by Payment Method")
    payment_df = (
        filtered_df.groupby("Payment_Method")["Booking_Value"]
        .sum()
    )
    st.bar_chart(payment_df)

    st.markdown("### Top 5 Customers by Total Booking Value")
    customer_df = (
        filtered_df.groupby("Customer_ID")["Booking_Value"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    st.bar_chart(customer_df)

# ====================== CANCELLATION PAGE ======================
elif page == "Cancellation":

    st.markdown("### Cancellation Type Breakdown")
    cancel_df = (
        df[df["IsCompleted"] == 0]
        .groupby("Cancellation_Type")
        .size()
    )
    st.bar_chart(cancel_df)

# ====================== RATINGS PAGE ======================
elif page == "Ratings":

    st.markdown("### Driver Ratings Distribution")
    driver_df = (
        filtered_df.groupby("Driver_Ratings")
        .size()
    )
    st.bar_chart(driver_df)

    st.markdown("### Customer Ratings Distribution")
    customer_df = (
        filtered_df.groupby("Customer_Rating")
        .size()
    )
    st.bar_chart(customer_df)
