import time

import src.Graph as Graph
import matplotlib.pyplot as plt

# CONST VALUES #
N_NODES = 30


# TODO: FAI CON 4 COLORI!!!!
# Confronta tempi per risoluzione con mappa random e mappa simmetrica
def time_performance_test():
    ran_FC_data, sym_FC_data = [], []
    ran_MAC_data, sym_MAC_data = [], []

    for i in range(2, N_NODES):
        random_graph = Graph.Graph(i, False, False)
        sym_graph = Graph.Graph(i, False, True)

        starting_node_random = random_graph.get_random_node()
        starting_node_sym = sym_graph.get_random_node()

        random_graph.generate_edges(starting_node_random)
        sym_graph.generate_edges(starting_node_sym)

        ran_FC_time = random_graph_FC(random_graph)
        ran_MAC_time = random_graph_MAC(random_graph)
        sym_FC_time = sym_graph_FC(sym_graph)
        sym_MAC_time = sym_graph_MAC(sym_graph)

        ran_FC_data.append((i, ran_FC_time))
        ran_MAC_data.append((i, ran_MAC_time))
        sym_FC_data.append((i, sym_FC_time))
        sym_MAC_data.append((i, sym_MAC_time))

        del random_graph, sym_graph

    # Grafico per i grafi random
    fig, ax = plt.subplots()
    ax.plot([x[0] for x in ran_FC_data], [x[1] for x in ran_FC_data], label="Forward Checking")
    ax.plot([x[0] for x in ran_MAC_data], [x[1] for x in ran_MAC_data], label="MAC")
    ax.set_title("Random Graph Performance")
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Execution time (ms)")
    ax.legend()
    plt.show()

    # Grafico per i grafi simmetrici
    fig, ax = plt.subplots()
    ax.plot([x[0] for x in sym_FC_data], [x[1] for x in sym_FC_data], label="Forward Checking")
    ax.plot([x[0] for x in sym_MAC_data], [x[1] for x in sym_MAC_data], label="MAC")
    ax.set_title("Symmetric Graph Performance")
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Execution time (ms)")
    ax.legend()
    plt.show()


def random_graph_FC(graph):
    start_time = time.time()
    graph.backtracking("ForwardChecking")
    end_time = time.time()

    return end_time - start_time


def random_graph_MAC(graph):
    start_time = time.time()
    graph.backtracking("Mac")
    end_time = time.time()

    return end_time - start_time


def sym_graph_FC(graph):
    start_time = time.time()
    graph.backtracking("ForwardChecking")
    end_time = time.time()

    return end_time - start_time


def sym_graph_MAC(graph):
    start_time = time.time()
    graph.backtracking("Mac")
    end_time = time.time()

    return end_time - start_time
