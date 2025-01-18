import tkinter as tk
import numpy as np
from tkinter import simpledialog, messagebox, Toplevel,PhotoImage
import random
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fonction pour générer un graphe fortement connexe avec des poids
def generate_strongly_connected_graph_with_weights():
    num_nodes = simpledialog.askinteger("Entrée", "Entrez le nombre de sommets :", minvalue=2)
    num_edges = simpledialog.askinteger("Entrée", "Entrez le nombre d'arcs :", minvalue=num_nodes - 1)

    if not num_nodes or not num_edges:
        messagebox.showinfo("Annulé", "Données non fournies.")
        return None

    if num_edges < num_nodes - 1:
        messagebox.showerror("Erreur", "Pour un graphe fortement connexe, le nombre d'arcs doit être au moins égal à (nombre de sommets - 1).")
        return None

    # Créer un graphe orienté avec une connexion minimale entre tous les sommets
    graph = nx.DiGraph()
    graph.add_nodes_from(range(1, num_nodes + 1))

    # Connecter les sommets de manière séquentielle pour garantir la connexité
    for i in range(1, num_nodes):
        weight = random.randint(1, 10)
        graph.add_edge(i, i + 1, weight=weight)

    # Ajouter des arêtes supplémentaires si nécessaire
    additional_edges = num_edges - (num_nodes - 1)
    for _ in range(additional_edges):
        source = random.randint(1, num_nodes)
        target = random.randint(1, num_nodes)
        while source == target or graph.has_edge(source, target):
            target = random.randint(1, num_nodes)
        weight = random.randint(1, 10)
        graph.add_edge(source, target, weight=weight)

    return graph


# Fonction pour afficher un graphe avec des poids sur les arêtes
def display_graph_with_weights(graph, node_colors=None):
    if not graph:
        messagebox.showerror("Erreur", "Le graphe est vide.")
        return

    # Créer une fenêtre pour afficher le graphe
    graph_window = Toplevel(root)
    graph_window.title("Visualisation du Graphe avec Poids")
    graph_window.geometry("800x600")

    # Préparer le graphique
    fig = Figure(figsize=(7, 5), dpi=100)
    ax = fig.add_subplot(1, 1, 1)

    # Appliquer les couleurs si elles sont définies
    color_map = node_colors if node_colors else ["lightblue"] * len(graph.nodes)
    pos = nx.spring_layout(graph)  # Disposition du graphe
    nx.draw(
        graph, pos, with_labels=True, ax=ax, node_color=color_map, edge_color="black",
        node_size=800, font_color="white", font_size=10
    )

    # Ajouter les poids sur les arêtes
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)

    # Afficher le graphique
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()


def run_potentiel_metra(update_results):
    num_stores = simpledialog.askinteger("Potentiel Metra", "Entrez le nombre de magasins :")
    num_units = simpledialog.askinteger("Potentiel Metra", "Entrez le nombre d'unités :")

    if not num_stores or not num_units:
        messagebox.showinfo("Annulé", "Données non fournies.")
        return

    # Génération aléatoire des coûts et des capacités
    cost_matrix = [[random.randint(5, 20) for _ in range(num_units)] for _ in range(num_stores)]
    supply = [random.randint(20, 50) for _ in range(num_stores)]
    demand = [random.randint(20, 50) for _ in range(num_units)]

    # Calcul de la solution de base (Méthode du Potentiel Metra)
    # Cette partie est simplifiée et nécessite des étapes supplémentaires pour une vraie solution.
    result = f"Coûts de transport: {cost_matrix}\n\nCapacités d'offres: {supply}\n\nDemande: {demand}\n\n"
    result += "Calcul Potentiel Metra effectué (simulé ici). Résultats à implémenter."

    update_results(result)

# Nord-Ouest
def run_nord_ouest(update_results):
    num_stores = simpledialog.askinteger("Nord-Ouest", "Entrez le nombre de magasins :")
    num_units = simpledialog.askinteger("Nord-Ouest", "Entrez le nombre d'unités :")

    if not num_stores or not num_units:
        messagebox.showinfo("Annulé", "Données non fournies.")
        return

    # Génération des coûts et des capacités
    cost_matrix = [[random.randint(5, 20) for _ in range(num_units)] for _ in range(num_stores)]
    supply = [random.randint(20, 50) for _ in range(num_stores)]
    demand = [random.randint(20, 50) for _ in range(num_units)]

    # Appliquer la méthode du Nord-Ouest
    # Méthode de distribution Nord-Ouest (simplifiée)
    result = f"Coûts de transport: {cost_matrix}\n\nCapacités d'offres: {supply}\n\nDemande: {demand}\n\n"
    result += "Méthode du Nord-Ouest effectuée (simulée ici). Résultats à implémenter."

    update_results(result)

# Fonction Nord-Ouest
def nord_ouest_method(capacities, demands):
    allocation = np.zeros((len(capacities), len(demands)), dtype=int)
    i, j = 0, 0

    while i < len(capacities) and j < len(demands):
        quantity = min(capacities[i], demands[j])
        allocation[i, j] = quantity
        capacities[i] -= quantity
        demands[j] -= quantity

        if capacities[i] == 0:
            i += 1
        elif demands[j] == 0:
            j += 1

    return allocation

# Fonction Moindre Coût
def moindre_cout_method(capacities, demands, costs):
    allocation = np.zeros((len(capacities), len(demands)), dtype=int)
    costs_copy = costs.astype(float)

    while np.sum(capacities) > 0 and np.sum(demands) > 0:
        min_index = np.unravel_index(np.argmin(costs_copy), costs_copy.shape)
        i, j = min_index

        quantity = min(capacities[i], demands[j])
        allocation[i][j] = quantity

        capacities[i] -= quantity
        demands[j] -= quantity

        if capacities[i] == 0:
            costs_copy[i, :] = float('inf')
        if demands[j] == 0:
            costs_copy[:, j] = float('inf')

    return allocation

# Calculer le coût total d'une solution donnée
def calculer_cout_total(costs, allocation):
    return np.sum(costs * allocation)

# Fonction Stepping Stone
def stepping_stone_method(costs, allocation):
    return allocation

# Fenêtre secondaire
def open_transport_optimization():
    def apply_method():
        try:
            num_factories = int(factory_entry.get())
            num_warehouses = int(warehouse_entry.get())
            costs = np.random.randint(1, 20, size=(num_factories, num_warehouses))
            capacities = np.random.randint(10, 50, size=num_factories)
            demands = np.random.randint(10, 50, size=num_warehouses)

            if np.sum(capacities) > np.sum(demands):
                demands[-1] += np.sum(capacities) - np.sum(demands)
            elif np.sum(capacities) < np.sum(demands):
                capacities[-1] += np.sum(demands) - np.sum(capacities)

            allocation_nw = nord_ouest_method(capacities.copy(), demands.copy())
            cost_nw = calculer_cout_total(costs, allocation_nw)

            allocation_mc = moindre_cout_method(capacities.copy(), demands.copy(), costs)
            cost_mc = calculer_cout_total(costs, allocation_mc)

            allocation_optimized = stepping_stone_method(costs, allocation_mc)
            cost_optimized = calculer_cout_total(costs, allocation_optimized)

            result_text.set(
                f"Nord-Ouest Allocation:\n{allocation_nw}\n"
                f"Coût total (Nord-Ouest): {cost_nw}\n\n"
                f"Moindre Coût Allocation:\n{allocation_mc}\n"
                f"Coût total (Moindre Coût): {cost_mc}\n\n"
                f"Optimisation (Stepping Stone):\n{allocation_optimized}\n"
                f"Coût total optimisé: {cost_optimized}"
            )

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    transport_window = tk.Toplevel(root)
    transport_window.title("Optimisation Transport")

    tk.Label(transport_window, text="Nombre d'usines:").grid(row=0, column=0, padx=10, pady=5)
    factory_entry = tk.Entry(transport_window)
    factory_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(transport_window, text="Nombre de magasins:").grid(row=1, column=0, padx=10, pady=5)
    warehouse_entry = tk.Entry(transport_window)
    warehouse_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(transport_window, text="Appliquer", command=apply_method).grid(row=2, column=0, columnspan=2, pady=10)

    result_text = tk.StringVar()
    result_label = tk.Label(transport_window, textvariable=result_text, justify="left", anchor="w")
    result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
    
    
    
def welsh_powell(update_results):
    graph = generate_strongly_connected_graph_with_weights()
    if graph:
        sorted_nodes = sorted(graph.nodes(), key=lambda x: graph.degree[x], reverse=True)
        coloring = {}
        available_colors = ["red", "blue", "green", "orange", "purple", "cyan", "yellow", "pink", "brown", "gray"]

        for node in sorted_nodes:
            used_colors = {coloring[neighbor] for neighbor in graph.neighbors(node) if neighbor in coloring}
            for color in available_colors:
                if color not in used_colors:
                    coloring[node] = color
                    break

        node_colors = [coloring[node] for node in graph.nodes()]
        display_graph_with_weights(graph, node_colors=node_colors)
        
        # Mettre à jour les résultats dans la zone de texte
        result = f"Coloration des sommets réussie : {coloring}"
        update_results(result)


# Dijkstra (Plus court chemin avec chemins détaillés)
def dijkstra(update_results):
    graph = generate_strongly_connected_graph_with_weights()
    if graph:
        start = simpledialog.askinteger("Dijkstra", "Entrez le sommet de départ :", minvalue=1)
        if start:
            try:
                # Calcul des distances et des chemins depuis le sommet de départ
                lengths, paths = nx.single_source_dijkstra(graph, start)

                # Génération des couleurs pour le graphe (optionnel pour visualisation)
                node_colors = ["lightblue"] * len(graph.nodes())
                node_colors[start - 1] = "green"  # Marquer le sommet de départ en vert

                # Afficher le graphe avec les poids sur les arêtes
                display_graph_with_weights(graph, node_colors)

                # Préparer un message détaillé avec les chemins et distances
                result = f"Plus court chemin depuis le sommet {start} :\n\n"
                for node in graph.nodes():
                    path = " -> ".join(map(str, paths[node]))
                    result += f"Vers sommet {node}: Distance = {lengths[node]}, Chemin = {path}\n"

                # Afficher le résultat détaillé
                update_results(result)
            except nx.NetworkXError as e:
                messagebox.showerror("Erreur", f"Erreur dans Dijkstra : {e}")


# Kruskal (Arbre couvrant minimum)
def kruskal(update_results):
    graph = generate_strongly_connected_graph_with_weights()
    if graph:
        mst = nx.minimum_spanning_tree(graph.to_undirected(), algorithm="kruskal")
        display_graph_with_weights(mst)
        update_results(f"Arêtes de l'arbre couvrant minimum : {list(mst.edges(data=True))}")


# Bellman-Ford (Poids négatifs)
def bellman_ford(update_results):
    graph = generate_strongly_connected_graph_with_weights()
    if graph:
        start = simpledialog.askinteger("Bellman-Ford", "Entrez le sommet de départ :", minvalue=1)
        if start:
            try:
                lengths, paths = nx.single_source_bellman_ford(graph, start)
                display_graph_with_weights(graph)

                # Préparer un message détaillé avec les chemins et distances
                result = f"Distances et chemins depuis le sommet {start} :\n\n"
                for node in graph.nodes():
                    path = " -> ".join(map(str, paths[node]))
                    result += f"Vers sommet {node}: Distance = {lengths[node]}, Chemin = {path}\n"

                # Afficher le résultat détaillé
                update_results(result)
            except nx.NetworkXError as e:
                messagebox.showerror("Erreur", f"Erreur dans Bellman-Ford : {e}")


# Ford-Fulkerson (Flot maximum)
def ford_fulkerson(update_results):
    graph = generate_strongly_connected_graph_with_weights()
    if graph:
        source = simpledialog.askinteger("Ford-Fulkerson", "Entrez le sommet source :", minvalue=1)
        target = simpledialog.askinteger("Ford-Fulkerson", "Entrez le sommet cible :", minvalue=1)
        if source and target:
            try:
                flow_value, _ = nx.maximum_flow(graph, source, target)
                display_graph_with_weights(graph)
                update_results(f"Flot maximum entre {source} et {target} : {flow_value}")
            except nx.NetworkXError as e:
                messagebox.showerror("Erreur", f"Erreur dans Ford-Fulkerson : {e}")


# Interface principale
def create_main_interface():
    title = tk.Label(root, text="Interface Graphique Tkinter - Algorithmes", font=("Arial", 18, "bold"), pady=20, fg="#4B0082")
    title.pack()

    # Zone pour afficher les résultats
    result_text = tk.Text(root, height=5, width=80, font=("Arial", 12), bg="#f0f0f0", fg="#333")
    result_text.pack(padx=5, pady=10)

    def update_results(result):
        result_text.delete(1.0, tk.END)  # Effacer les anciens résultats
        result_text.insert(tk.END, result)  # Ajouter les nouveaux résultats

    # Liste des algorithmes avec bouton pour exécuter
    algorithms = [
        ("Welsh Powell (Coloration)", lambda: welsh_powell(update_results)),
        ("Dijkstra (Plus court chemin)", lambda: dijkstra(update_results)),
        ("Kruskal (Arbre minimum)", lambda: kruskal(update_results)),
        ("Bellman-Ford (Poids négatifs)", lambda: bellman_ford(update_results)),
        ("Ford-Fulkerson (Flot max)", lambda: ford_fulkerson(update_results)),
    ]

    for algo_name, algo_function in algorithms:
        btn = tk.Button(root, text=algo_name, font=("Arial", 12), command=algo_function, bg="Green", fg="white")
        btn.pack(pady=0)
    tk.Button(root, text="Ouvrir l'Optimisation Transport", command=open_transport_optimization,bg="green",fg="white", font=("Arial", 12),).pack(pady=20)
    btn_exit = tk.Button(root, text="Quitter", font=("Arial", 12), command=root.quit, bg="Purple", fg="white")
    btn_exit.pack(pady=0)
    text1 = tk.Label(root, text="Réalisé par ZOUGAGH mounsif", font=("Arial", 10, "bold"), pady=4, fg="#4B0082")
    text1.pack()
    text2 = tk.Label(root, text="Encader Par MKHALET Mouna", font=("Arial", 10, "bold"), pady=4, fg="#4B0082")
    text2.pack()


# Fenêtre principale
root = tk.Tk()
root.title("Application des Algorithmes")
root.geometry("800x600")
image = tk.PhotoImage(file="emsi.png")
image_label = tk.Label(root, image=image)
image_label.image = image  # Liaison pour éviter la suppression
image_label.pack()

create_main_interface()

root.mainloop()