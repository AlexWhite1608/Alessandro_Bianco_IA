from Graph import Graph as Graph
from Graph import Node as Node


# CONST VALUES #
N_NODES = 6
SAVE_GRAPH = False

def main():
    graph = Graph(N_NODES)
    print(graph)

    random_node = graph.get_random_node()
    print(random_node.get_label(), graph.find_nearest_node(random_node).get_label())

    graph.visualize(SAVE_GRAPH)


if __name__ == "__main__":
    main()
