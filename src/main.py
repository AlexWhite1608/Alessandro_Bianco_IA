import time
from Backtracking import COLORS
import Graph as Graph
from testBT import test1

# CONST VALUES #
N_NODES = 20
ANIMATION = False
SYMMETRICAL = False


def main():
    # for i in range(1, N_NODES + 1):
    #     graph = Graph.Graph(i, ANIMATION, SYMMETRICAL)
    #     # print(graph)
    #
    #     random_node1 = graph.get_random_node()
    #     # print("RANDOM: ", random_node1.get_label())
    #
    #     graph.generate_edges(random_node1)
    #
    #     # graph.backtracking("ForwardChecking")
    #     graph.backtracking("Mac")

    # test1.test_timeit()
    # test1.comparison_k3_k4()
    test1.time_performance()


if __name__ == "__main__":
    main()
