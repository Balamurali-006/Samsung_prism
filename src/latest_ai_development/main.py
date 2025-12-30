import json
import sys
import re

from crews.discovery_crew import run_discovery_crew
from crews.collection_crew import run_collection_crew
from crews.analysis_crew import run_analysis_crew
from crews.aggregation_crew import run_aggregation_crew
from tools.token_counter import get_token_summary


# --------------------------------------------------
# Utility: Extract JSON from markdown-wrapped LLM output
# --------------------------------------------------
def extract_json_from_raw(raw_text: str):
    if not raw_text:
        return None

    # Remove ```json ``` or ``` wrappers and extract JSON object
    # Handle both ```json\n...\n``` and ```\n...\n``` formats
    cleaned = re.sub(r"```json\s*\n?|\n?```", "", raw_text).strip()
    
    # If there's still leading/trailing text, try to find the JSON object
    if cleaned and not cleaned.startswith("{"):
        # Try to find JSON object starting with {
        json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if json_match:
            cleaned = json_match.group(0)
        else:
            # If no JSON found, return None
            return None

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        # Log the error for debugging
        print(f"⚠️ JSON parse error: {e}")
        print(f"Attempted to parse: {cleaned[:200]}...")
        return None


def main(company_name: str):
    print(f"\n🚀 Starting Competitor Intelligence for: {company_name}\n")

    # --------------------------------------------------
    # 1️⃣ Discovery Phase
    # --------------------------------------------------
    print("🔍 Discovering competitors...")
    discovery_output = run_discovery_crew(company_name)

    discovery_data = (
        discovery_output.json_dict
        or extract_json_from_raw(discovery_output.raw)
    )

    if not discovery_data:
        print("RAW DISCOVERY OUTPUT:")
        print(discovery_output.raw)
        raise RuntimeError("❌ Discovery crew did not return valid JSON")

    competitors = discovery_data.get("competitors", [])
    print(f"✅ Found {len(competitors)} competitors")

    # --------------------------------------------------
    # 2️⃣ Collection Phase
    # --------------------------------------------------
    print("\n🌐 Collecting competitor data...")
    collected_data = []

    for comp in competitors:
        name = comp.get("name")
        website = comp.get("website")

        if not website:
            print(f"⚠️ Skipping {name}, no website found")
            continue

        try:
            collection_output = run_collection_crew(name, website)

            collection_data = (
                collection_output.json_dict
                or extract_json_from_raw(collection_output.raw)
            )

            if collection_data:
                collected_data.append(collection_data)
                print(f"  ✔ Collected data for {name}")
            else:
                print(f"  ⚠️ No structured data for {name}")

        except Exception as e:
            print(f"  ❌ Failed collecting {name}: {e}")

    # --------------------------------------------------
    # 3️⃣ Strategic Analysis Phase
    # --------------------------------------------------
    print("\n🧠 Running strategic analysis...")
    analysis_output = run_analysis_crew(company_name, collected_data)

    strategy_data = (
        analysis_output.json_dict
        or extract_json_from_raw(analysis_output.raw)
    )

    if not strategy_data:
        print("RAW ANALYSIS OUTPUT:")
        print(analysis_output.raw)
        raise RuntimeError("❌ Strategic analysis failed")

    # --------------------------------------------------
    # 4️⃣ Aggregation Phase
    # --------------------------------------------------
    print("\n📦 Aggregating final insights...")
    final_payload = {
        "company": company_name,
        "competitors": competitors,
        "competitor_details": collected_data,
        "strategy": strategy_data
    }

    aggregation_output = run_aggregation_crew(final_payload)

    final_json = (
        aggregation_output.json_dict
        or extract_json_from_raw(aggregation_output.raw)
    )

    if not final_json:
        print("RAW AGGREGATION OUTPUT:")
        print(aggregation_output.raw)
        raise RuntimeError("❌ Aggregation failed")

    # --------------------------------------------------
    # 5️⃣ Output
    # --------------------------------------------------
    print("\n✅ Competitor Intelligence Report Generated\n")
    print(json.dumps(final_json, indent=2))

    with open("competitor_report.json", "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2)

    print("\n💾 Saved as competitor_report.json\n")
    
    # --------------------------------------------------
    # 6️⃣ Token Usage Summary
    # --------------------------------------------------
    print(get_token_summary())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <company_name>")
        sys.exit(1)

    company = sys.argv[1]
    main(company)
