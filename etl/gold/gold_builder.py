import pandas as pd

from dashboard.database import engine

from sqlalchemy import text


class GoldBuilder:

    # ==========================================
    # TOP 5 LINGUAGENS MAIS USADAS
    # ==========================================

    def top_languages(self):

        query = """
        SELECT
            language,
            COUNT(*) AS total_repositories
        FROM github_repositories
        WHERE language IS NOT NULL
        GROUP BY language
        ORDER BY total_repositories DESC
        LIMIT 5
        """

        df = pd.read_sql(
            query,
            engine
        )

        df.to_sql(
            "gold_top_languages",
            engine,
            if_exists="replace",
            index=False
        )

        print("TOP LANGUAGES OK")

    # ==========================================
    # ATIVIDADE DOS REPOSITÓRIOS
    # ==========================================

    def repository_activity(self):

        query = """
        SELECT
            gr.name AS repo_name,

            COUNT(DISTINCT gc.sha) AS commits_count,

            COUNT(DISTINCT gi.issue_id) AS issues_count,

            COUNT(DISTINCT gp.pr_id)
                AS pull_requests_count

        FROM github_repositories gr

        LEFT JOIN github_commits gc
            ON gr.name = gc.repo_name

        LEFT JOIN github_issues gi
            ON gr.name = gi.repo_name

        LEFT JOIN github_pull_requests gp
            ON gr.name = gp.repo_name

        GROUP BY gr.name

        ORDER BY commits_count DESC
        """

        df = pd.read_sql(
            query,
            engine
        )

        df.to_sql(
            "gold_repository_activity",
            engine,
            if_exists="replace",
            index=False
        )

        print("REPOSITORY ACTIVITY OK")

    # ==========================================
    # STACKOVERFLOW TOPICS
    # ==========================================

    def stackoverflow_topics(self):

        query = """
        SELECT
            tags,
            COUNT(*) AS total_questions,
            AVG(answer_count) AS avg_answers
        FROM stack_questions
        GROUP BY tags
        ORDER BY total_questions DESC
        LIMIT 20
        """

        df = pd.read_sql(
            query,
            engine
        )

        df.to_sql(
            "gold_stackoverflow_topics",
            engine,
            if_exists="replace",
            index=False
        )

        print("STACKOVERFLOW TOPICS OK")

    # ==========================================
    # CORRELAÇÃO GITHUB X STACKOVERFLOW
    # ==========================================

    def github_stackoverflow_correlation(self):

        query = """
        SELECT
            gr.language AS technology,

            COUNT(DISTINCT gr.repo_id)
                AS github_repositories,

            COUNT(sq.question_id)
                AS stackoverflow_mentions

        FROM github_repositories gr

        LEFT JOIN stack_questions sq
            ON LOWER(sq.tags)
            LIKE CONCAT('%', LOWER(gr.language), '%')

        WHERE gr.language IS NOT NULL

        GROUP BY gr.language

        ORDER BY stackoverflow_mentions DESC
        """

        with engine.connect() as conn:
            result = conn.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

        df.to_sql(
            "github_stackoverflow_correlation",
            engine,
            if_exists="replace",
            index=False
        )

        print("CORRELATION OK")