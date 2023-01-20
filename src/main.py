from Graph import Graph as Graph
from Graph import Node as Node


# CONST VALUES #
N_NODES = 3
SAVE_GRAPH = False

def main():
    graph = Graph(N_NODES)
    print(graph)

    graph.visualize()


if __name__ == "__main__":
    main()
