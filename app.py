import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from database import SessionLocal
from models import Expense
from ai_service import analyze_expense_with_ai

st.set_page_config(page_title="AI Smart Expense Tracker",
                   page_icon="💳", layout="wide")
st.title("💳 AI-Powered Smart Expense Tracker")

st.sidebar.header("🔑 API Setup")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

db = SessionLocal()

st.subheader("🤖 Add Expense using AI")
tab1, tab2 = st.tabs(["📝 Natural Language Text", "📸 Upload Receipt Photo"])
parsed_data = None

with tab1:
    text_desc = st.text_input(
        "Type your spend (e.g., 'Paid 450 for Uber ride'):")
    if st.button("Extract from Text", type="primary") and api_key and text_desc:
        with st.spinner("Parsing text..."):
            parsed_data = analyze_expense_with_ai(
                api_key, text_input=text_desc)

with tab2:
    uploaded_file = st.file_uploader(
        "Upload Receipt Image", type=["jpg", "jpeg", "png"])
    if uploaded_file and st.button("Extract from Receipt Image", type="primary") and api_key:
        with st.spinner("Analyzing image..."):
            image = Image.open(uploaded_file)
            parsed_data = analyze_expense_with_ai(api_key, image_input=image)

if parsed_data:
    new_expense = Expense(
        item=parsed_data['item'],
        amount=float(parsed_data['amount']),
        category=parsed_data['category']
    )
    db.add(new_expense)
    db.commit()
    st.toast("✅ Expense saved successfully!")
    st.rerun()

st.divider()
st.subheader("📊 Spend Analytics & History")
expenses_query = db.query(Expense).all()

if expenses_query:
    data = [{"ID": e.id, "Item": e.item, "Amount": e.amount, "Category": e.category,
             "Date": e.date.strftime("%Y-%m-%d %H:%M")} for e in expenses_query]
    df = pd.DataFrame(data)

    chart_col, table_col = st.columns([1, 1])
    with chart_col:
        fig_pie = px.pie(df, values="Amount", names="Category", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    with table_col:
        st.dataframe(df.sort_values(by="ID", ascending=False),
                     use_container_width=True)
else:
    st.info("No transaction records found yet.")
# UI styling adjustments
