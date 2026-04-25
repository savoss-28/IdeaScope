"""
IdeaScope - GitHub API Integration Module
Adapted from IIVP GUI (Tkinter) version.
Handles fetching repository data from GitHub's REST API.
"""

import requests
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor, as_completed


GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"


def check_github_connection():
    """Check API connectivity and rate limit status."""
    try:
        response = requests.get("https://api.github.com/rate_limit", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def search_github_repos(query, max_results=10):
    """
    Search GitHub repositories matching the given query.

    Args:
        query (str): Search query (idea title + domain keywords).
        max_results (int): Maximum number of repositories to return.

    Returns:
        dict: Custom dict with 'total_count', 'repositories', and 'error'
    """
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }

    # Use GitHub token if available (increases rate limit)
    github_token = getattr(settings, 'GITHUB_TOKEN', None)
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": min(max_results, 100),
    }

    try:
        response = requests.get(
            GITHUB_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=15,
        )
        # Handle custom errors
        if response.status_code == 403:
            return {
                "total_count": 0,
                "repositories": [],
                "error": "GitHub API rate limit exceeded. Please wait a moment and try again."
            }
        elif response.status_code == 422:
            return {
                "total_count": 0,
                "repositories": [],
                "error": "Invalid search query. Please refine your idea description."
            }
            
        response.raise_for_status()
        data = response.json()

        repositories = []
        for repo in data.get("items", [])[:max_results]:
            repositories.append({
                "name": repo.get("name", "N/A"),
                "full_name": repo.get("full_name", "N/A"),
                "description": repo.get("description", "") or "No description available",
                "stars": repo.get("stargazers_count", 0),
                "url": repo.get("html_url", "#"),
                "language": repo.get("language", "Unknown") or "Unknown",
                "forks": repo.get("forks_count", 0),
                "topics": repo.get("topics", []),
            })

        return {
            "total_count": data.get("total_count", 0),
            "repositories": repositories,
            "error": None,
        }

    except requests.exceptions.Timeout:
        return {
            "total_count": 0,
            "repositories": [],
            "error": "GitHub API request timed out. Please try again.",
        }
    except requests.exceptions.ConnectionError:
        return {
            "total_count": 0,
            "repositories": [],
            "error": "Could not connect to GitHub. Check your internet connection.",
        }
    except Exception as e:
        return {
            "total_count": 0,
            "repositories": [],
            "error": f"An unexpected error occurred: {str(e)}",
        }


def search_multiple_queries(queries, max_results_per=10):
    """
    Search multiple queries in parallel using thread pool.
    
    Args:
        queries (list): List of search query strings.
        max_results_per (int): Max results per query.
        
    Returns:
        dict: Custom dict with 'total_count', 'repositories', and 'error'
    """
    all_repos = []
    seen_urls = set()
    total_count = 0
    error_msg = None
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(search_github_repos, q, max_results_per): q
            for q in queries
        }
        for future in as_completed(futures):
            try:
                result = future.result()
                if result["error"]:
                    # Keep the first error we see
                    if not error_msg:
                        error_msg = result["error"]
                
                total_count += result.get("total_count", 0)
                
                for repo in result.get("repositories", []):
                    url = repo.get("url", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        all_repos.append(repo)
            except Exception:
                pass
    
    # Sort deduplicated results by stars descending
    all_repos.sort(key=lambda r: r.get("stars", 0), reverse=True)
    
    return {
        "total_count": total_count,
        "repositories": all_repos,  # We can return all deduplicated, or slice it to a max later
        "error": error_msg,
    }
