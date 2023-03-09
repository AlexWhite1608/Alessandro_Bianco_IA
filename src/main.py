import Graph as Graph
from Graph import Node as Node

# CONST VALUES #
N_NODES = 25
ANIMATION = False
SYMMETRICAL = False


def main():
    graph = Graph.Graph(N_NODES, ANIMATION, SYMMETRICAL)
    print(graph)

    random_node1 = graph.get_random_node()
    print("RANDOM: ", random_node1.get_label())

    graph.generate_edges(random_node1)

    # print("FC: ", graph.backtracking("ForwardChecking"))
    print("Mac: ", graph.backtracking("Mac"))

if __name__ == "__main__":
    main()
