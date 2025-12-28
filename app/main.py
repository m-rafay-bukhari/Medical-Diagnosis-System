from app.nlp_loader import load_knowledge_with_nlp
from app.bayesian import run_diagnosis
from app.knowledge_query import query_diseases_by_symptoms


print("Step 1: Loading knowledge into Neo4j...")
load_knowledge_with_nlp("knowledge.txt", default_probability=0.8)
print("Knowledge loaded successfully!\n")



observed = {
    "Fever": 1,
    "Cough": 1,
    "Shortness of Breath": 0
}


print("Step 2: Running Bayesian diagnosis based on observed symptoms...")
results = run_diagnosis(observed)
print("Bayesian diagnosis completed.\n")


print("Ranked Diseases based on observed symptoms:")
for disease, prob in results[:10]:  # top 10
    print(f"{disease}: {prob:.2f}")
print("\n")



patient_symptoms = ["Fever", "Cough", "Shortness of Breath"]
print("Step 3: Querying Neo4j for possible diseases based on symptoms...")
possible_diseases = query_diseases_by_symptoms(patient_symptoms)


print("Possible diseases based on symptoms:")
for disease in possible_diseases:
    print(f"- {disease}")
print("\n")



# load_knowledge_with_nlp("knowledge.txt", default_probability=0.8)
# print("Medical knowledge reloaded into Neo4j.")
