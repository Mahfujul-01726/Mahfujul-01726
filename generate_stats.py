#!/usr/bin/env python3
"""
Generate professional GitHub statistics for portfolio
Collects: coding activity, projects completed, learning hours, contributions
"""

import os
import sys
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict
import time
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
GITHUB_USERNAME = "mahfujul-01726"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set as environment variable for security
OUTPUT_FILE = "./stats.json"

# If token not set, try without authentication (limited requests)
HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

# Create session with retry strategy
def create_session():
    """Create a requests session with retry strategy"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

SESSION = create_session()

def get_user_info():
    """Fetch GitHub user information"""
    print("📊 Fetching user information...")
    url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️  Error fetching user info: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_user_repos():
    """Fetch all user repositories"""
    print("📚 Fetching repositories...")
    repos = []
    page = 1
    
    while True:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100&page={page}"
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                repos.extend(data)
                page += 1
                time.sleep(0.5)  # Rate limiting
            else:
                break
        except Exception as e:
            print(f"⚠️  Error fetching repos: {e}")
            break
    
    return repos

def get_repo_commits(repo_name):
    """Fetch commits from a repository"""
    commits = []
    page = 1
    
    while True:
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/commits?per_page=100&page={page}"
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                commits.extend(data)
                page += 1
                time.sleep(0.3)
            else:
                break
        except Exception as e:
            print(f"⚠️  Error fetching commits from {repo_name}: {e}")
            break
    
    return commits

def calculate_activity_stats(all_commits):
    """Calculate daily, monthly, yearly activity statistics"""
    print("📈 Calculating activity statistics...")
    
    daily_commits = defaultdict(int)
    monthly_commits = defaultdict(int)
    yearly_commits = defaultdict(int)
    
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    
    for commit in all_commits:
        try:
            commit_date = datetime.fromisoformat(commit['commit']['author']['date'].replace('Z', '+00:00'))
            
            # Only count commits from last year
            if commit_date >= one_year_ago:
                day_key = commit_date.strftime("%Y-%m-%d")
                month_key = commit_date.strftime("%Y-%m")
                year_key = commit_date.strftime("%Y")
                
                daily_commits[day_key] += 1
                monthly_commits[month_key] += 1
                yearly_commits[year_key] += 1
        except Exception as e:
            continue
    
    return {
        "daily": dict(sorted(daily_commits.items())),
        "monthly": dict(sorted(monthly_commits.items())),
        "yearly": dict(sorted(yearly_commits.items()))
    }

def calculate_learning_hours(all_commits):
    """Estimate learning hours based on commit patterns"""
    print("🎓 Calculating learning hours...")
    
    # Estimate: ~1 hour per commit (conservative estimate)
    total_commits = len(all_commits)
    learning_hours = total_commits * 1.5  # 1.5 hours average per commit
    
    return round(learning_hours, 0)

def get_contribution_stats(repos_data):
    """Calculate contribution statistics"""
    print("🔄 Calculating contribution statistics...")
    
    total_forks = sum(1 for repo in repos_data if repo['fork'])
    total_stars = sum(repo['stargazers_count'] for repo in repos_data)
    repos_with_stars = sum(1 for repo in repos_data if repo['stargazers_count'] > 0)
    
    # Count active projects (pushed to within last 3 months)
    three_months_ago = datetime.now() - timedelta(days=90)
    active_projects = 0
    
    for repo in repos_data:
        try:
            pushed_date = datetime.fromisoformat(repo['pushed_at'].replace('Z', '+00:00'))
            if pushed_date >= three_months_ago:
                active_projects += 1
        except:
            pass
    
    return {
        "total_repos": len(repos_data),
        "forked_repos": total_forks,
        "original_projects": len(repos_data) - total_forks,
        "total_stars": total_stars,
        "repos_with_stars": repos_with_stars,
        "active_projects_3m": active_projects
    }

def get_language_stats(repos_data):
    """Calculate language statistics"""
    print("💻 Calculating language statistics...")
    
    languages = defaultdict(int)
    
    for repo in repos_data:
        if repo['language']:
            languages[repo['language']] += 1
    
    return dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))

def generate_statistics():
    """Main function to generate all statistics"""
    print("🚀 Starting GitHub Statistics Generation...\n")
    
    # Fetch user info
    user_info = get_user_info()
    if not user_info:
        print("❌ Failed to fetch user information")
        return
    
    print(f"✓ User: {user_info['name']} (@{user_info['login']})")
    print(f"✓ Account created: {user_info['created_at']}\n")
    
    # Fetch all repos
    repos_data = get_user_repos()
    print(f"✓ Found {len(repos_data)} repositories\n")
    
    # Collect all commits
    print("📝 Fetching commits from all repositories...")
    all_commits = []
    for idx, repo in enumerate(repos_data):
        if not repo['fork']:  # Only original projects
            commits = get_repo_commits(repo['name'])
            all_commits.extend(commits)
            if (idx + 1) % 5 == 0:
                print(f"   ✓ Processed {idx + 1}/{len(repos_data)} repos")
    
    print(f"✓ Total commits collected: {len(all_commits)}\n")
    
    # Calculate all statistics
    activity_stats = calculate_activity_stats(all_commits)
    learning_hours = calculate_learning_hours(all_commits)
    contribution_stats = get_contribution_stats(repos_data)
    language_stats = get_language_stats(repos_data)
    
    # Compile final statistics
    final_stats = {
        "generated_at": datetime.now().isoformat(),
        "username": GITHUB_USERNAME,
        "profile": {
            "name": user_info.get('name', 'N/A'),
            "bio": user_info.get('bio', 'N/A'),
            "location": user_info.get('location', 'N/A'),
            "followers": user_info['followers'],
            "following": user_info['following'],
            "public_repos": user_info['public_repos']
        },
        "activity": {
            "daily": activity_stats['daily'],
            "monthly": activity_stats['monthly'],
            "yearly": activity_stats['yearly'],
            "total_commits": len(all_commits)
        },
        "projects": {
            "total_repositories": contribution_stats['total_repos'],
            "original_projects": contribution_stats['original_projects'],
            "forked_projects": contribution_stats['forked_repos'],
            "active_projects_3m": contribution_stats['active_projects_3m'],
            "repos_with_stars": contribution_stats['repos_with_stars']
        },
        "contributions": {
            "total_stars": contribution_stats['total_stars'],
            "followers": user_info['followers'],
            "public_gists": user_info['public_gists']
        },
        "learning": {
            "estimated_hours": int(learning_hours),
            "commit_based_hours": int(learning_hours)
        },
        "languages": language_stats,
        "activity_summary": {
            "total_commits_last_year": len(all_commits),
            "avg_commits_per_day": round(len(all_commits) / 365, 2) if all_commits else 0,
            "max_commits_in_day": max([int(v) for v in activity_stats['daily'].values()]) if activity_stats['daily'] else 0,
            "busiest_month": max(activity_stats['monthly'], key=activity_stats['monthly'].get) if activity_stats['monthly'] else "N/A"
        }
    }
    
    # Save to file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(final_stats, f, indent=2)
    
    print(f"\n✅ Statistics generated successfully!")
    print(f"📁 Saved to: {OUTPUT_FILE}\n")
    
    # Display summary
    print("=" * 60)
    print("📊 STATISTICS SUMMARY")
    print("=" * 60)
    print(f"Total Commits (last year): {final_stats['activity']['total_commits']}")
    print(f"Original Projects: {final_stats['projects']['original_projects']}")
    print(f"Total Stars: {final_stats['contributions']['total_stars']}")
    print(f"Estimated Learning Hours: {final_stats['learning']['estimated_hours']}")
    print(f"Average Commits/Day: {final_stats['activity_summary']['avg_commits_per_day']}")
    print(f"Followers: {final_stats['contributions']['followers']}")
    print(f"Top Language: {list(language_stats.keys())[0] if language_stats else 'N/A'}")
    print("=" * 60)
    
    return final_stats

if __name__ == "__main__":
    stats = generate_statistics()
