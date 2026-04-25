from django.db import models
from django.contrib.auth.models import User


class Idea(models.Model):
    """Stores a user-submitted project idea."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')
    title = models.CharField(max_length=200)
    description = models.TextField()
    domain = models.CharField(max_length=100)
    complexity = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Analysis(models.Model):
    """Stores the analysis results for an idea."""
    idea = models.OneToOneField(Idea, on_delete=models.CASCADE, related_name='analysis')
    uniqueness_score = models.FloatField(default=0)
    feasibility_score = models.FloatField(default=0)
    impact_score = models.FloatField(default=0)
    innovation_score = models.FloatField(default=0)
    competition_level = models.CharField(max_length=20, default='Low')
    competition_detail = models.TextField(blank=True, default='')
    similarity = models.FloatField(default=0)
    keywords = models.JSONField(default=list)
    weighted_keywords = models.JSONField(default=list)
    github_repos = models.JSONField(default=list)
    github_total_count = models.IntegerField(default=0)
    github_error = models.CharField(max_length=500, blank=True, default='')
    score_reasons = models.JSONField(default=dict)
    recommendations = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for: {self.idea.title}"
