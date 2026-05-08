import pandas as pd


class GoldTransform:

    # ====================================
    # TOP LANGUAGES
    # ====================================

    def top_languages(
        self,
        repositories_df
    ):

        result = (
            repositories_df
            .groupby("language")
            .size()
            .reset_index(name="total_repositories")
            .sort_values(
                "total_repositories",
                ascending=False
            )
            .head(5)
        )

        return result

    # ====================================
    # REPOSITORY ACTIVITY
    # ====================================

    def repo_activity(
        self,
        commits_df,
        issues_df,
        prs_df
    ):

        commits = (
            commits_df
            .groupby("repo_name")
            .size()
            .reset_index(name="commits_count")
        )

        issues = (
            issues_df
            .groupby("repo_name")
            .size()
            .reset_index(name="issues_count")
        )

        prs = (
            prs_df
            .groupby("repo_name")
            .size()
            .reset_index(name="pull_requests_count")
        )

        activity = commits.merge(
            issues,
            on="repo_name",
            how="outer"
        )

        activity = activity.merge(
            prs,
            on="repo_name",
            how="outer"
        )

        activity = activity.fillna(0)

        return activity

    # ====================================
    # STACKOVERFLOW TOPICS
    # ====================================

    def stackoverflow_topics(
        self,
        questions_df
    ):

        tags_series = (
            questions_df["tags"]
            .str.split(",")
            .explode()
        )

        topics = (
            tags_series
            .value_counts()
            .reset_index()
        )

        topics.columns = [
            "topic",
            "mentions"
        ]

        return topics.head(20)

    # ====================================
    # GITHUB x STACKOVERFLOW
    # ====================================

    def github_stackoverflow_correlation(
        self,
        repositories_df,
        questions_df
    ):

        github_languages = (
            repositories_df["language"]
            .value_counts()
            .reset_index()
        )

        github_languages.columns = [
            "technology",
            "github_repositories"
        ]

        tags_series = (
            questions_df["tags"]
            .str.split(",")
            .explode()
        )

        stack_tags = (
            tags_series
            .value_counts()
            .reset_index()
        )

        stack_tags.columns = [
            "technology",
            "stackoverflow_mentions"
        ]

        correlation = github_languages.merge(
            stack_tags,
            on="technology",
            how="inner"
        )

        return correlation