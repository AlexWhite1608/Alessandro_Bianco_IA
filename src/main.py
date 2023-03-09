from Graph import Graph as Graph
from Graph import Node as Node

# CONST VALUES #
N_NODES = 5
ANIMATION = True


def main():
    graph = Graph(N_NODES, ANIMATION)
    print(graph)

    random_node1 = graph.get_random_node()
    print("RANDOM: ", random_node1.get_label())

    graph.generate_edges(random_node1)

    # print("FC: ", graph.backtracking("ForwardChecking"))
    print("Mac: ", graph.backtracking("Mac"))

if __name__ == "__main__":
    main()
