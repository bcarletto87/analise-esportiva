import requests
import streamlit as st

st.set_page_config(page_title="Análise Esportiva", layout="centered")

st.title("📊 Análise Esportiva Gratuita")
st.caption("Dados de fontes públicas. Conteúdo educacional.")

st.warning(
    "Aviso: este site tem fins informativos e educacionais. "
    "Não é recomendação financeira nem garantia de resultados."
)

aba = st.tabs(["🏀 NBA (balldontlie)", "⚽ Futebol (OpenLigaDB)"])

# =========================
# NBA - API balldontlie
# =========================
with aba[0]:
    st.subheader("NBA — Jogos recentes")
    team_id = st.number_input(
        "ID do time (ex.: 14 costuma ser Lakers em exemplos)",
        min_value=1,
        value=14
    )
    jogos_qtd = st.slider("Quantidade de jogos", 1, 15, 5)

    if st.button("Analisar NBA"):
        url = "https://www.balldontlie.io/api/v1/games"
        params = {"team_ids[]": team_id, "per_page": jogos_qtd}

        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        jogos = r.json().get("data", [])

        if not jogos:
            st.info("Nenhum jogo encontrado.")
        else:
            pontos_pro = []
            pontos_contra = []
            vitorias = 0

            for j in jogos:
                if j["home_team"]["id"] == team_id:
                    pf = j["home_team_score"]
                    ps = j["visitor_team_score"]
                else:
                    pf = j["visitor_team_score"]
                    ps = j["home_team_score"]

                pontos_pro.append(pf)
                pontos_contra.append(ps)
                if pf > ps:
                    vitorias += 1

            st.write(f"**Jogos analisados:** {len(jogos)}")
            st.write(f"**Vitórias:** {vitorias}")
            st.write(f"**Derrotas:** {len(jogos) - vitorias}")
            st.write(f"**Média pontos feitos:** {sum(pontos_pro)/len(pontos_pro):.1f}")
            st.write(f"**Média pontos sofridos:** {sum(pontos_contra)/len(pontos_contra):.1f}")

            st.markdown("### Leitura responsável")
            st.write(
                "- Médias refletem apenas a amostra analisada.\n"
                "- Lesões, calendário e força do adversário não estão considerados.\n"
                "- Use como informação, não como previsão."
            )

# =========================
# Futebol - OpenLigaDB
# =========================
with aba[1]:
    st.subheader("Futebol — Bundesliga (OpenLigaDB)")
    temporada = st.number_input("Temporada (ex.: 2024)", min_value=2000, value=2024)
    rodada = st.number_input("Rodada", min_value=1, value=1)

    if st.button("Analisar Futebol"):
        url = f"https://www.openligadb.de/api/getmatchdata/bl1/{temporada}/{rodada}"
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        jogos = r.json()

        if not jogos:
            st.info("Nenhum jogo encontrado.")
        else:
            gols = []
            for j in jogos:
                t1 = j["Team1"]["TeamName"]
                t2 = j["Team2"]["TeamName"]
                res = j.get("MatchResults", [])

                if res:
                    final = res[-1]
                    g1 = final["PointsTeam1"]
                    g2 = final["PointsTeam2"]
                    gols.append(g1 + g2)
                    st.write(f"- {t1} {g1} x {g2} {t2}")
                else:
                    st.write(f"- {t1} vs {t2} (sem resultado)")

            if gols:
                st.write(f"**Média de gols da rodada:** {sum(gols)/len(gols):.2f}")

            st.markdown("### Observação")
            st.write(
                "- Esta fonte não fornece xG.\n"
                "- A análise usa apenas placares e contexto básico."
            )
