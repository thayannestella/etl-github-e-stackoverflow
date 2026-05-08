from etl.utils.database import engine


class GoldLoader:

    def load(
        self,
        dataframe,
        table_name
    ):

        dataframe.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )