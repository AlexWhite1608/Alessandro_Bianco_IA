from Graph import Graph as Graph
from Graph import Node as Node


# CONST VALUES #
N_NODES = 6
SAVE_GRAPH = False

def main():
    graph = Graph(N_NODES)
    print(graph)

    graph.visualize(graph.get_random_node())


if __name__ == "__main__":
    main()
