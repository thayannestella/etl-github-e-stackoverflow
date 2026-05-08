import json
import pandas as pd

from etl.utils.database import engine
from etl.utils.logger import logger


class RawLoader:

    def save_raw_data(
        self,
        table_name,
        endpoint,
        payload
    ):

        logger.info(
            f"Salvando RAW: {table_name}"
        )

        df = pd.DataFrame([
            {
                "endpoint": endpoint,
                "payload": json.dumps(payload)
            }
        ])

        df.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False
        )