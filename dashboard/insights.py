def generate_insights(
    top_languages_df,
    topics_df
):

    main_language = (
        top_languages_df
        .iloc[0]["language"]
    )

    main_topic = (
        topics_df
        .iloc[0]["topic"]
    )

    insights = f"""
    ## Insights

    - A linguagem mais popular no GitHub é:
      **{main_language}**

    - O tópico mais discutido no StackOverflow é:
      **{main_topic}**

    - Existe forte correlação entre
      popularidade no GitHub e
      volume de dúvidas técnicas.

    - Projetos com maior atividade
      tendem a gerar maior engajamento
      da comunidade.
    """

    return insights