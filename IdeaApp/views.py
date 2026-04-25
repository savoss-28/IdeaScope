"""
IdeaScope - Views Module
Handles authentication, idea submission, analysis, and result display.
"""

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib

from .models import Idea, Analysis
from .github_api import search_multiple_queries
from .analysis import analyze_idea
from .ai_insights import generate_explanations, generate_suggestions


# ── Authentication Views ─────────────────────────────────────────────────────

def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('pass1', '')
        password2 = request.POST.get('pass2', '')

        # Validation
        if not name or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return redirect('register')

        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        password = request.POST.get('pass1', '')

        if not name or not password:
            messages.error(request, "Please enter both username and password.")
            return redirect('login')

        user = authenticate(username=name, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ── Dashboard View ───────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """
    Main dashboard — idea submission form + history of past ideas.
    """
    ideas = Idea.objects.filter(user=request.user).select_related('analysis')
    context = {
        'ideas': ideas,
        'idea_count': ideas.count(),
    }
    return render(request, 'dashboard.html', context)


# ── Analyze Idea View ────────────────────────────────────────────────────────

@login_required
def analyze_idea_view(request):
    """
    Process submitted idea:
    1. Save idea to database
    2. Fetch GitHub repos using ThreadPool multi-query
    3. Run NLP analysis and Recommendations
    4. Save results
    5. Redirect to result page
    """
    if request.method != "POST":
        return redirect('dashboard')

    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    domain = request.POST.get('domain', 'General').strip()
    complexity = request.POST.get('complexity', '5')

    # Validation
    if not title:
        messages.error(request, "Please enter an idea title.")
        return redirect('dashboard')

    if not description:
        messages.error(request, "Please enter an idea description.")
        return redirect('dashboard')

    try:
        complexity = int(complexity)
        complexity = max(1, min(10, complexity))
    except (ValueError, TypeError):
        complexity = 5

    # 1. Save idea
    idea = Idea.objects.create(
        user=request.user,
        title=title,
        description=description,
        domain=domain,
        complexity=complexity,
    )

    # 2. Extract quick keywords for multi-query
    from .analysis import extract_keywords
    quick_kw = extract_keywords(f"{title} {description}")[:5]
    
    queries = [
        title,
        " ".join(quick_kw),
        f"{domain} {title}"
    ]
    github_data = search_multiple_queries(queries, max_results_per=10)

    # 3. Run analysis
    analysis_result = analyze_idea(title, description, domain, complexity, github_data)

    # 4. Handle invalid input
    if analysis_result.get("status") == "invalid_input":
        Analysis.objects.create(
            idea=idea,
            uniqueness_score=0,
            feasibility_score=0,
            impact_score=0,
            innovation_score=0,
            competition_level="N/A",
            competition_detail=analysis_result.get("message", ""),
            similarity=0,
            keywords=[],
            weighted_keywords=[],
            github_repos=github_data.get("repositories", []),
            github_total_count=github_data.get("total_count", 0),
            github_error=github_data.get("error", "") or "",
        )
        messages.warning(request, analysis_result.get("message", "Input was not meaningful enough to analyze."))
        return redirect('result', idea_id=idea.id)

    # 5. Save analysis results
    competition = analysis_result.get("competition", {})
    Analysis.objects.create(
        idea=idea,
        uniqueness_score=analysis_result.get("uniqueness", 0),
        feasibility_score=analysis_result.get("feasibility", 0),
        impact_score=analysis_result.get("impact", 0),
        innovation_score=analysis_result.get("innovation", 0),
        competition_level=competition.get("level", "Low"),
        competition_detail=competition.get("detail", ""),
        similarity=analysis_result.get("similarity", 0),
        keywords=analysis_result.get("keywords", []),
        weighted_keywords=analysis_result.get("weighted_keywords", []),
        github_repos=github_data.get("repositories", []),
        github_total_count=github_data.get("total_count", 0),
        github_error=github_data.get("error", "") or "",
        score_reasons=analysis_result.get("score_reasons", {}),
        recommendations=analysis_result.get("recommendations", {}),
    )

    return redirect('result', idea_id=idea.id)


# ── Result View ──────────────────────────────────────────────────────────────

@login_required
def result(request, idea_id):
    """Display analysis results for a specific idea."""
    idea = get_object_or_404(Idea, id=idea_id, user=request.user)
    analysis = get_object_or_404(Analysis, idea=idea)

    overall = (
        analysis.uniqueness_score * 0.3 +
        analysis.feasibility_score * 0.25 +
        analysis.impact_score * 0.25 +
        analysis.innovation_score * 0.20
    )

    context = {
        'idea': idea,
        'analysis': analysis,
        'overall': round(overall, 1),
        'repos': analysis.github_repos[:8],
        'keywords': analysis.keywords,
        'weighted_keywords': analysis.weighted_keywords,
        'recommendations': analysis.recommendations,
        'score_reasons': analysis.score_reasons,
    }
    return render(request, 'result.html', context)


# ── Compare View ─────────────────────────────────────────────────────────────

@login_required
def compare_ideas(request):
    """Compare two existing ideas."""
    ideas = Idea.objects.filter(user=request.user).select_related('analysis')
    
    # Look in GET or POST
    idea1_id = request.POST.get('idea1') or request.GET.get('idea1')
    idea2_id = request.POST.get('idea2') or request.GET.get('idea2')
    
    idea1 = None
    idea2 = None
    better_idea = None
    
    if idea1_id and idea2_id:
        idea1 = ideas.filter(id=idea1_id).first()
        idea2 = ideas.filter(id=idea2_id).first()
        
        if idea1 and idea2 and hasattr(idea1, 'analysis') and hasattr(idea2, 'analysis'):
            o1 = (idea1.analysis.uniqueness_score * 0.3 + idea1.analysis.feasibility_score * 0.25 + 
                  idea1.analysis.impact_score * 0.25 + idea1.analysis.innovation_score * 0.20)
            o2 = (idea2.analysis.uniqueness_score * 0.3 + idea2.analysis.feasibility_score * 0.25 + 
                  idea2.analysis.impact_score * 0.25 + idea2.analysis.innovation_score * 0.20)
                  
            idea1.overall = round(o1, 1)
            idea2.overall = round(o2, 1)
            
            if o1 > o2:
                better_idea = idea1
            elif o2 > o1:
                better_idea = idea2
            else:
                better_idea = "Tie"
    
    context = {
        'ideas': ideas,
        'idea1': idea1,
        'idea2': idea2,
        'better_idea': better_idea,
    }
    return render(request, 'compare.html', context)
    

# ── Delete Idea View ─────────────────────────────────────────────────────────

@login_required
def delete_idea(request, idea_id):
    """Delete an idea and its analysis."""
    idea = get_object_or_404(Idea, id=idea_id, user=request.user)
    idea.delete()
    messages.success(request, f'Idea "{idea.title}" has been deleted.')
    return redirect('dashboard')


# ── AI Insights API ──────────────────────────────────────────────────────────

@login_required
def generate_insights_api(request):
    """API endpoint to lazily generate AI insights for an idea."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
        
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
        
    title = data.get("title", "")
    description = data.get("description", "")
    
    # Generate cache key
    cache_str = f"{title}_{description}"
    cache_key = "ai_insights_" + hashlib.md5(cache_str.encode('utf-8')).hexdigest()
    
    # Check cache
    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse(cached_data)
        
    # Generate new insights
    explanations = generate_explanations(data)
    suggestions = generate_suggestions(data)
    
    response_data = {
        "explanations": explanations,
        "suggestions": suggestions
    }
    
    # Cache for 24 hours
    cache.set(cache_key, response_data, 60 * 60 * 24)
    
    return JsonResponse(response_data)
