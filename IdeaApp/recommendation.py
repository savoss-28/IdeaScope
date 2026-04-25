"""
IdeaScope - Intelligent Recommendation Engine
Ported from IIVP GUI application.
Generates tech stacks, improvements, risks, strategies, and verdicts.
"""

class RecommendationEngine:
    """Generates intelligent recommendations with clear, approachable language."""

    TECH_STACKS = {
        "Web Development": {
            "Frontend": ["React", "Vue.js", "Next.js", "Svelte", "Vanilla JS"],
            "Backend": ["Django", "Node.js", "FastAPI", "Express"],
            "Database": ["PostgreSQL", "MongoDB", "Redis"],
            "Deployment": ["Vercel", "AWS", "Docker + Kubernetes"],
        },
        "Mobile Development": {
            "Cross-Platform": ["React Native", "Flutter", "Kotlin Multiplatform"],
            "Native": ["Swift (iOS)", "Kotlin (Android)"],
            "Backend": ["Firebase", "Supabase", "AWS Amplify"],
        },
        "AI / Machine Learning": {
            "Frameworks": ["TensorFlow", "PyTorch", "scikit-learn", "Hugging Face"],
            "Data Tools": ["Pandas", "NumPy", "Apache Spark"],
            "Deployment": ["MLflow", "Kubeflow", "SageMaker"],
            "Visualization": ["Matplotlib", "Plotly", "Streamlit"],
        },
        "Data Science": {
            "Analysis": ["Pandas", "NumPy", "SciPy"],
            "Visualization": ["Matplotlib", "Seaborn", "Plotly", "Tableau"],
            "Workflow": ["Jupyter", "Apache Airflow", "dbt"],
            "Database": ["PostgreSQL", "BigQuery", "Snowflake"],
        },
        "DevOps / Cloud": {
            "CI/CD": ["GitHub Actions", "Jenkins", "GitLab CI"],
            "Containers": ["Docker", "Kubernetes", "Podman"],
            "Cloud Providers": ["AWS", "GCP", "Azure"],
            "Monitoring": ["Prometheus", "Grafana", "Datadog"],
        },
        "Cybersecurity": {
            "Tools": ["Wireshark", "Burp Suite", "Metasploit"],
            "Frameworks": ["OWASP", "NIST", "MITRE ATT&CK"],
            "Languages": ["Python", "Go", "Rust"],
        },
        "Blockchain": {
            "Platforms": ["Ethereum", "Solana", "Polkadot"],
            "Dev Tools": ["Hardhat", "Truffle", "Foundry"],
            "Languages": ["Solidity", "Rust", "Move"],
        },
        "IoT": {
            "Hardware": ["Raspberry Pi", "Arduino", "ESP32"],
            "Protocols": ["MQTT", "CoAP", "HTTP/2"],
            "Platforms": ["AWS IoT", "Azure IoT Hub", "ThingsBoard"],
        },
        "Game Development": {
            "Engines": ["Unity", "Unreal Engine", "Godot"],
            "Languages": ["C#", "C++", "GDScript"],
            "Tools": ["Blender", "Aseprite", "FMOD"],
        },
        "Finance": {
            "Backend": ["Java", "Python", "Go"],
            "Database": ["PostgreSQL", "TimescaleDB", "Redis"],
            "Security": ["OWASP API Security", "OAuth 2.0", "mTLS"],
        },
        "Healthcare": {
            "Standards": ["HL7", "FHIR", "HIPAA Compliant Cloud"],
            "Backend": ["Python", "Java", "C#"],
            "Database": ["PostgreSQL", "MongoDB (Encrypted)"],
        },
        "Education": {
            "Frontend": ["React", "Vue"],
            "Backend": ["Django", "Node.js"],
            "Video/Streaming": ["WebRTC", "Mux", "AWS IVS"],
        },
        "General": {
            "Languages": ["Python", "JavaScript", "Go", "Rust"],
            "Dev Tools": ["Git", "Docker", "VS Code"],
            "Databases": ["PostgreSQL", "SQLite", "Redis"],
        },
    }

    def generate_recommendations(
        self, scores: dict, keywords: list, domain: str,
        complexity: int, similarity: float, repo_count: int
    ) -> dict:
        """Generate comprehensive recommendations with user-friendly language."""
        recs = {
            "improvements": [],
            "risks": [],
            "strategies": [],
            "tech_stack": {},
            "overall_verdict": "",
        }

        uniqueness = scores.get("uniqueness", 50)
        feasibility = scores.get("feasibility", 50)
        impact = scores.get("impact", 50)
        innovation = scores.get("innovation", 50)

        # Map integer complexity 1-10 to categorical
        comp_str = "Advanced" if complexity >= 8 else ("Intermediate" if complexity >= 4 else "Beginner")

        recs["improvements"] = self._generate_improvements(
            uniqueness, feasibility, impact, similarity, keywords, domain
        )
        recs["risks"] = self._generate_risks(
            uniqueness, feasibility, impact, similarity, repo_count, comp_str
        )
        recs["strategies"] = self._generate_strategies(
            uniqueness, feasibility, impact, innovation, domain, comp_str
        )
        recs["tech_stack"] = self._get_tech_stack(domain)
        recs["overall_verdict"] = self._generate_verdict(
            innovation, uniqueness, feasibility, impact
        )

        return recs

    def _generate_improvements(self, uniqueness, feasibility, impact, similarity, keywords, domain) -> list:
        improvements = []
        domain_tips = {
            "Web Development": "🌐 Architecture: Add Progressive Web App (PWA) features for offline usability. Ensure maximum lighthouse performance scores for SEO.",
            "AI / Machine Learning": "🧠 Trust & Ethics: Incorporate explainable AI (XAI) models to let users understand the reasoning behind outputs. Ensure data pipelines are bias-tested.",
            "Mobile Development": "📱 User Experience: Implement an offline-first data model using SQLite/Realm. Ensure deep linking is supported for marketing campaigns.",
            "Data Science": "📊 Automation: Automate your data cleaning pipelines using tools like Airflow or dbt. Add anomaly detection before dashboard generation."
        }
        improvements.append(domain_tips.get(domain, "⚡ Performance: Focus on optimizing core workflows. Profile your code to reduce load times and ensure a snappy user experience."))

        if uniqueness < 40:
            improvements.append("🔄 Stand Out: Many similar projects already exist. Try adding a unique feature or combining it with another idea (for example, adding AI features to a simple To-Do app).")
        elif uniqueness >= 70:
            improvements.append("✅ New Idea Potential: This idea is quite unique. Before building everything, first check if people are interested by creating a simple demo or basic version.")

        if impact < 50:
            improvements.append("📈 Increase Value: Right now, the idea has limited impact. Try adding features that save users time, effort, or money.")
        else:
            improvements.append("🎯 Ready for Growth: This idea has strong impact. You can think about adding security features and advanced options to make it suitable for real-world use.")

        if feasibility < 50:
            improvements.append("🔧 Simplify Build: This project may be complex to build. Start with a basic version (MVP) and use existing tools or APIs instead of building everything from scratch.")
        
        if len(improvements) < 4:
            improvements.append("📚 Improve Code Quality: Use proper testing and keep your code organized. This will make your project easier to manage as it grows.")

        return improvements
    
    def _generate_risks(self, uniqueness, feasibility, impact, similarity, repo_count, complexity) -> list:
        risks = []
        if complexity == "Advanced":
            risks.append("🔴 High Complexity Risk: Advanced projects can become too complicated. You might end up building too many features before checking if people actually need them.")
        else:
            risks.append("⚠️ Code Quality Risk: Starting simple is good, but if you don’t follow good coding practices, your code can become messy later.")

        if uniqueness < 40 or similarity > 0.5:
            risks.append("⚠️ High Competition: Many similar projects already exist. It may be difficult to attract users unless your idea offers something different.")

        if feasibility < 40:
            risks.append("⚠️ Build Difficulty: This project may be hard to complete with current resources. Time and effort required could be high.")

        if impact < 40:
            risks.append("📉 Low User Engagement: The idea may not solve a strong problem, so users might not continue using it regularly.")

        if repo_count > 15:
            risks.append("📉 Easy to Copy: Many similar projects exist, so others can easily build something like this too.")
        elif repo_count == 0:
            risks.append("🔍 Uncertain Demand: No similar projects found. This could be a unique idea, but it might also mean there is no real demand.")

        if len(risks) < 3:
            risks.append("⚠️ External Dependency Risk: Depending too much on external tools or APIs can cause issues if they stop working or change.")

        return risks

    def _generate_strategies(self, uniqueness, feasibility, impact, innovation, domain, complexity) -> list:
        strategies = []
        strategies.append("🎯 Start Fast: Build and launch a simple version of your app quickly (within 2 weeks) instead of spending too much time perfecting it early.")

        if innovation >= 70:
            strategies.append("🏆 Growth Strategy: Since your idea is highly innovative, you can make parts of it open source to attract users, while offering advanced features as paid services.")
        else:
            strategies.append("📢 Share Your Journey: If the idea is not very unique, focus on sharing your progress online. People are more likely to support and follow your project.")

        if uniqueness < 50 and impact >= 60:
            strategies.append("💎 Focus on Execution: Even if similar projects exist, you can stand out by creating a clean, smooth, and user-friendly design.")

        if domain in ("AI / Machine Learning", "Data Science"):
            strategies.append("📊 Use Data Smartly: Collect and use your own data over time. This will help you improve your system and stay ahead of others.")

        if complexity == "Advanced":
            strategies.append("🧩 Build Step by Step: Start with a simple structure first. Only move to complex architecture when your app grows and needs it.")
        
        if len(strategies) < 4:
            strategies.append("📋 Focus on Users: Think about how users will discover your app. Promotion and reach are just as important as building the app.")

        return strategies

    def _get_tech_stack(self, domain: str) -> dict:
        return self.TECH_STACKS.get(domain, self.TECH_STACKS["General"])

    def _generate_verdict(self, innovation, uniqueness, feasibility, impact) -> str:
        overall = (uniqueness * 0.3 + feasibility * 0.25 + impact * 0.25 + innovation * 0.20)
        
        if overall >= 75:
            return "🌟 EXCELLENT — This idea shows exceptional potential! It scores well across metrics. Highly recommended to pursue — start building your MVP today."
        elif overall >= 60:
            return "✅ STRONG — A solid idea with good potential for success. Review the risks and improvement suggestions above, address weak spots, and you'll have a winning project."
        elif overall >= 45:
            return "🟡 PROMISING — Your idea has merit but needs some refinement. Focus on the areas where you scored lowest and consider the suggestions to strengthen it."
        elif overall >= 30:
            return "🟠 NEEDS REFINEMENT — The idea could work but faces challenges. Consider pivoting, narrowing your scope, or adding features that increase uniqueness."
        else:
            return "🔴 HIGH RISK — This idea faces significant challenges. The market may be too crowded or the concept too generic. Idea pivot recommended."
