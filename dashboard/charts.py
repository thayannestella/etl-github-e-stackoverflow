import plotly.express as px


# ====================================
# TOP LANGUAGES
# ====================================

def languages_chart(df):

    fig = px.bar(
        df,
        x="language",
        y="total_repositories",
        title="Top Linguagens no GitHub",
        text_auto=True
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        title_font=dict(size=24),
        font=dict(size=14),
        xaxis_title="Linguagem",
        yaxis_title="Quantidade de Repositórios"
    )

    return fig


# ====================================
# STACKOVERFLOW TOPICS
# ====================================

def topics_chart(df):

    fig = px.bar(
        df.head(10),
        x="topic",
        y="mentions",
        title="Top Tópicos do StackOverflow",
        text_auto=True
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        title_font=dict(size=24),
        font=dict(size=14),
        xaxis_title="Tópico",
        yaxis_title="Menções"
    )

    return fig


# ====================================
# GITHUB X STACKOVERFLOW
# ====================================

def correlation_chart(df):

    # Ordenar alfabeticamente por tecnologia
    df_sorted = df.sort_values("technology").reset_index(drop=True)

    fig = px.line(
        df_sorted,
        x="technology",
        y="github_repositories",
        markers=True,
        title="Correlação: Linguagens vs Repositórios GitHub",
        height=750,
        labels={
            "technology": "Linguagem",
            "github_repositories": "Quantidade de Repositórios"
        }
    )

    # ====================================
    # MELHORIAS VISUAIS DA LINHA
    # ====================================

    fig.update_traces(
        line=dict(width=3, color="cyan"),
        marker=dict(
            size=10,
            color="white",
            line=dict(width=2, color="cyan")
        ),
        mode="lines+markers+text",
        text=df_sorted["github_repositories"],
        textposition="top center",
        textfont=dict(size=10, color="white"),
        hovertemplate="<b>%{x}</b><br>Repositórios: %{y}<extra></extra>"
    )

    # ====================================
    # LAYOUT - GRÁFICO DE LINHA
    # ====================================

    fig.update_layout(
        template="plotly_dark",
        title_font=dict(size=26, color="white"),
        font=dict(size=12),
        xaxis_title="Linguagem",
        yaxis_title="Quantidade de Repositórios",
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(128, 128, 128, 0.2)",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(128, 128, 128, 0.2)",
            zeroline=False
        ),
        margin=dict(l=80, r=80, t=100, b=100),
        hovermode="x unified"
    )

    return fig