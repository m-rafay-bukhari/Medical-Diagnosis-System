from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from db.connection import driver

DEFAULT_PROB = 0.8

def get_disease_symptom_data():

    disease_symptom = {}
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Disease)-[r:CAUSES]->(s:Symptom)
            RETURN d.name AS disease, s.name AS symptom, r.probability AS prob
        """)

        for row in result:
            disease = row["disease"]
            symptom = row["symptom"]
            prob = row["prob"] if row["prob"] is not None else  0.8

            if disease not in disease_symptom:
                disease_symptom[disease] = {}
            disease_symptom[disease][symptom] = prob
    
    return disease_symptom


def build_dynamic_bn(disease_symptoms):

    model = DiscreteBayesianNetwork()

    symptoms_set = set()

    for disease, symptoms in disease_symptoms.items():
        for symptom in symptoms:
            symptoms_set.add(symptom)
            model.add_edge(symptom, disease)

    for symptom in symptoms_set:
        cpd = TabularCPD(
            variable=symptom,
            variable_card=2,
            values=[[0.5], [0.5]]
        )
        model.add_cpds(cpd)

    for disease, symptoms in disease_symptoms.items():
        parents = list(symptoms.keys())
        if not parents:
            continue

        evidence_card = [2] * len(parents)
        

        import itertools
        values_0 = []
        values_1 = []

        for combo in itertools.product([0,1], repeat=len(parents)):
            prob = 1.0
            for i, val in enumerate(combo):
                p_symptom = symptoms[parents[i]]
                prob *= p_symptom if val == 1 else (1 - p_symptom)
            
            values_1.append(prob)
            values_0.append(1 - prob)

        cpd = TabularCPD(
            variable=disease,
            variable_card=2,
            values=[values_0, values_1],
            evidence=parents,
            evidence_card=evidence_card
        )
        model.add_cpds(cpd)
    
    model.check_model()
    return model



def perform_inference(model, observed, diseases):
    
    inference = VariableElimination(model)
    results = []

    for disease in diseases:
        try:
            q = inference.query([disease], evidence=observed)
            results.append((disease, q.values[1]))
        except:
            continue

    return sorted(results, key=lambda x: x[1], reverse=True)


def run_diagnosis(observed_symptoms):
    
    disease_symptoms = get_disease_symptom_data()
    model = build_dynamic_bn(disease_symptoms)
    ranked_diseases = perform_inference(model, observed_symptoms, disease_symptoms.keys())

    return ranked_diseases