
import json
import base64
import pandas as pd

def generate_data(csv_path):
    df = pd.read_csv(csv_path)

    mosques = df['mosque_name'].unique()
    decades = df['decade'].unique()

    nodes = []

    for mosque in mosques:
        nodes.append({
            "id": f"mosque::" + mosque,
            "label": mosque,
            "color": "#6A50FF"
        })

    for decade in decades:
        nodes.append({
            "id": f"decade::" + str(decade),
            "label": str(decade),
            "color": "#4C4646"
        })

    links = []
    for _, row in df.iterrows():
        links.append({
            "source": f"mosque::" + row['mosque_name'],
            "target": f"decade::" + str(row['decade']),
            "event": row['what_happend']
        })

    graph_data = {
        "nodes": nodes,
        "links": links
    }

    b64_data = base64.b64encode(json.dumps(graph_data).encode('utf-8')).decode('utf-8')
    return b64_data

if __name__ == "__main__":
    path = "mosques_years_graph.csv"  # путь к вашему CSV
    print(generate_data(path))
