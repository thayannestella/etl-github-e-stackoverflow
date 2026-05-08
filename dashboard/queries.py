import pandas as pd

from database import engine

def get_top_languages():

    return pd.read_sql(
        "SELECT * FROM top_languages",
        engine
    )


def get_repo_activity():

    return pd.read_sql(
        "SELECT * FROM repo_activity",
        engine
    )


def get_stackoverflow_topics():

    return pd.read_sql(
        "SELECT * FROM stackoverflow_topics",
        engine
    )


def get_correlation():

    return pd.read_sql(
        """
        SELECT *
        FROM github_stackoverflow_correlation
        """,
        engine
    )