from db.connection import driver

def query_diseases_by_symptoms(symptoms):
    
    with driver.session() as session:

        query = """
            MATCH (d:Disease)-[:CAUSES]->(s:Symptom)
            WHERE s.name IN $symptoms
            RETURN DISTINCT d.name AS disease
        """
        result = session.run(query, symptoms=symptoms)
        diseases = [record["disease"] for record in result]
        
        return diseases
