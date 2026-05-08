import streamlit as st
import plotly.express as px


from queries import (
    get_top_languages,
    get_repo_activity,
    get_stackoverflow_topics,
    get_correlation
)

from charts import (
    languages_chart,
    topics_chart,
    correlation_chart
)

from insights import (
   generate_insights
)

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="GitHub & StackOverflow ETL",
    layout="wide"
)

# ====================================
# TITLE
# ====================================

st.title(
    "GitHub & StackOverflow ETL"
)

# ====================================
# LOAD DATA
# ====================================

top_languages = get_top_languages()

repo_activity = get_repo_activity()

topics = get_stackoverflow_topics()

correlation = get_correlation()

# ====================================
# KPIs
# ====================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Top Linguagens",
        top_languages.iloc[0]["language"]
    )

with col2:

    st.metric(
        "Top Topicos",
        topics.iloc[0]["topic"]
    )

with col3:

    st.metric(
        "Tecnologias Correlacionadas",
        len(correlation)
    )

# ====================================
# CHARTS
# ====================================

st.plotly_chart(
    languages_chart(top_languages),
    use_container_width=True
)

st.plotly_chart(
    topics_chart(topics),
    use_container_width=True
)

st.plotly_chart(
    correlation_chart(correlation),
    use_container_width=True
)

# ====================================
# TABLES
# ====================================

st.subheader(
    "Atividade dos Repositórios"
)

st.dataframe(repo_activity)

# ====================================
# INSIGHTS
# ====================================

st.markdown(
    generate_insights(
        top_languages,
        topics
    )
)