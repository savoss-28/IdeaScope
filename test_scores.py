import sys
import os

# Set up Django environment manually if needed, or just import analysis.py directly
sys.path.append(r"c:\Users\Shripad Thakur\.gemini\antigravity\playground\Django-IIVP\IdeaProj")
from IdeaApp.analysis import calculate_uniqueness, calculate_feasibility, calculate_impact, calculate_innovation

tests = [
    {
        "title": "To-Do App",
        "desc": "A simple todo app to manage daily tasks.",
        "domain": "Productivity",
        "complexity": 2,
        "sim": 0.8,
        "repo_count": 50,
        "total_count": 1000
    },
    {
        "title": "AI Resume Analyzer",
        "desc": "Uses natural language processing and machine learning to score resumes.",
        "domain": "HR",
        "complexity": 6,
        "sim": 0.5,
        "repo_count": 10,
        "total_count": 50
    },
    {
        "title": "Smart Parking",
        "desc": "IoT and sensors based real-time parking detection system.",
        "domain": "Smart City",
        "complexity": 8,
        "sim": 0.2,
        "repo_count": 2,
        "total_count": 10
    },
    {
        "title": "Blockchain Voting",
        "desc": "Decentralized voting system using smart contract on blockchain.",
        "domain": "Governance",
        "complexity": 9,
        "sim": 0.1,
        "repo_count": 1,
        "total_count": 5
    },
    {
        "title": "Chat App",
        "desc": "Real-time messaging chat application with websockets.",
        "domain": "Communication",
        "complexity": 5,
        "sim": 0.7,
        "repo_count": 30,
        "total_count": 500
    },
    {
        "title": "Quote Generator",
        "desc": "Simple random quote generator website.",
        "domain": "Entertainment",
        "complexity": 1,
        "sim": 0.9,
        "repo_count": 100,
        "total_count": 2000
    }
]

for t in tests:
    print(f"--- {t['title']} ---")
    u, _ = calculate_uniqueness(t['sim'], t['repo_count'], t['total_count'], t['title'], t['desc'])
    f, _ = calculate_feasibility(t['complexity'], t['title'], t['desc'])
    i, _ = calculate_impact(t['domain'], t['title'], t['desc'])
    inn, _ = calculate_innovation(t['title'], t['desc'], u)
    
    print(f"Uniqueness: {u}")
    print(f"Feasibility: {f}")
    print(f"Impact: {i}")
    print(f"Innovation: {inn}")
    print()
