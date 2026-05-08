CREATE TABLE IF NOT EXISTS github_repositories (
    repo_id BIGINT PRIMARY KEY,
    name TEXT,
    owner TEXT,
    language TEXT,
    stars INT,
    forks INT,
    open_issues INT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS github_commits (
    sha TEXT PRIMARY KEY,
    repo_name TEXT,
    author_name TEXT,
    commit_message TEXT,
    commit_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS github_issues (
    issue_id BIGINT PRIMARY KEY,
    repo_name TEXT,
    title TEXT,
    state TEXT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS github_pull_requests (
    pr_id BIGINT PRIMARY KEY,
    repo_name TEXT,
    title TEXT,
    state TEXT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stack_questions (
    question_id BIGINT PRIMARY KEY,
    title TEXT,
    tags TEXT,
    answer_count INT,
    score INT,
    creation_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stack_answers (
    answer_id BIGINT PRIMARY KEY,
    question_id BIGINT,
    score INT,
    creation_date TIMESTAMP
);