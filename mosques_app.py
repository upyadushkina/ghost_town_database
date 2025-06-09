import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import base64

# === Цветовая схема ===
PAGE_BG_COLOR = "#262123"
PAGE_TEXT_COLOR = "#E8DED3"
GRAPH_BG_COLOR = "#262123"
GRAPH_LABEL_COLOR = "#E8DED3"
EDGE_COLOR = "#322C2E"
HIGHLIGHT_EDGE_COLOR = "#6A50FF"
TEXT_FONT = "Lexend"
POPUP_BG_COLOR = "#262123"
POPUP_TEXT_COLOR = "#E8DED3"

# === Настройка страницы ===
st.set_page_config(page_title="Mosques Graph", layout="wide")
st.markdown(f"""
  <style>
    html, body, .stApp {{
      background-color: {PAGE_BG_COLOR} !important;
      color: {PAGE_TEXT_COLOR} !important;
      font-family: '{TEXT_FONT}', sans-serif;
    }}
    header, footer {{
      background-color: {PAGE_BG_COLOR} !important;
    }}
  </style>
""", unsafe_allow_html=True)

# === Загрузка и обработка CSV ===
df = pd.read_csv("mosques_years_graph.csv")
df.fillna('', inplace=True)

nodes = []
links = []
node_ids = set()

def add_node(node_id, label, color):
    if node_id not in node_ids:
        nodes.append({
            "id": node_id,
            "label": label,
            "color": color
        })
        node_ids.add(node_id)

# === Построение графа ===
for _, row in df.iterrows():
    mosque_id = f"mosque::{row['mosque_name']}"
    decade_id = f"decade::{row['decade']}"

    add_node(mosque_id, row['mosque_name'], "#6A50FF")
    add_node(decade_id, str(row['decade']), "#4C4646")

    links.append({
        "source": mosque_id,
        "target": decade_id,
        "event": row['what_happend']
    })

graph_data = {
    "nodes": nodes,
    "links": links
}

# === Кодирование данных в base64 и внедрение в шаблон ===
d3_json = json.dumps(graph_data)
b64_data = base64.b64encode(d3_json.encode("utf-8")).decode("utf-8")

with open("graph_template.html", "r", encoding="utf-8") as f:
    html_template = f.read()

html_filled = html_template.replace("{{ b64_data }}", b64_data)
html_filled = html_filled.replace("{{ popup_bg }}", POPUP_BG_COLOR)
html_filled = html_filled.replace("{{ popup_text }}", POPUP_TEXT_COLOR)

# === Встраивание HTML-графа ===
components.html(html_filled, height=1400, scrolling=False)
