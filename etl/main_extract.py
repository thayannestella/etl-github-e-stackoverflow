from etl.extract.github_extractor import (
    GitHubExtractor
)

from etl.extract.stackoverflow_extractor import (
    StackOverflowExtractor
)

from etl.load.raw_loader import RawLoader

github = GitHubExtractor()

stack = StackOverflowExtractor()

loader = RawLoader()

# ====================================
# REPOSITORIES
# ====================================

github_repos = github.search_repositories()

loader.save_raw_data(
    "github_raw",
    "search/repositories",
    github_repos
)

# ====================================
# COMMITS / ISSUES / PRS
# ====================================

for repo in github_repos["items"][:10]:

    owner = repo["owner"]["login"]

    repo_name = repo["name"]

    # COMMITS
    commits = github.get_commits(
        owner,
        repo_name
    )

    loader.save_raw_data(
        "github_raw",
        f"{repo_name}/commits",
        commits
    )

    # ISSUES
    issues = github.get_issues(
        owner,
        repo_name
    )

    loader.save_raw_data(
        "github_raw",
        f"{repo_name}/issues",
        issues
    )

    # PULL REQUESTS
    prs = github.get_pull_requests(
        owner,
        repo_name
    )

    loader.save_raw_data(
        "github_raw",
        f"{repo_name}/pulls",
        prs
    )

# ====================================
# STACKOVERFLOW QUESTIONS
# ====================================

questions = stack.get_questions()

loader.save_raw_data(
    "stackoverflow_raw",
    "questions",
    questions
)

# ====================================
# STACKOVERFLOW ANSWERS
# ====================================

answers = stack.get_answers()

loader.save_raw_data(
    "stackoverflow_raw",
    "answers",
    answers
)

print("EXTRAÇÃO FINALIZADA")