import timeit
import pandas as pd
from matplotlib.ticker import MaxNLocator
import src.Graph as Graph
import matplotlib.pyplot as plt
from src.Backtracking import COLORS

# CONST VALUES #
N_NODES = 80
N_ITER = 20


def comparison_k3_k4():
    """

    in this test a comparison is made on the execution times of the two backtracking algorithms both when you have
    3 colors available for assignment (k3), and when you have 4 (k4). It generates N_NODES graph and it measures the
    execution time with time.timeit()

    """

    times_FC_k3, times_MAC_k3 = list(), list()

    for n in range(1, N_NODES + 1):
        graph = Graph.Graph(n)
        starting_node = graph.get_random_node()
        graph.generate_edges(starting_node)

        time_FC = timeit.timeit(lambda: graph.backtracking("ForwardChecking", animate=False), number=1)
        time_MAC = timeit.timeit(lambda: graph.backtracking("Mac", animate=False), number=1)

        times_FC_k3.append(time_FC * 1000)
        times_MAC_k3.append(time_MAC * 1000)

        del graph

    fig, ax = plt.subplots()
    ax.plot(range(1, N_NODES + 1), times_FC_k3, label="Forward Checking")
    ax.plot(range(1, N_NODES + 1), times_MAC_k3, label="Mac")
    ax.set_title("K" + str(len(COLORS)) + f" Graph Performance ({N_NODES} Nodes)")
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
    """

    In this test the number of assignments failed by the two algorithms is measured both for k3 and k4 colors.
    Several graph instances are generated, each with an increasing number of nodes N_NODES. Subsequently,
    the process of creating the graph is iterated N_ITER times, and it is verified how many times the assignment
    of colors to the nodes is not possible

    """

    fails_FC_k3 = []
    fails_MAC_k3 = []

    for j in range(1, N_NODES + 1, 5):
        counter_fc_k3, counter_mac_k3 = 0, 0

        for n in range(1, N_ITER + 1):
            graph = Graph.Graph(j)
            starting_node = graph.get_random_node()
            graph.generate_edges(starting_node)

            if graph.backtracking("ForwardChecking", animate=False) == False:
                counter_fc_k3 += 1

            if graph.backtracking("Mac", animate=False) == False:
                counter_mac_k3 += 1

        fails_FC_k3.append(counter_fc_k3)
        fails_MAC_k3.append(counter_mac_k3)

    print("Fallimenti FC: ", fails_FC_k3)
    print("Fallimenti MAC: ", fails_MAC_k3)

    fig, ax = plt.subplots()
    ax.plot(range(1, N_NODES + 1, 5), fails_FC_k3, label="Forward Checking")
    ax.plot(range(1, N_NODES + 1, 5), fails_MAC_k3, label="Mac")
    ax.set_title("K" + str(len(COLORS)) + f" failed assignments ({N_NODES} Nodes, {N_ITER} Iterations)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Number of failed assignments")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax.legend()
    plt.tight_layout()
    plt.show()


def test_graph_visualization(n_nodes, bt_type):
    """

    This test is used to visualize the construction of the graph and the consequent application
    of the two different backtracking algorithms. If no solution is found by the algorithms, prints an error
    on the console

    :param n_nodes: (int) Number of nodes of the graph
    :param bt_type: (String) ForwardChecking or Mac

    """

    graph = Graph.Graph(n_nodes)
    print(graph)

    random_node1 = graph.get_random_node()
    print("Starting node: ", random_node1.get_label())

    graph.generate_edges(random_node1)
    graph.visualize()

    if not graph.backtracking(bt_type, animate=True):
        print(f"There is no solution with 3 colors using {bt_type}")
