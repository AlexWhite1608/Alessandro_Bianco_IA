import time
import timeit

import src.Graph as Graph
import matplotlib.pyplot as plt

# CONST VALUES #
N_NODES = 20
N_ITER = 30


# Confronta tempi per risoluzione con mappa random e mappa simmetrica
def time_performance_test():
    fc_times = []
    mac_times = []

    for n_nodes in range(1, N_NODES + 1):
        graph = Graph.Graph(N_NODES, False, False)

        graph.generate_edges(graph.get_random_node())

        start_time = time.time()
        graph.backtracking("ForwardChecking")
        fc_times.append(time.time() - start_time)

        start_time = time.time()
        graph.backtracking("Mac")
        mac_times.append(time.time() - start_time)

    plt.plot(range(1, N_NODES + 1), fc_times, label='FC')
    plt.plot(range(1, N_NODES + 1), mac_times, label='MAC')
    plt.xlabel('Number of nodes')
    plt.ylabel('Execution time (s)')
    plt.yscale('log')
    plt.title('Comparison of FC and MAC backtracking')
    plt.legend()
    plt.show()


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

# TODO: CONFRONTA TEMPI TRA COLORAZIONE K3 E K4

