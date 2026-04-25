"""
IdeaScope - Advanced Idea Analysis Engine
Adapted from IIVP GUI (Tkinter) version's AnalysisEngine class.

Performs keyword extraction, TF-IDF vectorization, cosine similarity
computation, multi-dimensional scoring, and provides score explanations.
"""

from pydoc import text
import re
import hashlib
from collections import Counter

from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine

from .recommendation import RecommendationEngine


STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
    "your", "yours", "yourself", "yourselves", "he", "him", "his",
    "himself", "she", "her", "hers", "herself", "it", "its", "itself",
    "they", "them", "their", "theirs", "themselves", "what", "which",
    "who", "whom", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "having",
    "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while", "of", "at", "by", "for",
    "with", "about", "against", "between", "through", "during", "before",
    "after", "above", "below", "to", "from", "up", "down", "in", "out",
    "on", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "both",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "s", "t",
    "can", "will", "just", "don", "should", "now", "would", "could",
    "also", "use", "using", "used", "make", "made", "like", "want",
    "need", "get", "new", "one", "two", "many", "much", "way", "well",
    "back", "even", "still", "may", "must", "let", "put", "say",
    "going", "thing", "things", "come", "good", "know", "take", "look",
    "based", "system", "app", "application", "project", "build",
    "create", "develop", "tool", "simple", "basic",
}

HIGH_IMPORTANCE_KEYWORDS = {
    "ai", "blockchain", "machine-learning", "deep-learning", "neural",
    "automation", "optimization", "real-time", "scalable", "distributed",
    "quantum", "cryptography", "autonomous", "prediction", "analytics",
    "security", "cloud", "microservice", "kubernetes", "docker",
    "healthcare", "sustainability", "climate", "energy", "fintech",
}

MEDIUM_IMPORTANCE_KEYWORDS = {
    "api", "dashboard", "monitoring", "pipeline", "integration",
    "visualization", "database", "authentication", "notification",
    "search", "recommendation", "streaming", "caching", "testing",
    "deployment", "serverless", "mobile", "responsive", "realtime",
    "collaboration", "productivity", "workflow", "scheduler",
}

UNIQUE_SYSTEM_KEYWORDS = {
    "real-time", "scalable", "distributed", "fault-tolerant",
    "load balancing", "microservices", "event-driven",

    "multi-role", "role-based access", "workflow engine",
    "approval system", "pipeline", "orchestration",

    "data pipeline", "stream processing", "aggregation",
    "sync", "replication", "consistency",

    "api integration", "third-party integration",
    "webhook", "service integration",

    "erp", "crm", "hrms", "procurement system",
    "hospital system", "banking system", "inventory system"
} 

COMPLEX_KEYWORDS = {
    "high": [
        "blockchain", "quantum", "neural network", "deep learning",
        "distributed", "cryptography", "compiler", "kernel", "microservice",
        "real-time rendering", "computer vision", "reinforcement learning",
    ],
    "medium": [
        "machine learning", "artificial intelligence", "ai", "ml",
        "natural language processing", "nlp", "cloud", "devops",
        "kubernetes", "docker", "api gateway", "data pipeline",
        "recommendation engine", "search engine",
    ],
    "low": [
        "crud", "todo", "calculator", "landing page", "blog",
        "portfolio", "static site", "form", "timer", "counter",
    ],
}

GENERIC_IDEAS = [
    "billing system", "invoice system", "to-do app", "todo app",
    "todo list", "chat app", "chat application", "messaging app",
    "e-commerce", "ecommerce", "online store", "shopping cart",
    "blog platform", "portfolio website", "weather app", "calculator",
    "note taking", "notes app", "task manager", "expense tracker",
    "social media", "social network", "url shortener", "quiz app",
    "recipe app", "fitness tracker", "music player", "file manager",
    "login system", "registration system", "contact form",
]

ENTERPRISE_KEYWORDS = [
    "erp", "sap", "procurement", "supply chain",
    "enterprise", "integration", "msd"
]

IMPACT_KEYWORDS = {
    "automation": 15, "automate": 15, "automated": 12,
    "optimization": 14, "optimize": 14, "optimizing": 12,
    "real-time": 13, "realtime": 13,
    "scalable": 12, "scalability": 12,
    "ai": 11, "artificial intelligence": 15,
    "machine learning": 13, "ml": 10,
    "analytics": 10, "dashboard": 8,
    "prediction": 12, "predictive": 12, "forecasting": 12,
    "security": 11, "monitoring": 9,
    "detection": 10, "intelligent": 11, "smart": 9,
    "autonomous": 14, "distributed": 10,
    "cloud": 8, "performance": 9,
    "efficiency": 12, "efficient": 10,
    "data-driven": 12, "platform": 8, "framework": 7,
    "engine": 8, "pipeline": 9,
    "integration": 7, "visualization": 8,
    "collaboration": 7, "productivity": 9, "innovation": 10,
    "healthcare": 18, "medical": 16, "patient": 14, "diagnosis": 16,
    "education": 16, "learning platform": 15, "student": 12,
    "sustainability": 18, "green energy": 17, "renewable": 16,
    "climate": 17, "carbon": 15, "environment": 14,
    "accessibility": 16, "inclusive": 14, "disability": 15,
    "cost reduction": 14, "cost-effective": 13, "affordable": 12,
    "energy": 13, "power consumption": 14,
    "safety": 13, "emergency": 14, "disaster": 13,
    "poverty": 15, "food security": 16, "water": 13,
    "transportation": 12, "logistics": 13, "supply chain": 14,
    "privacy": 13, "data protection": 14,
    "mental health": 16, "wellness": 12,
    "agriculture": 14, "farming": 13, "crop": 12,
}

HIGH_IMPACT_DOMAINS = {
    "healthcare", "medical", "patient", "diagnosis",
    "education", "learning", "student", "e-learning",
    "sustainability", "climate", "environment", "green energy",
    "agriculture", "food security", "water", "poverty",
    "mental health", "wellness", "disability",
    "safety", "emergency", "disaster", "rescue",
}

ENTERPRISE_IMPACT_KEYWORDS = {
    "erp", "enterprise", "procurement", "supply chain",
    "inventory", "warehouse", "logistics", "vendor",
    "billing", "invoicing", "accounting", "finance",
    "hrms", "payroll", "crm", "customer management",

    "workflow", "automation", "process automation",
    "operations", "management system", "admin panel",
    "dashboard", "reporting", "analytics",

    "banking", "insurance", "fintech", "transaction",
    "payment", "billing system", "audit", "compliance",

    "scalability", "distributed system", "microservices",
    "cloud", "saas", "platform", "integration"
}

SOCIETAL_IMPACT_KEYWORDS = {
    "government", "e-governance", "public service",
    "citizen", "transportation", "smart city",
    "traffic", "urban", "infrastructure",
    "law enforcement", "security system",
    "data protection", "privacy", "cybersecurity"
}

PRODUCTIVITY_IMPACT_KEYWORDS = {
    "productivity", "efficiency", "optimization",
    "collaboration", "communication", "remote work",
    "task management", "scheduler", "automation",
    "notification", "tracking", "monitoring"
}

INNOVATION_KEYWORDS = {
    "ai", "artificial intelligence",
    "ml", "machine learning",
    "deep learning", "neural network",
    "nlp", "natural language processing",
    "computer vision",
    "generative", "llm", "transformer",
    "diffusion",

    "blockchain", "crypto",
    "web3", "decentralized", "smart contract",
    "quantum",
    "iot", "internet of things",
    "ar", "vr", "augmented reality", "virtual reality",
    "metaverse",
    "robotics", "drone", "3d printing",
    "edge computing",

    "microservices", "cloud native",
    "distributed system", "event-driven",
    "real-time system", "low latency",
    "high availability", "fault tolerance",
    "scalable architecture",

    "api gateway", "load balancing",
    "caching strategy", "message queue",
    "pub-sub",

    "automation workflow",
    "smart routing",
    "decision engine",
    "recommendation system",
    "adaptive system"
}

def extract_keywords(text, top_n=15):
    if not text or not text.strip():
        return []
    text_lower = text.lower()
    text_clean = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text_lower)
    words = text_clean.split()
    keywords = [w for w in words if w not in STOPWORDS and len(w) > 2]
    freq = Counter(keywords)
    return [word for word, _ in freq.most_common(top_n)]


def extract_weighted_keywords(text, top_n=15):
    if not text or not text.strip():
        return []
    text_lower = text.lower()
    text_clean = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text_lower)
    words = text_clean.split()
    keywords = [w for w in words if w not in STOPWORDS and len(w) > 2]
    freq = Counter(keywords)

    weighted = []
    for word, count in freq.most_common(20):
        if word in HIGH_IMPORTANCE_KEYWORDS:
            tier = "high"
            base_score = 3.0
        elif word in MEDIUM_IMPORTANCE_KEYWORDS:
            tier = "medium"
            base_score = 2.0
        elif word in IMPACT_KEYWORDS:
            tier = "high"
            base_score = 2.5
        else:
            tier = "low"
            base_score = 1.0

        score = base_score * (1 + 0.3 * min(count - 1, 3))
        weighted.append({"word": word, "weight": tier, "score": round(score, 2)})

    weighted.sort(key=lambda x: x["score"], reverse=True)
    return weighted[:top_n]


def compute_similarity(idea_text, repo_descriptions):
    if not repo_descriptions:
        return 0.0

    valid_descs = [d for d in repo_descriptions if d and d.strip() and d != "No description available"]
    if not valid_descs:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
        corpus = [idea_text.lower()] + [d.lower() for d in valid_descs]
        tfidf_matrix = vectorizer.fit_transform(corpus)
        similarities = sklearn_cosine(tfidf_matrix[0:1], tfidf_matrix[1:])
        avg_sim = float(similarities.mean())
        max_sim = float(similarities.max())
        return round(0.6 * max_sim + 0.4 * avg_sim, 4)
    except Exception:
        return 0.0


def check_input_validity(text):
    words = re.findall(r'[A-Za-z]+', text.lower())

    if not words or len(words) < 3:
        return False, "Input is too short to effectively analyze.", 10.0

    known_tokens = STOPWORDS.copy()
    known_tokens.update([
        "app", "web", "system", "platform", "user", "data", "software", "tool", "mobile",
        "application", "project", "management", "game", "design", "build", "create",
        "website", "database", "api", "interface", "using", "how", "what", "can", "i", "we", "my", "this"
    ])

    for v in COMPLEX_KEYWORDS.values():
        known_tokens.update(v)

    known_tokens.update(GENERIC_IDEAS)

    known_tokens.update(ENTERPRISE_IMPACT_KEYWORDS)
    known_tokens.update(UNIQUE_SYSTEM_KEYWORDS)
    known_tokens.update(INNOVATION_KEYWORDS)

    all_known = set()
    for k in known_tokens:
        all_known.update(k.split())

    meaningful_count = sum(1 for w in words if w in all_known)

    long_words = sum(1 for w in words if len(w) > 4)
    unique_words = len(set(words))

    ratio = meaningful_count / len(words)

    confidence = (
        (ratio * 60) +
        (min(long_words / len(words), 1) * 25) +
        (min(unique_words / len(words), 1) * 15)
    )

    if len(words) >= 5:
        confidence += 5

    longest_consonants = 0
    current_c = 0
    for char in text.lower():
        if char in 'bcdfghjklmnpqrstvwxyz':
            current_c += 1
            longest_consonants = max(longest_consonants, current_c)
        else:
            current_c = 0

    if longest_consonants >= 6:
        confidence -= 40

    if confidence < 25.0:
        return False, "Input does not appear meaningful. Please provide a clearer idea description.", round(confidence, 1)

    return True, "Valid", round(confidence, 1)

def calculate_uniqueness(similarity, repo_count, title, description):
    """Returns (score, explanation) tuple."""
    text = (title + " " + description).lower()
    word_count = len(text.split())
    
    score = 65.0
    
    similarity_penalty = min(similarity * 50.0, 40.0)
    repo_penalty = min(repo_count * 3.0, 25.0)
    
    score -= similarity_penalty
    score -= repo_penalty
    

    GENERIC_TERMS = [
        "todo", "to-do", "calculator", "blog", "portfolio", "ecommerce", "weather app", "quiz app",
        "management system", "library management", "attendance system", "inventory system",
        "tic tac toe", "snake game", "clone", "twitter clone", "netflix clone", "whatsapp clone",
        "chat app", "messaging app", "music player", "video player", "to-do list", "notes app", "crud"
    ]
    if any(term in text for term in GENERIC_TERMS):
        score -= 40.0  
        
    if word_count < 15:
        score -= 15.0
        
    if ("chatgpt" in text or "openai api" in text or "llm wrapper" in text) and ("wrapper" in text or "chatbot" in text or "assistant" in text):
        score -= 20.0

    is_generic = any(term in text for term in GENERIC_TERMS)
    if similarity < 0.1 and repo_count == 0 and not is_generic:
        score += 20.0
    elif similarity < 0.2 and repo_count < 5 and not is_generic:
        score += 10.0
        
    uniqueness = max(20, min(100, round(score)))
    
    if uniqueness <= 30:
        explanation = "Low uniqueness. This is a highly saturated or fundamentally generic project idea."
    elif uniqueness < 70:
        explanation = "Moderate uniqueness. Similar existing solutions were found in the market."
    elif uniqueness < 85:
        explanation = "Good uniqueness with a balanced market presence and room for differentiation."
    else:
        explanation = "Exceptional uniqueness. A highly differentiated concept with almost no direct open-source competitors."
        
    return uniqueness, explanation

def calculate_competition(similarity, repo_count):
    score = repo_count * 0.4 + similarity * 20

    if score < 4 or (repo_count < 5 and similarity < 0.25):
        return {
            "level": "Low",
            "detail": f"Only {repo_count} similar repos found with low semantic similarity ({similarity:.0%}). Excellent differentiation.",
        }
    elif score < 10 or (repo_count < 13 and similarity < 0.45):
        return {
            "level": "Medium",
            "detail": f"{repo_count} similar repos found with moderate similarity ({similarity:.0%}). A competitive but accessible market.",
        }
    else:
        return {
            "level": "High",
            "detail": f"{repo_count} repos found matching this concept tightly ({similarity:.0%}). Red ocean - expect strong competition.",
        }


def calculate_feasibility(complexity, title, description):
    """Returns (score, explanation) tuple."""
    text = (title + " " + description).lower()
    
    score = 90.0

    score -= (complexity * 4.5)
    
    tech_penalty = 0.0
    
    if any(k in text for k in ["quantum computing", "agi", "brain computer interface", "custom os", "kernel module", "custom compiler"]):
        tech_penalty += 20.0
        
    elif any(k in text for k in ["zk-rollups", "zero knowledge proofs", "custom blockchain", "layer 1", "defi protocol"]):
        tech_penalty += 15.0
    elif any(k in text for k in ["blockchain", "crypto", "smart contract", "dapp", "web3"]):
        tech_penalty += 8.0
        
    if any(k in text for k in ["train foundation model", "custom llm", "distributed training"]):
        tech_penalty += 15.0
    elif any(k in text for k in ["deep learning", "neural network", "reinforcement learning", "generative adversarial"]):
        tech_penalty += 10.0
    elif any(k in text for k in ["ai", "machine learning", "ml", "computer vision", "object detection", "nlp"]):
        tech_penalty += 5.0
        
    if any(k in text for k in ["kubernetes cluster", "microservices architecture", "distributed system", "high availability"]):
        tech_penalty += 8.0
    elif any(k in text for k in ["real-time", "websocket", "streaming", "webrtc"]):
        tech_penalty += 4.0
        
    if any(k in text for k in ["static site", "html css", "simple script", "no-code", "low-code", "basic crud", "todo", "to-do", "calculator"]):
        score += 20.0
        
    score -= tech_penalty
        
    feasibility = max(20, min(100, round(score)))
    
    if feasibility < 40:
        explanation = "Very challenging feasibility. Requires expert domain knowledge, significant compute, or advanced distributed architectures."
    elif feasibility < 60:
        explanation = "Lower feasibility. Requires handling advanced technologies or intricate state management."
    elif feasibility < 80:
        explanation = "Moderate feasibility with manageable technical hurdles for an intermediate developer."
    else:
        explanation = "Highly feasible. Relies on standard, well-documented development patterns."

    return feasibility, explanation


def calculate_impact(domain, title, description):
    """Returns (score, explanation) tuple."""
    text = (title + " " + description).lower()
    word_count = len(text.split())
    
    score = 50.0
    
    high_impact_domains = ["healthcare", "education", "sustainability", "climate", "agriculture", "energy", "mental health", "cybersecurity", "disaster response", "accessibility", "poverty", "fintech"]
    if domain.lower() in high_impact_domains:
        score += 15.0
        
    if any(k in text for k in ["open source", "social good", "community driven", "non-profit", "public sector", "democratize", "underprivileged", "rural"]):
        score += 10.0
        
    if any(k in text for k in ["enterprise", "b2b", "workflow automation", "productivity", "efficiency", "supply chain"]):
        score += 5.0
        
    GENERIC_TERMS = [
        "todo", "to-do", "calculator", "blog", "portfolio", "ecommerce", "weather app", "quiz app",
        "clone", "chat app", "messaging app", "music player", "notes app", "crud"
    ]
    if any(term in text for term in GENERIC_TERMS):
        score -= 25.0
        
    if any(k in text for k in ["entertainment", "gaming", "meme", "joke", "prank", "casual game", "fun", "hobby"]):
        score -= 15.0
        
    if word_count < 15:
        score -= 10.0
    
    keyword_weights = 0.0
    for word, value in IMPACT_KEYWORDS.items():
        if word in text:
            keyword_weights += value
            
    score += min(keyword_weights * 0.4, 20.0)
        
    impact = max(20, min(100, round(score)))
    
    if impact > 80:
        explanation = "Exceptional impact potential. Highly aligned with critical global problems or systemic improvements."
    elif impact > 60:
        explanation = "Strong impact. Addresses significant domain-specific challenges or productivity bottlenecks."
    elif impact > 40:
        explanation = "Moderate impact. Useful utility but lacks broader societal or systemic reach."
    else:
        explanation = "Limited impact. Primarily serves as a niche utility or entertainment project."
        
    return impact, explanation

def calculate_innovation(title, description):
    """Returns (score, explanation) tuple."""
    text = (title + " " + description).lower()
    word_count = len(text.split())
    
    score = 40.0
    
    tech_novelty = 0.0
    domains_found = set()
    
    if any(k in text for k in ["quantum computing", "neuromorphic", "agi", "brain computer interface"]):
        tech_novelty += 20.0
        domains_found.add("deep_tech")
        
    if any(k in text for k in ["generative ai", "llm", "foundation model", "autonomous agent", "agentic"]):
        tech_novelty += 20.0
        domains_found.add("gen_ai")

    if any(k in text for k in ["blockchain", "crypto", "web3", "smart contract", "zk-rollups", "defi"]):
        tech_novelty += 15.0
        domains_found.add("web3")
        
    if any(k in text for k in ["ai", "machine learning", "ml", "deep learning", "neural"]):
        tech_novelty += 5.0
        domains_found.add("ai")
    if any(k in text for k in ["computer vision", "image recognition", "object detection"]):
        tech_novelty += 8.0
        domains_found.add("cv")
    if any(k in text for k in ["nlp", "natural language", "speech recognition"]):
        tech_novelty += 8.0
        domains_found.add("nlp")
 
    if any(k in text for k in ["iot", "edge computing", "digital twin", "ar", "vr", "spatial computing", "metaverse"]):
        tech_novelty += 8.0
        domains_found.add("hw_ar")
        
    score += min(tech_novelty, 35.0)
    
    if len(domains_found) >= 3:
        score += 15.0
    elif len(domains_found) == 2:
        score += 8.0
        
    if any(k in text for k in ["wrapper", "clone", "template", "boilerplate"]):
        score -= 20.0
    if any(k in text for k in ["crud", "basic dashboard", "simple api", "todo", "to-do", "calculator", "notes app", "management system"]):
        score -= 20.0
        
    if word_count < 15:
        score -= 10.0
        
    innovation = max(20, min(100, round(score)))
    
    if innovation > 85:
        explanation = "Bleeding-edge innovation. Pushes boundaries with highly advanced, combined emerging technologies."
    elif innovation > 65:
        explanation = "Highly innovative, effectively leveraging modern tech stacks like AI, Web3, or Edge computing."
    elif innovation > 45:
        explanation = "Moderately innovative. Uses standard modern frameworks with slight technological advancements."
    else:
        explanation = "Standard innovation relying entirely on established paradigms and basic CRUD architectures."
        
    return innovation, explanation

def analyze_idea(title, description, domain, complexity, github_data):
    """
    Perform full analysis of a user idea, returning detailed explanations
    and generating strategic recommendations.
    """
    full_text = f"{title} {description} {domain}"
    text_lower = full_text.lower()

    is_valid, reason, confidence = check_input_validity(full_text)
    if not is_valid:
        return {
            "status": "invalid_input",
            "message": reason,
            "confidence": round(confidence, 1),
        }

    keywords = extract_keywords(full_text)
    weighted_keywords = extract_weighted_keywords(full_text)

    repos = github_data.get("repositories", [])
    repo_descriptions = [r.get("description", "") for r in repos]
    total_count = github_data.get("total_count", 0)
    repo_count = len(repos)

    similarity = compute_similarity(full_text, repo_descriptions)

    uniqueness, uniq_reason = calculate_uniqueness(similarity, repo_count, title, description)
    competition = calculate_competition(similarity, repo_count)
    feasibility, feas_reason = calculate_feasibility(complexity, title, description)
    impact, imp_reason = calculate_impact(domain, title, description)
    innovation, inn_reason = calculate_innovation(title, description)

    score_reasons = {
        "uniqueness": uniq_reason,
        "feasibility": feas_reason,
        "impact": imp_reason,
        "innovation": inn_reason,
    }

    recommender = RecommendationEngine()
    current_scores = {
        "uniqueness": uniqueness,
        "feasibility": feasibility,
        "impact": impact,
        "innovation": innovation
    }
    recommendations = recommender.generate_recommendations(
        scores=current_scores,
        keywords=[k["word"] for k in  weighted_keywords],
        domain=domain,
        complexity=complexity,
        similarity=similarity,
        repo_count=repo_count
    )

    return {
        "status": "success",
        "uniqueness": uniqueness,
        "feasibility": feasibility,
        "impact": impact,
        "innovation": innovation,
        "competition": competition,
        "keywords": keywords,
        "weighted_keywords": weighted_keywords,
        "similarity": round(similarity, 4),
        "score_reasons": score_reasons,
        "explanations": score_reasons,
        "recommendations": recommendations,
        "message": None,
    }
