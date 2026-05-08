import requests

from etl.utils.logger import logger

BASE_URL = (
    "https://api.stackexchange.com/2.3"
)


class StackOverflowExtractor:

    def get_questions(self):

        logger.info(
            "Extraindo perguntas StackOverflow"
        )

        url = f"{BASE_URL}/questions"

        params = {
            "site": "stackoverflow",
            "pagesize": 100,
            "sort": "votes",
            "order": "desc"
        }

        response = requests.get(
            url,
            params=params
        )

        response.raise_for_status()

        return response.json()

    def get_answers(self):

        logger.info(
            "Extraindo respostas StackOverflow"
        )

        url = f"{BASE_URL}/answers"

        params = {
            "site": "stackoverflow",
            "pagesize": 100,
            "sort": "votes",
            "order": "desc"
        }

        response = requests.get(
            url,
            params=params
        )

        response.raise_for_status()

        return response.json()
    
def get_answers(self):

    endpoint = "/answers"

    response = requests.get(
        f"{self.base_url}{endpoint}",
        params={
            "site": "stackoverflow",
            "pagesize": 100,
            "order": "desc",
            "sort": "votes"
        }
    )

    response.raise_for_status()

    return response.json()