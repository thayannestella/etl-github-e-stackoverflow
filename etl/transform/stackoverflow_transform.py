import pandas as pd


class StackOverflowTransform:

    def questions(self, raw_data):

        questions = []

        for question in raw_data["items"]:

            questions.append({
                "question_id":
                    question["question_id"],

                "title":
                    question["title"],

                "tags":
                    ",".join(question["tags"]),

                "answer_count":
                    question["answer_count"],

                "score":
                    question["score"],

                "creation_date":
                    pd.to_datetime(
                        question["creation_date"],
                        unit="s"
                    )
            })

        return pd.DataFrame(questions)

    def answers(self, raw_data):

        answers = []

        for answer in raw_data["items"]:

            answers.append({
                "answer_id":
                    answer["answer_id"],

                "question_id":
                    answer["question_id"],

                "score":
                    answer["score"],

                "creation_date":
                    pd.to_datetime(
                        answer["creation_date"],
                        unit="s"
                    )
            })

        return pd.DataFrame(answers)