from Graph import Graph as Graph
from Graph import Node as Node


# CONST VALUES #
N_NODES = 6
SAVE_GRAPH = False

def main():
    graph = Graph(N_NODES)
    print(graph)

    random_node1 = graph.get_random_node()
    print(random_node1.get_label())

    graph.generate_edges(random_node1)

    graph.visualize(SAVE_GRAPH)


if __name__ == "__main__":
    main()
