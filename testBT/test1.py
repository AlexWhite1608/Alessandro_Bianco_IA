import timeit

import pandas as pd
from matplotlib.ticker import MaxNLocator

import src.Graph as Graph
import matplotlib.pyplot as plt
from src.Backtracking import COLORS

# CONST VALUES #
N_NODES = 50
N_ITER = 20


def comparison_k3_k4():
    times_FC_k3, times_MAC_k3 = list(), list()
    times_FC_k4, times_MAC_k4 = list(), list()

    # TEMPI K3
    for n in range(1, N_NODES + 1):
        graph = Graph.Graph(n, False, False)
        starting_node = graph.get_random_node()
        graph.generate_edges(starting_node)

        time_FC = timeit.timeit(lambda: graph.backtracking("ForwardChecking"), number=1)
        time_MAC = timeit.timeit(lambda: graph.backtracking("Mac"), number=1)

        times_FC_k3.append(time_FC * 1000)
        times_MAC_k3.append(time_MAC * 1000)

        del graph

    # TEMPI K4
    COLORS.add('yellow')

    for n in range(1, N_NODES + 1):
        graph = Graph.Graph(n, False, False)
        starting_node = graph.get_random_node()
        graph.generate_edges(starting_node)

        time_FC = timeit.timeit(lambda: graph.backtracking("ForwardChecking"), number=1)
        time_MAC = timeit.timeit(lambda: graph.backtracking("Mac"), number=1)

        times_FC_k4.append(time_FC * 1000)
        times_MAC_k4.append(time_MAC * 1000)

        del graph

    pd.set_option('display.max_columns', None)
    print(pd.DataFrame({'Nodes': range(1, N_NODES + 1), 'K3 FC time': times_FC_k3, 'K3 MAC time': times_MAC_k3,
                        'K4 FC time': times_FC_k4, 'K4 MAC time': times_MAC_k4}))

    # Grafico per k3
    fig, ax = plt.subplots()
    ax.plot(range(1, N_NODES + 1), times_FC_k3, label="Forward Checking")
    ax.plot(range(1, N_NODES + 1), times_MAC_k3, label="Mac")
    ax.set_title(f"K3 Graph Performance ({N_NODES} Nodes)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Average Execution Time (ms)")

    if N_NODES <= 30:
        ax.set_xticks(range(1, N_NODES + 1, 2))
    elif 30 <= N_NODES <= 50:
        ax.set_xticks(range(1, N_NODES + 1, 5))
    elif N_NODES >= 100:
        ax.set_xticks(range(1, N_NODES + 1, 10))

    ax.legend()
    ax.set_yscale('log')
    plt.tight_layout()
    plt.show()

    # Grafico per k4
    fig, ax = plt.subplots()
    ax.plot(range(1, N_NODES + 1), times_FC_k4, label="Forward Checking")
    ax.plot(range(1, N_NODES + 1), times_MAC_k4, label="Mac")
    ax.set_title(f"K4 Graph Performance ({N_NODES} Nodes)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Average Execution Time (ms)")

    if N_NODES <= 30:
        ax.set_xticks(range(1, N_NODES + 1, 2))
    elif 30 <= N_NODES <= 50:
        ax.set_xticks(range(1, N_NODES + 1, 5))
    elif N_NODES >= 100:
        ax.set_xticks(range(1, N_NODES + 1, 10))

    ax.legend()
    ax.set_yscale('log')
    plt.tight_layout()
    plt.show()


def test_failed_assignment():
    fails_FC_k3, fails_FC_k4 = [], []
    fails_MAC_k3, fails_MAC_k4 = [], []

    for j in range(1, N_NODES + 1, 5):
        counter_fc_k3, counter_mac_k3 = 0, 0
        counter_fc_k4, counter_mac_k4 = 0, 0

        for n in range(1, N_ITER + 1):
            graph = Graph.Graph(j, False, False)
            starting_node = graph.get_random_node()
            graph.generate_edges(starting_node)

            if graph.backtracking("ForwardChecking") == False:
                counter_fc_k3 += 1

            if graph.backtracking("Mac") == False:
                counter_mac_k3 += 1

        # TEMPI K4
        COLORS.add('yellow')

        for n in range(1, N_ITER + 1):
            graph = Graph.Graph(j, False, False)
            starting_node = graph.get_random_node()
            graph.generate_edges(starting_node)

            if graph.backtracking("ForwardChecking") == False:
                counter_fc_k4 += 1

            if graph.backtracking("Mac") == False:
                counter_mac_k4 += 1

        fails_FC_k3.append(counter_fc_k3)
        fails_MAC_k3.append(counter_mac_k3)
        fails_FC_k4.append(counter_fc_k4)
        fails_MAC_k4.append(counter_mac_k4)

    print("Fallimenti FC k3: ", fails_FC_k3)
    print("Fallimenti MAC k3: ", fails_MAC_k3)
    print("Fallimenti FC k4: ", fails_FC_k4)
    print("Fallimenti MAC k4: ", fails_MAC_k4)

    # Grafico per k3
    fig, ax = plt.subplots()
    ax.plot(range(1, N_NODES + 1, 5), fails_FC_k3, label="Forward Checking")
    ax.plot(range(1, N_NODES + 1, 5), fails_MAC_k3, label="Mac")
    ax.set_title(f"K3 failed assignments ({N_NODES} Nodes, {N_ITER} Iterations)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Number of failed assignments")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax.legend()
    plt.tight_layout()
    plt.show()

    # Grafico per k4
    fig, ax = plt.subplots()
    ax.plot(range(1, N_NODES + 1, 5), fails_FC_k4, label="Forward Checking")
    ax.plot(range(1, N_NODES + 1, 5), fails_MAC_k4, label="Mac")
    ax.set_title(f"K4 failed assignments ({N_NODES} Nodes, {N_ITER} Iterations)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Number of failed assignments")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax.legend()
    plt.tight_layout()
    plt.show()


def test_graph_visualization(n_nodes, animate, symmetrical, bt_type):
    graph = Graph.Graph(n_nodes, animate, symmetrical)
    print(graph)

    random_node1 = graph.get_random_node()
    print("Starting node: ", random_node1.get_label())

    graph.generate_edges(random_node1)
    graph.visualize()

    if not graph.backtracking(bt_type):
        print(f"There is no solution with 3 colors using {bt_type}")

