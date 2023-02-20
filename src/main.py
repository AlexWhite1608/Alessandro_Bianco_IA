from Graph import Graph as Graph
from Graph import Node as Node


# CONST VALUES #
N_NODES = 10
SAVE_GRAPH = False

def main():
    graph = Graph(N_NODES, SAVE_GRAPH)
    print(graph)

    random_node1 = graph.get_random_node()
    print("RANDOM: ", random_node1.get_label())

    graph.generate_edges(random_node1)



if __name__ == "__main__":
    main()
