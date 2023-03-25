import time

from matplotlib import pyplot as plt
from Backtracking import COLORS
import Graph as Graph
from testBT import test1

# CONST VALUES #
N_NODES = 10
ANIMATION = True
SYMMETRICAL = False
BT_TYPE = "Mac"


def main():
    #FIXME: togli il simmetrical bro

    # TEST
    test1.test_graph_visualization(N_NODES, ANIMATION, SYMMETRICAL, BT_TYPE)
    test1.comparison_k3_k4()
    test1.test_failed_assignment()


if __name__ == "__main__":
    main()
