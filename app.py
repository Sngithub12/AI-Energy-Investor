import streamlit as st
from main_agent import run_hybrid_agent

st.set_page_config(page_title="🌍 Investment AI", layout="wide")

st.title("🚀 AI Intelligence Dashboard")
st.markdown("AI-powered Renewable Energy Investment Insights")

query = st.text_input("🔍 Enter Query", placeholder="e.g. top solar companies in India")

if st.button("Analyze"):

    if query:
        results = run_hybrid_agent(query)

        for r in results:
            st.divider()

            st.subheader(f"🌍 {r.get('country', 'N/A')}")

            col1, col2, col3 = st.columns(3)

            col1.metric("Score", round(r.get("score", 0), 2))
            col2.metric("Trend", r.get("trend", "N/A"))
            col3.metric("Companies", r.get("num_companies", 0))

            st.markdown("### 💼 Investment Analysis")

            st.write(f"**Market Attractiveness:** {r.get('market_attractiveness', 'N/A')}")
            st.write(f"**Competition:** {r.get('competition', 'N/A')}")
            st.write(f"**Investment Required:** {r.get('investment_required', 'N/A')}")
            st.write(f"**ROI Potential:** {r.get('roi', 'N/A')}")
            st.write(f"**Recommendation:** {r.get('recommendation', 'N/A')}")

            st.markdown("### 🧠 Insight")
            st.info(r.get("insight", "No insight available"))

            st.markdown("### 🏢 Companies")
            for c in r.get("companies", []):
                st.write(f"- {c.get('company', 'N/A')}")

            st.markdown("### 📊 Company Financial Insights")

            for ci in r.get("company_insights", []):
                st.write(f"**{ci['company']}**")
                st.write(f"💰 Investment: {ci['investment']}")
                st.write(f"📈 ROI: {ci['roi']}")
                st.write(f"💵 Profit: {ci['profit']}")
                st.write("---")

            st.success(f"📊 Total Companies: {r.get('num_companies', 0)}")

    else:
        st.warning("Enter a query first")