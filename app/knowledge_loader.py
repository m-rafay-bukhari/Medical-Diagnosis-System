from db.connection import driver

def load_knowledge(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    with driver.session() as session:
        
        for line in lines:
            line = line.strip().rstrip(".")
            
            if not line:
                continue

        
            disease_part, symptoms_part = line.split(" has symptoms ")

            disease = disease_part.strip()
            symptoms = [s.strip() for s in symptoms_part.split(",")]

            session.execute_write(
                create_disease_and_symptoms,
                disease,
                symptoms
            )


def create_disease_and_symptoms(tx, disease, symptoms):
    tx.run(
        "MERGE (d:Disease {name: $name})",
        name=disease
    )

    for symptom in symptoms:
        tx.run("""
            MERGE (s:Symptom {name: $symptom})
            WITH s
            MATCH (d:Disease {name: $disease})
            MERGE (d)-[:CAUSES]->(s)
        """, symptom=symptom, disease=disease)
        # can do MERGE (d)-[:HAS_SYMPTOM]->(s)