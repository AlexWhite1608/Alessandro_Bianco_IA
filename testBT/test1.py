import time
import timeit
import pandas as pd
import src.Graph as Graph
import matplotlib.pyplot as plt
from src.Backtracking import COLORS

# CONST VALUES #
N_NODES = 15
N_ITER = 50


# Confronta tempi per risoluzione con mappa random e mappa simmetrica


def test_timeit():
    # testo l'esecuzione dei due algoritmi N volte su un grafo random e su uno simmetrico facendo variare magari il numero di nodi

    random_graph = Graph.Graph(N_NODES, False, False)
    sym_graph = Graph.Graph(N_NODES, False, True)

    starting_node_random = random_graph.get_random_node()
    starting_node_sym = sym_graph.get_random_node()

    random_graph.generate_edges(starting_node_random)
    sym_graph.generate_edges(starting_node_sym)

    random_graph_times_FC, sym_graph_times_FC = list(), list()
    random_graph_times_MAC, sym_graph_times_MAC = list(), list()

    avg_time_random_FC, avg_time_sym_FC = list(), list()
    avg_time_random_MAC, avg_time_sym_MAC = list(), list()

    for n in range(1, N_NODES + 1):
        for i in range(1, N_ITER + 1):
            random_graph_times_FC.append(timeit.timeit(lambda: random_graph.backtracking("ForwardChecking"), number=1) * 1000)
            sym_graph_times_FC.append(timeit.timeit(lambda: sym_graph.backtracking("ForwardChecking"), number=1) * 1000)

            random_graph_times_MAC.append(timeit.timeit(lambda: random_graph.backtracking("Mac"), number=1) * 1000)
            sym_graph_times_MAC.append(timeit.timeit(lambda: sym_graph.backtracking("Mac"), number=1) * 1000)

        avg_time_random_FC.append(calculate_average(random_graph_times_FC))
        avg_time_sym_FC.append(calculate_average(sym_graph_times_FC))
        avg_time_random_MAC.append(calculate_average(random_graph_times_MAC))
        avg_time_sym_MAC.append(calculate_average(sym_graph_times_MAC))

    print("Random FC: ", avg_time_random_FC)
    print("Sym FC: ", avg_time_sym_FC)
    print("Random MAC: ", avg_time_random_MAC)
    print("Sym MAC: ", avg_time_sym_MAC)

    pd.set_option('display.max_columns', None)
    print(pd.DataFrame({'Nodes': range(1, N_NODES+1), 'Ran FC time': avg_time_random_FC, 'Ran MAC time': avg_time_random_MAC,
                        'Sym FC time': avg_time_sym_FC, 'Sym MAC time': avg_time_sym_MAC}))

    # Grafico per i grafi random
    fig, ax = plt.subplots()
    ax.plot(range(1, N_NODES + 1), avg_time_random_FC, label="Forward Checking")
    ax.plot(range(1, N_NODES + 1), avg_time_random_MAC, label="Mac")
    ax.set_title(f"Random Graph Performance ({N_NODES} Nodes, {N_ITER} Iterations)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Average Execution Time (ms)")
    ax.set_yscale('log')
    ax.set_xticks(range(1, N_NODES + 1))
    ax.legend()
    plt.tight_layout()
    plt.show()

    # Grafico per i grafi sìmmetrici
    fig, ax = plt.subplots()
    ax.plot(range(1, N_NODES + 1), avg_time_sym_FC, label="Forward Checking")
    ax.plot(range(1, N_NODES + 1), avg_time_sym_MAC, label="Mac")
    ax.set_title(f"Symmetric Graph Performance ({N_NODES} Nodes, {N_ITER} Iterations)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Average Execution Time (ms)")
    ax.set_yscale('log')
    ax.set_xticks(range(1, N_NODES + 1))
    ax.legend()
    plt.tight_layout()
    plt.show()


def calculate_average(times):
    total = 0
    count = 0
    for num in times:
        total += num
        count += 1
    average = total / count
    return round(average, 3)


def comparison_k3_k4():
    graph = Graph.Graph(N_NODES, False, False)

    starting_node = graph.get_random_node()

    graph.generate_edges(starting_node)

    times_FC_k3, times_MAC_k3 = list(), list()
    times_FC_k4, times_MAC_k4 = list(), list()

    avg_times_FC_k3, avg_times_MAC_k3 = list(), list()
    avg_times_FC_k4, avg_times_MAC_k4 = list(), list()

    # TEMPI K3
    for n in range(1, N_NODES + 1):
        for i in range(1, N_ITER + 1):
            times_FC_k3.append(timeit.timeit(lambda: graph.backtracking("ForwardChecking"), number=1) * 1000)
            times_MAC_k3.append(timeit.timeit(lambda: graph.backtracking("Mac"), number=1) * 1000)

        avg_times_FC_k3.append(calculate_average(times_FC_k3))
        avg_times_MAC_k3.append(calculate_average(times_MAC_k3))

    # TEMPI K4
    COLORS.add('yellow')

    for n in range(1, N_NODES + 1):
        for i in range(1, N_ITER + 1):
            times_FC_k4.append(timeit.timeit(lambda: graph.backtracking("ForwardChecking"), number=1) * 1000)
            times_MAC_k4.append(timeit.timeit(lambda: graph.backtracking("Mac"), number=1) * 1000)

        avg_times_FC_k4.append(calculate_average(times_FC_k4))
        avg_times_MAC_k4.append(calculate_average(times_MAC_k4))

    # print("Random FC: ", avg_time_random_FC)
    # print("Sym FC: ", avg_time_sym_FC)
    # print("Random MAC: ", avg_time_random_MAC)
    # print("Sym MAC: ", avg_time_sym_MAC)

    pd.set_option('display.max_columns', None)
    print(pd.DataFrame({'Nodes': range(1, N_NODES+1), 'K3 FC time': avg_times_FC_k3, 'K3 MAC time': avg_times_MAC_k3,
                        'K4 FC time': avg_times_FC_k4, 'K4 MAC time': avg_times_MAC_k4}))

    # Grafico per k3
    fig, ax = plt.subplots()
    ax.plot(range(1, N_NODES + 1), avg_times_FC_k3, label="Forward Checking")
    ax.plot(range(1, N_NODES + 1), avg_times_MAC_k3, label="Mac")
    ax.set_title(f"K3 Graph Performance ({N_NODES} Nodes, {N_ITER} Iterations)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Average Execution Time (ms)")
    ax.set_xticks(range(1, N_NODES + 1))
    ax.legend()
    plt.tight_layout()
    plt.show()

    # Grafico per k4
    fig, ax = plt.subplots()
    ax.plot(range(1, N_NODES + 1), avg_times_FC_k4, label="Forward Checking")
    ax.plot(range(1, N_NODES + 1), avg_times_MAC_k4, label="Mac")
    ax.set_title(f"K4 Graph Performance ({N_NODES} Nodes, {N_ITER} Iterations)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Average Execution Time (ms)")
    ax.set_xticks(range(1, N_NODES + 1))
    ax.legend()
    plt.tight_layout()
    plt.show()

# TODO: confronta il numero di fallimenti dei due algoritmi all'aumentare del numero dei nodi in relazione alle iterazioni
#       cioè esegui N_ITER volte il codice e vedi quante volte ha fallito


