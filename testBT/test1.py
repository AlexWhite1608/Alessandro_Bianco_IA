import time

import src.Graph as Graph
import matplotlib.pyplot as plt

# CONST VALUES #
N_NODES = 20
ANIMATION = False


# TODO: FAI CON 4 COLORI!!!!

def generate_graph(ax1_title, ax2_title, ax3_title, ax4_title, ax1_data, ax2_data, ax3_data, ax4_data):
    # Creiamo una figura con quattro assi verticali
    fig, axs = plt.subplots(4, sharex=True)


    # Impostiamo i titoli per gli assi
    axs[0].set_title(ax1_title)
    axs[1].set_title(ax2_title)
    axs[2].set_title(ax3_title)
    axs[3].set_title(ax4_title)

    # Estrapoliamo i dati dagli argomenti e li inseriamo in liste separate
    data1_x, data1_y = list(ax1_data.keys()), list(ax1_data.values())
    data2_x, data2_y = list(ax2_data.keys()), list(ax2_data.values())
    data3_x, data3_y = list(ax3_data.keys()), list(ax3_data.values())
    data4_x, data4_y = list(ax4_data.keys()), list(ax4_data.values())

    # Tracciamo i dati sui subplot
    axs[0].plot(data1_x, data1_y)
    axs[1].plot(data2_x, data2_y)
    axs[2].plot(data3_x, data3_y)
    axs[3].plot(data4_x, data4_y)

    # Mostriamo il grafico
    plt.tight_layout()
    plt.show()


# Confronta tempi per risoluzione con mappa random e mappa simmetrica
def time_performance_test():
    ran_FC_data, sym_FC_data = dict(), dict()
    ran_MAC_data, sym_MAC_data = dict(), dict()

    for i in range(2, N_NODES):
        random_graph = Graph.Graph(i, ANIMATION, False)
        sym_graph = Graph.Graph(i, ANIMATION, True)

        print("Random Graph:", random_graph)
        print("Symmetrical Graph:", sym_graph)

        starting_node_random = random_graph.get_random_node()
        starting_node_sym = sym_graph.get_random_node()

        # TODO: prendi i tempi di esecuzione dei bt!
        random_graph.generate_edges(starting_node_random)
        sym_graph.generate_edges(starting_node_sym)

        # -------- FC --------#
        start_time_ran_FC = time.time()
        print("Random graph solution FC: ", random_graph.backtracking("ForwardChecking"))
        end_time_ran_FC = time.time()

        start_time_sym_FC = time.time()
        print("Symmetric graph solution FC: ", sym_graph.backtracking("ForwardChecking"))
        end_time_sym_FC = time.time()

        # ------- MAC --------#
        start_time_ran_MAC = time.time()
        print("Random graph solution MAC: ", random_graph.backtracking("Mac"))
        end_time_ran_MAC = time.time()

        start_time_sym_MAC = time.time()
        print("Symmetric graph solution MAC: ", sym_graph.backtracking("Mac"))
        end_time_sym_MAC = time.time()

        ran_FC_data[i] = (end_time_ran_FC - start_time_ran_FC) * 1000
        ran_MAC_data[i] = (end_time_ran_MAC - start_time_ran_MAC) * 1000

        sym_FC_data[i] = (end_time_sym_FC - start_time_sym_FC) * 1000
        sym_MAC_data[i] = (end_time_sym_MAC - start_time_sym_MAC) * 1000

        del random_graph, sym_graph

    generate_graph("Random Graph FC", "Random Graph MAC", "Symmetric Graph FC", "Symmetric Graph MAC",
                   ran_FC_data, ran_MAC_data, sym_FC_data, sym_MAC_data)
