import requests

from etl.utils.config import GITHUB_TOKEN
from etl.utils.logger import logger
from etl.extract.rate_limit import (
    handle_rate_limit
)

BASE_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}


class GitHubExtractor:

    def search_repositories(self):

        logger.info(
            "Extraindo repositórios GitHub"
        )

        url = f"{BASE_URL}/search/repositories"

        params = {
            "q": "stars:>50000 fork:false",
            "sort": "stars",
            "order": "desc",
            "per_page": 50
        }

        response = requests.get(
            url,
            headers=HEADERS,
            params=params
        )

        handle_rate_limit(response)

        response.raise_for_status()

        return response.json()

    def get_commits(
        self,
        owner,
        repo
    ):

        logger.info(
            f"Extraindo commits: {repo}"
        )

        url = (
            f"{BASE_URL}/repos/"
            f"{owner}/{repo}/commits"
        )

        response = requests.get(
            url,
            headers=HEADERS
        )

        handle_rate_limit(response)

        response.raise_for_status()

        return response.json()

    def get_issues(
        self,
        owner,
        repo
    ):

        logger.info(
            f"Extraindo issues: {repo}"
        )

        url = (
            f"{BASE_URL}/repos/"
            f"{owner}/{repo}/issues"
        )

        response = requests.get(
            url,
            headers=HEADERS
        )

        handle_rate_limit(response)

        response.raise_for_status()

        return response.json()

    def get_pull_requests(
        self,
        owner,
        repo
    ):

        logger.info(
            f"Extraindo PRs: {repo}"
        )

        url = (
            f"{BASE_URL}/repos/"
            f"{owner}/{repo}/pulls"
        )

        response = requests.get(
            url,
            headers=HEADERS
        )

        handle_rate_limit(response)

        response.raise_for_status()

        return response.json()
    
def get_commits(
    self,
    owner,
    repo
):

    endpoint = f"/repos/{owner}/{repo}/commits"

    response = requests.get(
        f"{self.base_url}{endpoint}",
        headers=self.headers,
        params={"per_page": 100}
    )

    self.handle_rate_limit(response)

    response.raise_for_status()

    return response.json()


def get_issues(
    self,
    owner,
    repo
):

    endpoint = f"/repos/{owner}/{repo}/issues"

    response = requests.get(
        f"{self.base_url}{endpoint}",
        headers=self.headers,
        params={
            "state": "all",
            "per_page": 100
        }
    )

    self.handle_rate_limit(response)

    response.raise_for_status()

    return response.json()


def get_pull_requests(
    self,
    owner,
    repo
):

    endpoint = f"/repos/{owner}/{repo}/pulls"

    response = requests.get(
        f"{self.base_url}{endpoint}",
        headers=self.headers,
        params={
            "state": "all",
            "per_page": 100
        }
    )

    self.handle_rate_limit(response)

    response.raise_for_status()

    return response.json()