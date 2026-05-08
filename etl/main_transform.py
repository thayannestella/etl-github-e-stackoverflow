import pandas as pd

from etl.utils.database import engine

from etl.transform.github_transform import (
    GitHubTransform
)

from etl.transform.stackoverflow_transform import (
    StackOverflowTransform
)

from etl.load.silver_loader import (
    SilverLoader
)

github_transform = GitHubTransform()

stack_transform = StackOverflowTransform()

loader = SilverLoader()

# ====================================
# GITHUB RAW
# ====================================

github_raw = pd.read_sql(
    """
    SELECT *
    FROM github_raw
    WHERE endpoint = 'search/repositories'
    ORDER BY extracted_at DESC
    LIMIT 1
    """,
    engine
)

repos_payload = github_raw.iloc[0]["payload"]

repos_df = github_transform.repositories(
    repos_payload
)

loader.load(
    repos_df,
    "github_repositories"
)

# ====================================
# STACK QUESTIONS RAW
# ====================================

stack_raw = pd.read_sql(
    """
    SELECT *
    FROM stackoverflow_raw
    WHERE endpoint = 'questions'
    ORDER BY extracted_at DESC
    LIMIT 1
    """,
    engine
)

questions_payload = stack_raw.iloc[0]["payload"]

questions_df = stack_transform.questions(
    questions_payload
)

loader.load(
    questions_df,
    "stack_questions"
)

print("TRANSFORMAÇÃO FINALIZADA")

# ====================================
# COMMITS / ISSUES / PRS
# ====================================

for repo in repos_df.itertuples():

    repo_name = repo.name

    # COMMITS
    commits_raw = pd.read_sql(
        f"""
        SELECT *
        FROM github_raw
        WHERE endpoint = '{repo_name}/commits'
        ORDER BY extracted_at DESC
        LIMIT 1
        """,
        engine
    )

    if not commits_raw.empty:

        commits_payload = (
            commits_raw.iloc[0]["payload"]
        )

        commits_df = (
            github_transform.commits(
                commits_payload,
                repo_name
            )
        )

        loader.load(
            commits_df,
            "github_commits"
        )

    # ISSUES
    issues_raw = pd.read_sql(
        f"""
        SELECT *
        FROM github_raw
        WHERE endpoint = '{repo_name}/issues'
        ORDER BY extracted_at DESC
        LIMIT 1
        """,
        engine
    )

    if not issues_raw.empty:

        issues_payload = (
            issues_raw.iloc[0]["payload"]
        )

        issues_df = (
            github_transform.issues(
                issues_payload,
                repo_name
            )
        )

        loader.load(
            issues_df,
            "github_issues"
        )

    # PRS
    prs_raw = pd.read_sql(
        f"""
        SELECT *
        FROM github_raw
        WHERE endpoint = '{repo_name}/pulls'
        ORDER BY extracted_at DESC
        LIMIT 1
        """,
        engine
    )

    if not prs_raw.empty:

        prs_payload = prs_raw.iloc[0]["payload"]

        prs_df = (
            github_transform.pull_requests(
                prs_payload,
                repo_name
            )
        )

        loader.load(
            prs_df,
            "github_pull_requests"
        )

# ====================================
# STACK ANSWERS
# ====================================

answers_raw = pd.read_sql(
    """
    SELECT *
    FROM stackoverflow_raw
    WHERE endpoint = 'answers'
    ORDER BY extracted_at DESC
    LIMIT 1
    """,
    engine
)

answers_payload = answers_raw.iloc[0]["payload"]

answers_df = stack_transform.answers(
    answers_payload
)

loader.load(
    answers_df,
    "stack_answers"
)