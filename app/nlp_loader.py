import spacy
from db.connection import driver


nlp = spacy.load("en_core_web_sm")


def extract_entities_and_relationship(sentence):

    sentence = sentence.strip().rstrip(".")

    doc = nlp(sentence)

    if " has symptoms " in sentence:
        disease_part, symptoms_part = sentence.split(" has symptoms ")
        disease = disease_part.strip()
        symptoms = [s.strip() for s in symptoms_part.split(",")]
        return disease, symptoms
    
    return None, []


def create_disease_and_symptoms(disease, symptom, probability=None):
    
    with driver.session() as session:
        
        if probability is not None:
            session.run(
                """
                MERGE (d:Disease {name: $disease})
                MERGE (s:Symptom {name: $symptom})
                MERGE (d)-[r:CAUSES]->(s)
                ON CREATE SET r.probability = $probability
                """,
                disease=disease,
                symptom=symptom,
                probability=probability
            )
        else:
            session.run(
                """
                MERGE (d:Disease {name: $disease})
                MERGE (s:Symptom {name: $symptom})
                MERGE (d)-[:CAUSES]->(s)
                """,
                disease=disease,
                symptom=symptom
            )



def load_knowledge_with_nlp(file_path, default_probability=None):
    
    with open(file_path, "r") as file:
        lines= file.readlines()

    
    for line in lines:
        disease, symptoms = extract_entities_and_relationship(line)
        if not disease or not symptoms:
            continue
        
        for symptom in symptoms:
            create_disease_and_symptoms(disease, symptom, default_probability)