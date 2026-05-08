CREATE TABLE IF NOT EXISTS top_languages (
    language TEXT,
    total_repositories INT
);

CREATE TABLE IF NOT EXISTS repo_activity (
    repo_name TEXT,
    commits_count INT,
    issues_count INT,
    pull_requests_count INT
);

CREATE TABLE IF NOT EXISTS stackoverflow_topics (
    topic TEXT,
    mentions INT
);

CREATE TABLE IF NOT EXISTS github_stackoverflow_correlation (
    technology TEXT,
    github_repositories INT,
    stackoverflow_mentions INT
);