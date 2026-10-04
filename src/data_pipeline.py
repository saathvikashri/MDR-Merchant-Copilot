import pandas as pd
import streamlit as st
import random
from datetime import datetime, timedelta

def generate_mock_data():
    """
    Generates 50 dummy transactions with intentional deduction errors for testing.
    """
    data = []
    start_date = datetime(2026, 10, 15)
    categories = ['Grocery', 'Electronics', 'Pharmacy', 'Apparel']
    
    for i in range(1, 51):
        txn_id = f"TXN{1000 + i}"
        date = start_date + timedelta(days=random.randint(0, 10))
        amount = round(random.uniform(500, 5000), 2)
        category = random.choice(categories)
        
        if amount > 2000:
            expected_fee = min(amount * 0.009, 50.0)
        else:
            expected_fee = 0.0
            
        actual_fee = expected_fee
        
        if i % 8 == 0:
            actual_fee = expected_fee + random.uniform(10, 30)
            
        actual_fee = round(actual_fee, 2)
        settled_amount = round(amount - actual_fee, 2)
        
        data.append([txn_id, date.strftime('%Y-%m-%d'), amount, 'UPI', category, settled_amount, actual_fee])
        
    columns = ['Transaction_ID', 'Date', 'Amount', 'Payment_Mode', 'Merchant_Category', 'Settled_Amount', 'Actual_Fee_Deducted']
    return pd.DataFrame(data, columns=columns)

def load_data():
    """
    Provides the UI for file uploads, applies schema validation, and handles missing data.
    Exposes a CSV file uploader and a 'Load Sample Audit Data' fallback in the sidebar.
    """
    st.sidebar.header("📁 Data Ingestion")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Settlement CSV", 
        type=['csv'], 
        help="Upload a settlement CSV containing Amount, Actual_Fee_Deducted, Settled_Amount, and Merchant_Category."
    )
    load_sample_btn = st.sidebar.button("Load Sample Audit Data")

    # If the user clicks the sample data button, record in session state
    if load_sample_btn:
        st.session_state["use_sample"] = True

    # 1. User uploaded a CSV file
    if uploaded_file is not None:
        # User uploaded a file, clear sample mode
        st.session_state["use_sample"] = False
        try:
            df = pd.read_csv(uploaded_file)
            
            # The exact columns the engine needs to do the math
            required_columns = ['Amount', 'Actual_Fee_Deducted', 'Settled_Amount', 'Merchant_Category']
            
            # 1. Check if the file is completely empty (headers only, no rows)
            if df.empty:
                st.sidebar.error("Error: The uploaded file has no data rows. Please upload a file containing transactions.")
                return None
                
            # 2. Check for missing or incorrectly named columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.sidebar.error(f"Error: Your file is missing these exact columns: {', '.join(missing_columns)}")
                st.sidebar.info(f"Please rename your CSV columns to match these exactly: {', '.join(required_columns)}")
                return None
                
            st.sidebar.success("File uploaded and validated successfully.")
            return df
            
        except Exception as e:
            st.sidebar.error(f"Error: Could not read the uploaded file. Details: {str(e)}")
            return None

    # 2. User chose to use sample audit data
    elif st.session_state.get("use_sample", False):
        st.sidebar.info("ℹ️ Using sample audit data.")
        if "sample_df" not in st.session_state:
            st.session_state["sample_df"] = generate_mock_data()
        return st.session_state["sample_df"]

    # 3. Neither uploaded nor sample selected
    else:
        st.info("👈 Please upload a settlement CSV file or click **'Load Sample Audit Data'** in the sidebar to begin the audit.")
        return None
