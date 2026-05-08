import pandas as pd


class GitHubTransform:

    def repositories(self, raw_data):

        items = raw_data["items"]

        repos = []

        for repo in items:

            repos.append({
                "repo_id": repo["id"],
                "name": repo["name"],
                "owner": repo["owner"]["login"],
                "language": repo["language"]
                if repo["language"]
                else "Unknown",
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "open_issues": repo["open_issues_count"],
                "created_at": pd.to_datetime(
                    repo["created_at"]
                )
            })

        df = pd.DataFrame(repos)

        return df.drop_duplicates()

    def commits(
        self,
        commits_raw,
        repo_name
    ):

        commits = []

        for commit in commits_raw:

            if "commit" not in commit:
                continue

            commits.append({
                "sha": commit["sha"],
                "repo_name": repo_name,
                "author_name":
                    commit["commit"]["author"]["name"],
                "commit_message":
                    commit["commit"]["message"],
                "commit_date": pd.to_datetime(
                    commit["commit"]["author"]["date"]
                )
            })

        return pd.DataFrame(commits)

    def issues(
        self,
        issues_raw,
        repo_name
    ):

        issues = []

        for issue in issues_raw:

            if "pull_request" in issue:
                continue

            issues.append({
                "issue_id": issue["id"],
                "repo_name": repo_name,
                "title": issue["title"],
                "state": issue["state"],
                "created_at": pd.to_datetime(
                    issue["created_at"]
                )
            })

        return pd.DataFrame(issues)

    def pull_requests(
        self,
        prs_raw,
        repo_name
    ):

        prs = []

        for pr in prs_raw:

            prs.append({
                "pr_id": pr["id"],
                "repo_name": repo_name,
                "title": pr["title"],
                "state": pr["state"],
                "created_at": pd.to_datetime(
                    pr["created_at"]
                )
            })

        return pd.DataFrame(prs)