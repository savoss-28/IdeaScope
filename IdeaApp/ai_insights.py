"""
IdeaScope - AI Insights Module
Balanced explanations: clear, descriptive, and user-friendly.
"""

def get_level(score):
    if score < 50:
        return "low"
    elif score <= 70:
        return "medium"
    return "high"


def generate_explanations(data):
    """Generates clear but descriptive explanations."""

    title = data.get("title", "this idea")
    scores = data.get("scores", {})

    u = scores.get("uniqueness", 0)
    f = scores.get("feasibility", 0)
    i = scores.get("impact", 0)
    inn = scores.get("innovation", 0)

    u_level = get_level(u)
    f_level = get_level(f)
    i_level = get_level(i)
    inn_level = get_level(inn)

    exp = {
        "uniqueness": f"The idea '{title}' has a {u_level} uniqueness score ({u}/100). " +
                      ("This suggests that many similar solutions already exist, making it harder to stand out in the market." if u_level == "low" else
                       "This indicates some level of differentiation, although parts of the idea overlap with existing solutions." if u_level == "medium" else
                       "This shows strong originality, with the idea standing out clearly from most existing solutions."),

        "feasibility": f"The feasibility score is {f_level} ({f}/100). " +
                       ("This means the implementation could be technically challenging and may require advanced tools, time, or expertise." if f_level == "low" else
                        "This indicates the idea is achievable with proper planning and structured development." if f_level == "medium" else
                        "This suggests the idea can be implemented using standard technologies and is practical to build."),

        "impact": f"The impact score is {i_level} ({i}/100). " +
                  ("This shows the idea has limited reach and mainly serves a specific or smaller use-case." if i_level == "low" else
                   "This indicates the idea provides useful value to a defined group of users or improves existing workflows." if i_level == "medium" else
                   "This reflects strong real-world relevance, with the potential to solve important problems or benefit a large audience."),

        "innovation": f"The innovation score is {inn_level} ({inn}/100). " +
                      ("This means the idea relies mostly on standard approaches without introducing new or advanced technologies." if inn_level == "low" else
                       "This shows the use of modern technologies or concepts, but in a relatively common way." if inn_level == "medium" else
                       "This highlights the use of advanced or emerging technologies in a creative and impactful way.")
    }

    exp["summary"] = (
        f"Overall, '{title}' appears to be a "
        f"{'highly distinctive' if u_level == 'high' else 'competitive'} idea that is "
        f"{'straightforward to implement' if f_level == 'high' else 'moderately complex to build'} "
        f"and delivers "
        f"{'strong real-world impact.' if i_level == 'high' else 'focused practical value.'}"
    )

    return exp


def generate_suggestions(data):
    """Generates structured and practical suggestions."""

    scores = data.get("scores", {})
    suggestions = []

    # Uniqueness
    u = scores.get("uniqueness", 0)
    if u < 50:
        suggestions.append({
            "category": "Uniqueness",
            "text": "Consider refining the idea by targeting a specific niche or adding a unique feature that differentiates it from existing solutions."
        })
    elif u <= 70:
        suggestions.append({
            "category": "Uniqueness",
            "text": "You can improve differentiation by introducing specialized features, personalization, or a unique user experience."
        })
    else:
        suggestions.append({
            "category": "Uniqueness",
            "text": "The idea is already distinct. Focus on execution quality and speed to maintain this advantage."
        })

    # Feasibility
    f = scores.get("feasibility", 0)
    if f < 50:
        suggestions.append({
            "category": "Feasibility",
            "text": "Break the project into smaller parts and start with a basic MVP to reduce complexity and risk."
        })
    elif f <= 70:
        suggestions.append({
            "category": "Feasibility",
            "text": "Leverage existing tools, frameworks, or cloud services to simplify development and improve efficiency."
        })
    else:
        suggestions.append({
            "category": "Feasibility",
            "text": "Since the idea is easy to implement, focus on optimizing performance and delivering a smooth user experience."
        })

    # Impact
    i = scores.get("impact", 0)
    if i < 50:
        suggestions.append({
            "category": "Impact",
            "text": "Try aligning the idea with a real-world problem that affects a broader audience or industry."
        })
    elif i <= 70:
        suggestions.append({
            "category": "Impact",
            "text": "Expand the reach by adding features like accessibility support, localization, or integration with other platforms."
        })
    else:
        suggestions.append({
            "category": "Impact",
            "text": "The idea has strong impact potential. Consider collaborations or scaling strategies to maximize its reach."
        })

    # Innovation
    inn = scores.get("innovation", 0)
    if inn < 50:
        suggestions.append({
            "category": "Innovation",
            "text": "Enhance the idea by incorporating modern technologies such as AI, automation, or data-driven features."
        })
    elif inn <= 70:
        suggestions.append({
            "category": "Innovation",
            "text": "You can improve innovation by adding real-time capabilities, intelligent decision-making, or adaptive features."
        })
    else:
        suggestions.append({
            "category": "Innovation",
            "text": "The idea is already technologically strong. Focus on making the advanced features intuitive and user-friendly."
        })

    return suggestions