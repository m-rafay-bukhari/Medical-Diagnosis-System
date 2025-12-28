🏥 Medical Diagnosis System
📖 Overview

The Medical Diagnosis System is an AI-based application that predicts possible diseases based on user-provided symptoms. It uses a Bayesian Network for probabilistic reasoning and Neo4j as a graph database to store and query medical knowledge.

The system is designed as an academic mini-project to demonstrate the use of Artificial Intelligence techniques, especially Bayesian inference, in healthcare decision-making.

🎯 Objectives

To model medical diagnosis using probabilistic reasoning

To handle uncertainty in symptom-disease relationships

To store medical knowledge using a graph-based approach

To provide accurate disease predictions based on symptoms

🧠 Key Technologies Used

Python

Bayesian Networks

Neo4j Graph Database

Basic NLP processing

Graph-based knowledge representation

📂 Project Structure
Medical-Diagnosis-System/
│
├── app/
│   ├── main.py                # Main application entry point
│   ├── bayesian.py            # Bayesian Network implementation
│   ├── knowledge_loader.py    # Loads medical knowledge into Neo4j
│   ├── knowledge_query.py     # Queries disease-symptom relationships
│   ├── nlp_loader.py          # Processes symptom text input
│   └── __init__.py
│
├── db/
│   └── connection.py          # Neo4j database connection
│
├── knowledge.txt              # Medical knowledge base
├── knowledge-graph.png        # Knowledge graph visualization
├── knowledge-graph-2.png
└── README.md

⚙️ How the System Works

Medical knowledge is stored in a Neo4j knowledge graph

Symptoms and diseases are connected using relationships

Bayesian probabilities are assigned to symptom-disease links

User inputs symptoms

Bayesian inference calculates disease probabilities

The most likely disease is returned as output

🧮 Algorithm Used
Bayesian Network

Handles uncertainty in medical diagnosis

Uses conditional probabilities

Computes posterior probability of diseases using:

𝑃(𝐷𝑖𝑠𝑒𝑎𝑠𝑒 ∣ 𝑆𝑦𝑚𝑝𝑡𝑜𝑚𝑠)
P(Disease∣Symptoms)

This allows prediction even when incomplete symptom data is provided.

🚀 How to Run the Project

Install Python dependencies

Set up Neo4j database

Load medical knowledge using knowledge_loader.py

Run the application:

python app/main.py

📊 Features

Probabilistic disease prediction

Knowledge-based reasoning

Graph visualization of medical data

Modular and well-structured code

Suitable for AI and Data Science learning

🎓 Academic Use

This project is ideal for:

AI / Machine Learning courses

Bayesian Network demonstrations

Healthcare decision-support studies

University mini or semester projects

👨‍💻 Author

M. Rafay Bukhari
BS Computer Science
COMSATS University Lahore