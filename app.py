import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="DateTime Excel Generator", layout="centered")

st.title("📅 DateTime Excel Generator")

with st.expander("📖 Glossary & How-to", expanded=False):
    st.markdown("""
    ## ⚡ Options
    - **Start Date / End Date:** Defines the date range.
    - **Interval:** Time step for the generated series:
      - 5 min, 15 min, 30 min, or 1 hour.
    - **Output Format:**
      - *Date + Time in one column* → single combined string.
      - *Date and Time in separate columns* → useful for load/PV models.

    ## 🔄 How it Works
    1. Select your start and end date.
    2. Choose the time interval.
    3. Pick the output format (one column vs. two columns).
    4. Click **Generate Excel File**.
    5. Download the ready-to-use Excel sheet.

    ## 📊 Use Cases
    - Create synthetic time-series templates.
    - Build load or PV generation profiles.
    - Feed into simulators (DC/AC coupled, financial models, etc.).
    """)


with st.expander("📖 Glossary & How-to", expanded=False):
    st.markdown("""
    ## ⚡ Options
    - **Start Date / End Date:** Defines the date range.
    - **Interval:** Time step for the generated series:
      - 5 min, 15 min, 30 min, or 1 hour.
    - **Output Format:**
      - *Date + Time in one column* → single combined string.
      - *Date and Time in separate columns* → useful for load/PV models.

    ## 🔄 How it Works
    1. Select your start and end date.
    2. Choose the time interval.
    3. Pick the output format (one column vs. two columns).
    4. Click **Generate Excel File**.
    5. Download the ready-to-use Excel sheet.

    ## 📊 Use Cases
    - Create synthetic time-series templates.
    - Build load or PV generation profiles.
    - Feed into simulators (DC/AC coupled, financial models, etc.).
    """)


# --- User Inputs ---
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

interval_options = {
    "5 minutes": "5min",
    "15 minutes": "15min",
    "30 minutes": "30min",
    "1 hour": "1h"
}
interval = st.selectbox("Select Time Interval", list(interval_options.keys()))

# New option for output format
format_option = st.radio(
    "Select Output Format",
    ["Date + Time in one column", "Date and Time in separate columns"]
)

# --- Generate Button ---
if st.button("Generate Excel File"):
    if start_date and end_date:
        if start_date > end_date:
            st.error("⚠️ End date must be after start date")
        else:
            # Create datetime range
            dt_range = pd.date_range(
                start=pd.to_datetime(start_date),
                end=pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(minutes=1),
                freq=interval_options[interval]
            )

            # Format DataFrame based on selection
            if format_option == "Date + Time in one column":
                df = pd.DataFrame({"DateTime": dt_range.strftime("%d/%m/%Y %H:%M")})
            else:
                df = pd.DataFrame({
                    "Date": dt_range.strftime("%d/%m/%Y"),
                    "Time": dt_range.strftime("%H:%M")
                })

            # Save to Excel in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:  # safer default
                df.to_excel(writer, index=False, sheet_name="DateTime")

            st.success("✅ Excel file generated!")
            st.download_button(
                label="📥 Download Excel",
                data=output.getvalue(),
                file_name="datetime_list.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("Please select start and end dates.")
