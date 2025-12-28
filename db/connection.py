import os
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "Abcd@12345"

# URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
# USER = os.getenv("NEO4J_USER", "neo4j")
# PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))