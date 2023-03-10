import src.Graph as Graph
import src.Backtracking as BT
import matplotlib.pyplot as plt

# CONST VALUES #
N_NODES = 4
ANIMATION = False


def generate_graph(ax1_title, ax2_title, ax1_data, ax2_data):
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    ax1.set_title(ax1_title)
    ax2.set_title(ax2_title)

    for x_1, y_1 in ax1_data.items():
        ax1.plot(x_1, y_1)

    for x_2, y_2 in ax2_data.items():
        ax2.plot(x_2, y_2)

    ax1.plot(2, 4)
    ax2.plot(1, 5)
    plt.show()


# Confronta tempi per risoluzione con mappa random e mappa simmetrica
def time_performance_test():
    for i in range(2, N_NODES):
        random_graph = Graph.Graph(i, ANIMATION, False)
        sym_graph = Graph.Graph(i, ANIMATION, True)

        print("Random Graph:", random_graph)
        print("Symmetrical Graph:", sym_graph)

        starting_node_random = random_graph.get_random_node()
        starting_node_sym = sym_graph.get_random_node()

        # TODO: prendi i tempi di esecuzione dei bt!
        random_graph.generate_edges(starting_node_random)
        sym_graph.generate_edges(starting_node_sym)

        del random_graph, sym_graph

    data1 = {3: 4}
    data2 = {6: 2}

    generate_graph("Random Graph", "Symmetric Graph", data1, data2)
