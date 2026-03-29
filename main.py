from main_agent import run_hybrid_agent
import csv
import os
import pandas as pd

from main_agent import run_hybrid_agent
import os
# SAVE CSV
# -------------------------------
def save_to_csv(results):
    os.makedirs("output", exist_ok=True)
    file_path = "output/investment_report.csv"

    df = pd.DataFrame(results)
    df.to_csv(file_path, index=False)

    print(f"\n✅ Saved: {file_path}")

# -------------------------------
# MAIN RUN
# -------------------------------
if __name__ == "__main__":
    print("🚀 Hybrid AI Agent")

    query = input("Enter query: ")

    results = run_hybrid_agent(query)

    print("\n📊 FINAL REPORT:\n")

    for r in results:
        print("===================================")
        print(f"🌍 Country: {r.get('country')}")
        
        if "score" in r:
            print(f"📊 Score: {r['score']}")
            print(f"🔄 Trend: {r['trend']}")

            print("\n💼 Investment Analysis:")
            print(f"- Market Attractiveness: {r['market_attractiveness']}")
            print(f"- Competition: {r['competition']}")
            print(f"- Investment Required: {r['investment_required']}")
            print(f"- ROI Potential: {r['roi']}")
            print(f"- Recommendation: {r['recommendation']}")

            print(f"\n🧠 Insight: {r['insight']}")

        print("\n🏢 Companies:")
        for c in r.get("companies", [])[:5]:
            print(f"- {c.get('company', 'N/A')}")

        print(f"\n📊 Total Companies Found: {r.get('num_companies', 0)}")

    save_to_csv(results)