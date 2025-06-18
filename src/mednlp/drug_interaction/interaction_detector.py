# interaction_detector.py

# Simulated drug interaction database
# INTERACTIONS = {
#     ("amoxicillin", "methotrexate"): "Amoxicillin may increase the blood levels of methotrexate.",
#     ("ibuprofen", "aspirin"): "Ibuprofen may interfere with the anti-platelet effect of aspirin.",
#     ("warfarin", "acetaminophen"): "High doses of acetaminophen can increase bleeding risk with warfarin."
# }

# def check_interactions(user_input: str):
#     found_interactions = []
#     drugs = [d.strip().lower() for d in user_input.split(",") if d.strip()]

#     for i in range(len(drugs)):
#         for j in range(i + 1, len(drugs)):
#             pair = (drugs[i], drugs[j])
#             reverse_pair = (drugs[j], drugs[i])

#             if pair in INTERACTIONS:
#                 found_interactions.append({
#                     "drug1": pair[0].capitalize(),
#                     "drug2": pair[1].capitalize(),
#                     "info": INTERACTIONS[pair]
#                 })
#             elif reverse_pair in INTERACTIONS:
#                 found_interactions.append({
#                     "drug1": reverse_pair[0].capitalize(),
#                     "drug2": reverse_pair[1].capitalize(),
#                     "info": INTERACTIONS[reverse_pair]
#                 })

#     return found_interactions


# # ✅ Add this at the end of interaction_detector.py
# if __name__ == "__main__":
#     user_input = input("Enter drug names separated by commas: ")  # e.g., Amoxicillin, Methotrexate
#     results = check_interactions(user_input)

#     if not results:
#         print("✅ No known interactions found.")
#     else:
#         print("\n⚠️ Found drug interactions:")
#         for item in results:
#             print(f"→ {item['drug1']} + {item['drug2']}: {item['info']}")



# interaction_detector.py
from typing import List, Dict  # Add this import at the top

# Simulated drug interaction database
INTERACTIONS = {
    ("amoxicillin", "methotrexate"): "Amoxicillin may increase the blood levels of methotrexate.",
    ("ibuprofen", "aspirin"): "Ibuprofen may interfere with the anti-platelet effect of aspirin.",
    ("warfarin", "acetaminophen"): "High doses of acetaminophen can increase bleeding risk with warfarin."
}

def check_interactions(drug_list: List[str]) -> List[Dict]:
    """Check for interactions between a list of drugs.
    
    Args:
        drug_list: List of drug names (can be mixed case)
        
    Returns:
        List of interaction dictionaries with keys: drug_pair, info
    """
    found_interactions = []
    drugs = [d.strip().lower() for d in drug_list if d.strip()]
    
    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):
            pair = (drugs[i], drugs[j])
            reverse_pair = (drugs[j], drugs[i])

            if pair in INTERACTIONS:
                found_interactions.append({
                    "drug_pair": (drugs[i], drugs[j]),
                    "info": INTERACTIONS[pair]
                })
            elif reverse_pair in INTERACTIONS:
                found_interactions.append({
                    "drug_pair": (drugs[j], drugs[i]),
                    "info": INTERACTIONS[reverse_pair]
                })

    return found_interactions


if __name__ == "__main__":
    # Test the function
    test_drugs = ["Amoxicillin", "Methotrexate"]
    results = check_interactions(test_drugs)
    print(results)