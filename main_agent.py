import pandas as pd
from tinyfish_agent import get_companies_for_country
from utils import extract_countries_from_query


# ==============================
# 📊 DATA LOADING
# ==============================

def load_data():
    df = pd.read_csv("data/owid-energy-data.csv")
    return df


def get_latest_data():
    df = load_data()
    latest_year = df["year"].max()
    return df[df["year"] == latest_year]

def detect_energy_type(query):
    query = query.lower()

    if "solar" in query:
        return "solar power"
    elif "biofuel" in query:
        return "biofuel"
    elif "coal" in query:
        return "coal"
    else:
        return "renewable energy"
# ==============================
# 📈 SCORING + TRENDS
# ==============================

def calculate_score(row):
    # Weighted score (customize as needed)
    solar = row.get("solar_share_elec", 0)
    renewable = row.get("renewables_share_elec", 0)

    return (solar * 0.6) + (renewable * 0.4)


def detect_trend_for_country(country):
    df = load_data()
    country_df = df[df["country"] == country].sort_values("year")

    if len(country_df) < 2:
        return "Stable"

    first = country_df.iloc[0]
    last = country_df.iloc[-1]

    if last["solar_share_elec"] > first["solar_share_elec"]:
        return "Coal → Solar Transition"
    elif last["renewables_share_elec"] > first["renewables_share_elec"]:
        return "Renewable Growth"
    else:
        return "Stable"


def get_country_score(country):
    df = get_latest_data()
    row = df[df["country"] == country]

    if row.empty:
        return 50  # default fallback

    return calculate_score(row.iloc[0])


# ==============================
# 💡 INVESTOR LOGIC
# ==============================

def competition_level(num_companies):
    if num_companies > 10:
        return "High"
    elif num_companies > 5:
        return "Medium"
    else:
        return "Low"


def investment_required(competition):
    if competition == "High":
        return "High CapEx ($$$)"
    elif competition == "Medium":
        return "Moderate CapEx ($$)"
    else:
        return "Low CapEx ($)"


def roi_estimate(score, competition):
    if score > 80 and competition != "High":
        return "High ROI (15–25%) 🚀"
    elif score > 60:
        return "Moderate ROI (10–15%)"
    else:
        return "Low ROI (3–8%) ⚠️"


def investment_recommendation(score, competition):
    if score > 80 and competition != "High":
        return "Strong Buy ✅"
    elif score > 60:
        return "Moderate Investment ⚖️"
    else:
        return "High Risk ❌"


def market_attractiveness(score):
    if score > 80:
        return "Very High"
    elif score > 60:
        return "High"
    elif score > 40:
        return "Medium"
    else:
        return "Low"


# ==============================
# 🧠 INSIGHT ENGINE
# ==============================

def generate_insight(country, score, trend):
    if score > 80:
        return f"{country} is a high-growth renewable market with strong {trend}. Ideal for long-term investments."
    elif score >= 50:
        return f"{country} shows moderate renewable expansion. Good for balanced portfolios."
    else:
        return f"{country} has limited renewable growth. Suitable only for high-risk investors."
import random

def estimate_company_financials(company, score, competition):
    # Base investment (in $ millions)
    if competition == "High":
        investment = random.randint(50, 150)
    elif competition == "Medium":
        investment = random.randint(20, 80)
    else:
        investment = random.randint(5, 30)

    # ROI multiplier based on score
    if score > 80:
        roi_percent = random.uniform(15, 25)
    elif score > 60:
        roi_percent = random.uniform(10, 15)
    else:
        roi_percent = random.uniform(3, 8)

    # Profit calculation
    annual_profit = (investment * roi_percent) / 100

    return {
        "company": company.get("company", "N/A"),
        "investment_million_usd": round(investment, 2),
        "roi_percent": round(roi_percent, 2),
        "estimated_annual_profit_million": round(annual_profit, 2)
    }

# ==============================
# 🚀 MAIN AGENT
# ==============================

def run_hybrid_agent(query):
    print("🚀 Running Opportunity Intelligence Agent...")

    results = []

    # 🔥 Step 1: Extract countries from query
    query_countries = extract_countries_from_query(query)

    if query_countries:
        print(f"🌍 Countries detected from query: {query_countries}")
        selected_countries = query_countries
    else:
        # fallback → dataset top countries
        df_latest = get_latest_data()
        df_latest["score"] = df_latest.apply(calculate_score, axis=1)

        top_countries = df_latest.sort_values(
            by="score", ascending=False
        ).head(3)

        selected_countries = top_countries["country"].tolist()

    # ==============================
    # 🔁 PROCESS EACH COUNTRY
    # ==============================

    for country in selected_countries:
        try:
            score = get_country_score(country)
            trend = detect_trend_for_country(country)
            insight = generate_insight(country, score, trend)

            print(f"\n🌍 {country} | Score: {round(score,2)} | Trend: {trend}")

            # 🔥 TinyFish call with query context
            energy_type = detect_energy_type(query)

            companies = get_companies_for_country(
            country,
            f"{energy_type} companies in {country}")
            num_companies = len(companies)
            

            competition = competition_level(num_companies)
            investment = investment_required(competition)
            roi = roi_estimate(score, competition)
            recommendation = investment_recommendation(score, competition)
            attractiveness = market_attractiveness(score)

            # ==============================
            # 📊 PRINT INVESTOR REPORT
            # ==============================

            print("\n💼 Investment Analysis:")
            print(f"- Market Attractiveness: {attractiveness}")
            print(f"- Competition: {competition}")
            print(f"- Investment Required: {investment}")
            print(f"- ROI Potential: {roi}")
            print(f"- Recommendation: {recommendation}")

            print(f"\n🧠 Insight: {insight}")

            print("\n🏢 Companies:")
            print("\n🏢 Company Financial Insights:")
            company_insights = []

            for c in companies:
                    financials = estimate_company_financials(c, score, competition)
                    company_insights.append(financials)
            # Sort companies by profit
            company_insights = sorted(
                company_insights,
                key=lambda x: x["estimated_annual_profit_million"],
                reverse=True
                )

            top_3 = company_insights[:3]

            print("\n🏆 Top Investment Picks:")
            for c in top_3:
                print(f"- {c['company']} (${c['estimated_annual_profit_million']}M profit)")

           

            print(f"\n- {financials['company']}")
            print(f"  💰 Investment: ${financials['investment_million_usd']}M")
            print(f"  📈 ROI: {financials['roi_percent']}%")
            print(f"  💵 Annual Profit: ${financials['estimated_annual_profit_million']}M") 

            print(f"\n📊 Total Companies Found: {num_companies}")

            # ==============================
            # 📦 STORE RESULTS
            # ==============================

            results.append({
                "country": country,
                "score": round(score, 2),
                "trend": trend,
                "insight": insight,
                "companies": companies,
                "company_financials": company_insights,
                "num_companies": num_companies,
                "competition": competition,
                "investment_required": investment,
                "roi": roi,
                "recommendation": recommendation,
                "market_attractiveness": attractiveness
            })
            

        except Exception as e:
            print(f"❌ Error processing {country}: {e}")

    # ==============================
    # 🏆 FINAL COMPARISON (MULTI COUNTRY)
    # ==============================

    if len(results) > 1:
        print("\n🏆 FINAL COMPARISON:")

        best = max(results, key=lambda x: x["score"])
        print(f"👉 Best Market: {best['country']}")

        for r in results:
            print(f"- {r['country']} | Score: {r['score']} | ROI: {r['roi']}")

    return results