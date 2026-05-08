import time
from etl.utils.logger import logger


def handle_rate_limit(response):

    remaining = response.headers.get(
        "X-RateLimit-Remaining"
    )

    if remaining == "0":

        reset_time = int(
            response.headers.get(
                "X-RateLimit-Reset"
            )
        )

        sleep_time = reset_time - int(time.time())

        logger.warning(
            f"Rate limit atingido. "
            f"Aguardando {sleep_time}s"
        )

        time.sleep(max(sleep_time, 0))