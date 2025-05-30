from flask import Flask, render_template, request
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def is_externally_stable(graph, subset):
    n = len(graph)
    subset_set = set(subset)
    for v in range(n):
        if v not in subset_set:
            if not any(graph[v][u] == 1 for u in subset_set):
                return False
    return True

def find_minimal_externally_stable_sets(graph):
    n = len(graph)
    all_vertices = list(range(n))
    min_size = n + 1
    result = []

    for r in range(1, n + 1):
        for subset in itertools.combinations(all_vertices, r):
            if is_externally_stable(graph, subset):
                if len(subset) < min_size:
                    min_size = len(subset)
                    result = [subset]
                elif len(subset) == min_size:
                    result.append(subset)
        if result:
            break
    return result

def draw_graph_image(matrix):
    G = nx.DiGraph()
    size = len(matrix)
    for i in range(size):
        G.add_node(f'v{i+1}')
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == 1:
                G.add_edge(f'v{i+1}', f'v{j+1}')

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(3.5, 3.5))  # Уменьшено с ~5x5
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=600,
            font_size=10, arrows=True, ax=ax)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=120)  # Можно выше DPI для четкости
    plt.close()
    img.seek(0)
    return base64.b64encode(img.read()).decode('utf-8')


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    size = None
    matrix_data = ''
    image_data = None
    if request.method == 'POST':
        size = int(request.form['size'])
        matrix_input = request.form['matrix']
        matrix_data = matrix_input
        rows = matrix_input.strip().split('\n')
        matrix = [list(map(int, row.strip().split())) for row in rows]
        subsets = find_minimal_externally_stable_sets(matrix)

        result = []

        def subscript(n):
            subs = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
            return str(n).translate(subs)

        for subset in subsets:
            label = ', '.join([f"v{subscript(v + 1)}" for v in subset])
            mapped = ', '.join([f"y{subscript(v + 1)}" for v in subset])
            result.append(f"{{{label}}} соответствует {{{mapped}}}")

        image_data = draw_graph_image(matrix)
    return render_template('index.html', result=result, size=size, matrix_data=matrix_data, image_data=image_data)

if __name__ == '__main__':
    app.run(debug=True)
