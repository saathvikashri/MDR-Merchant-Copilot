# ==============================================================================
# app.py — Main Application Orchestrator
# ==============================================================================
# This is the ONLY file that needs to be launched to run the full application.
#
# Its only job is to connect the three teammate modules in the correct order:
#
#   1. data_pipeline.py  → load_data()   → loads and validates the CSV upload
#   2. audit_engine.py   → run_audit()   → applies MDR fee rules
#   3. dashboard_view.py → render_ui()   → presents the results to the merchant
#
# This file does NOT:
#   - Generate mock data
#   - Perform MDR calculations
#   - Render any UI widgets of its own
#   - Clean or remap any columns
# ==============================================================================

import sys
import os

# Add the src/ folder to Python's search path so the modules can be found
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from data_pipeline import load_data       # Step 1: CSV upload + validation
from audit_engine import run_audit        # Step 2: MDR audit logic
from dashboard_view import render_ui      # Step 3: Streamlit UI presentation

# ==============================================================================
# EXECUTION FLOW
# ==============================================================================

# Step 1: Load the data via the file uploader defined in data_pipeline.py
# load_data() returns a valid DataFrame if upload succeeded, or None if not.
raw_df = load_data()

# Step 2: Only proceed if the user successfully uploaded a valid CSV
if raw_df is not None:

    # Step 3: Pass the raw DataFrame to the audit engine.
    # run_audit() adds Expected_Fee, Discrepancy_Amount, and Audit_Status columns.
    audited_df = run_audit(raw_df)

    # Step 4: Pass the fully audited DataFrame to the dashboard.
    # render_ui() draws all KPI cards, filters, table, and charts.
    render_ui(audited_df)
