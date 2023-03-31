import matplotlib.pyplot as plt
import networkx as nx
import Graph as G

COLORS = {'red', 'green', 'blue', 'yellow'}


def backtrack_fc(nxGraph, graph, assignment, nodes, animate):

    """

    Backtrack algorithm using Forward Checking. At first, we check if the assignment is complete; if not we select a node
    using the MRV heuristic combined with the degree heuristic. Then we order the domain of the selected variable using
    Least Constraining Value heuristic and check for consistency. We finally assign the color to the node and then
    inferences are made (using Forward Checking) and the nodes are correctly colored. We repeat the process until all
    the nodes are assigned to the right color or there is no possible complete assignment.

    :param nxGraph:     (nxGraph)
    :param graph:       (dict) dictionary corresponding to the structure of the graph {node: [neighbors]}
    :param assignment:  (dict) dictionary corresponding to the initial color assignment for each node {node: [color]}
    :param nodes:       (list) list of Nodes of the graph
    :param animate:     (bool) True if we want animation, false otherwise
    :return:            (dict) dictionary corresponding to the final color assignment

    """

    if check_assignment_complete(graph, assignment) is True:
        print("FC: ", assignment)
        return assignment

    var = select_unassigned_variable(nxGraph, graph, assignment)

    if var is not None:
        for value in order_domain_values(graph, var, assignment):
            if check_value_consistent(var, value, graph, assignment):
                assignment[var] = [value]
                inferences = forward_checking(graph, var, assignment)
                if inferences is not None:
                    assignment = inferences
                    if animate:
                        print_node_color(nodes, nxGraph, assignment, "FC")
                    result = backtrack_fc(nxGraph, graph, assignment, nodes, animate)
                    if result is not None:
                        return result
            else:
                assignment[var].remove(value)

    return False


def backtrack_mac(nxGraph, graph, assignment, nodes, animate):

    """

    Backtrack algorithm using Maintaining Arc Consistency. At first, we check if the assignment is complete; if not
    we select a node using the MRV heuristic combined with the degree heuristic. Then we order the domain of the
    selected variable using Least Constraining Value heuristic and check for consistency. We finally assign the color
    to the node and then inferences are made (using MAC) and the nodes are correctly colored. We repeat the process
    until all the nodes are assigned to the right color or there is no possible complete assignment.

    :param nxGraph:     (nxGraph)
    :param graph:       (dict) dictionary corresponding to the structure of the graph {node: [neighbors]}
    :param assignment:  (dict) dictionary corresponding to the initial color assignment for each node {node: [color]}
    :param nodes:       (list) list of Nodes of the graph
    :param animate:     (bool) True if we want animation, false otherwise
    :return:            (dict) dictionary corresponding to the final color assignment

    """

    if check_assignment_complete(graph, assignment) is True:
        print("MAC:", assignment)
        return assignment

    var = select_unassigned_variable(nxGraph, graph, assignment)

    if var is not None:
        for value in order_domain_values(graph, var, assignment):
            if check_value_consistent(var, value, graph, assignment):
                assignment[var] = [value]
                inferences = mac(graph, var, assignment)
                if inferences is not False:
                    if animate:
                        print_node_color(nodes, nxGraph, assignment, "MAC")
                    result = backtrack_mac(nxGraph, graph, assignment, nodes, animate)
                    if result is not None:
                        return result
            else:
                assignment[var].remove(value)

    return False


def check_value_consistent(var, value, graph, assignment):

    """

    Checks if the current assignment is consistent (if neighbors nodes don't have the same color assignment)

    :param var:         (Node) current node selected
    :param value:       (String) current color assigned to the node
    :param graph:       (dict) dictionary corresponding to the structure of the graph {node: [neighbors]}
    :param assignment:  (dict) dictionary corresponding to the color assignment for each node {node: [color]}
    :return:            True if assignment consistent, False otherwise

    """

    # If each node has len(colors) color assignments we don't check for consistency because we are in the first iteration
    for colors in assignment.values():
        n_colors = len(colors)
        if n_colors != len(COLORS):
            break
        else:
            return True

    for neighbors in graph[var]:
        for neighbor in neighbors:
            if value == assignment[neighbor]:
                return False

    return True


def check_assignment_complete(graph, assignment):

    """

    Checks if current assignment is complete (all the nodes have the correct color being assigned and there is consistency)

    :param graph:       (dict) dictionary corresponding to the structure of the graph {node: [neighbors]}
    :param assignment:  (dict) dictionary corresponding to the color assignment for each node {node: [color]}
    :return:            True if assignment is complete, False otherwise

    """

    for node in assignment:
        if len(assignment[node]) > 1:
            return False

    for node in graph:
        if node not in assignment:
            return False
        for neighbor in graph[node]:
            if neighbor in assignment and assignment[node] == assignment[neighbor]:
                return False

    return True


def select_unassigned_variable(nxGraph, graph, assignment):

    """

    Selects the unassigned nodes from the graph following the LRV heuristic

    :param nxGraph:     (nxGraph)
    :param graph:       (dict) dictionary corresponding to the structure of the graph {node: [neighbors]}
    :param assignment:  (dict) dictionary corresponding to the color assignment for each node {node: [color]}
    :return:            (Node)

    """

    # Counts the number of nodes that have the length of their domain == 3
    n_nodes_with_len_3 = sum(1 for node in graph if len(assignment[node]) == 3)

    # In case of first iteration (all the domains have length == 3) we consider the node with higher grade (heuristic)
    if n_nodes_with_len_3 == len(graph):
        unassigned_var = sorted(nxGraph.degree, key=lambda x: x[1], reverse=True)
        return unassigned_var[0][0]

    unassigned_var = [node for node in graph if len(assignment[node]) > 1]

    # If there are no variables left with length(domain) > 1
    if not unassigned_var:
        return None

    # Return the node with the lowest domain size
    return min(unassigned_var, key=lambda n: len(assignment[n]))


def order_domain_values(graph, var, assignment):

    """

    Orders the domain of each variable following the Least-Constraining-Value heuristic

    :param graph:       (dict) dictionary corresponding to the structure of the graph {node: [neighbors]}
    :param var:         (Node) current node variable selected
    :param assignment:  (dict) dictionary corresponding to the color assignment for each node {node: [color]}
    :return:            (dict) a sorted list of colors corresponding to the domain of the current variable

    """

    domain = assignment[var]
    neighbors = graph[var]

    # Create a dictionary that maps each color to the number of times it appears in the domain of the neighboring nodes
    n_assigned = {}
    for neighbor in neighbors:
        if neighbor in assignment:
            for color in assignment[neighbor]:
                n_assigned[color] = n_assigned.get(color, 0) + 1

    # Sort the colors in the domain of the variable by their number of occurrences in the neighboring domains
    sorted_domain = sorted(domain, key=lambda c: n_assigned.get(c, 0))

    return sorted_domain


def forward_checking(graph, var, assignment):

    """

    Forward checking inference: removes the conflicting colors from the neighbor's domain of var. Returns a partial
    assignment of colors.

    :param graph:       (dict) dictionary corresponding to the structure of the graph {node: [neighbors]}
    :param var:         (Node) current node variable selected
    :param assignment:  (dict) dictionary corresponding to the color assignment for each node {node: [color]}
    :return:            (dict) a partial assignment of the colors to the nodes

    """

    # Creates a copy of the current assignment to modify
    partial_assignment = assignment.copy()

    # Checks for conflicts with adjacent nodes
    for neighbor in graph[var]:
        if partial_assignment[var] in partial_assignment[neighbor]:
            chosen_color = partial_assignment[var]
            partial_assignment[neighbor].remove(chosen_color)
            if partial_assignment[neighbor] is None:
                return None

    return partial_assignment


def mac(graph, var, assignment):

    """

    Maintaining arc consistency inference (MAC): uses the AC-3 algorithm to guarantee arc consistency between each node
    of the graph.

    :param graph:       (dict) dictionary corresponding to the structure of the graph {node: [neighbors]}
    :param var:         (Node) current node variable selected
    :param assignment:  (dict) dictionary corresponding to the color assignment for each node {node: [color]}
    :return:            True if consistency is detected, False otherwise

    """

    q = get_neighbors(graph)

    while len(q) > 0:
        (x_i, x_j) = q.pop()
        if revise(x_i, x_j, assignment):
            if len(assignment[x_i]) == 0:
                return False
            for neighbor in graph[x_i]:
                if neighbor is not x_j:
                    q.append((neighbor, x_i))

    return True


def revise(x_i, x_j, assignment):

    """

    Implements the revise procedure to execute AC-3. Iterates between each possible color assignment of x_i, and for
    each color searches for an available node x_j such that the assignment is consistent. Otherwise, it removes the
    color from the available colors for the x_i node and is_revised is set True.


    :param x_i:         (Node) first node to check for arc consistency
    :param x_j:         (Node) second node to check for arc consistency
    :param assignment:  (dict) dictionary corresponding to the color assignment for each node {node: [color]}
    :return:            True if there is a revise of the assignment, False otherwise

    """

    is_revised = False
    for x in assignment[x_i]:
        is_consistent = False
        for y in assignment[x_j]:
            if x is not y:
                is_consistent = True
                break
        if not is_consistent:
            assignment[x_i].remove(x)
            is_revised = True

    return is_revised


def get_neighbors(graph):

    """

    Returns the list of neighbors for each node in graph

    :param graph:   (dict) dictionary corresponding to the structure of the graph {node: [neighbors]}
    :return:        (list) list of tuples containing all the neighbors for each node [(node, neighbor)]

    """

    arcs = []
    for node in graph:
        for neighbor in graph[node]:
            arcs.append((node, neighbor))

    return arcs


def print_node_color(nodes, nxGraph, assignment, bt_type):

    """

    Used for the color animation of the graph. If it is called in the first iteration of the backtracking algorithm it
    sets all the nodes color to black, otherwise the colors of the nodes are set based on the assignment evaluated by
    the algorithm

    :param nodes:       (list) list of Node class instances referring to each node of the graph
    :param nxGraph:     (nxGraph) nxGraph object used for the graph visualization properties
    :param assignment:  (dict) dictionary corresponding to the color assignment for each node {node: [color]}
    :param bt_type:     (String) used to distinguish between FC and MAC algorithm for the different starting condition

    """

    colors = {}
    fig, ax = plt.subplots()

    # In the first iteration all the nodes are black, otherwise the color is set based on assignment color value
    if bt_type == "FC":
        ax.set_title("Backtracking with FC")
        for node in nodes:
            if len(assignment[node.get_label()]) == 3:
                colors[node.get_label()] = 'black'
            else:
                colors[node.get_label()] = assignment[node.get_label()][0]
    elif bt_type == "MAC":
        ax.set_title("Backtracking with MAC")
        for node in nodes:
            if len(assignment[node.get_label()]) != 1:
                colors[node.get_label()] = 'black'
            else:
                colors[node.get_label()] = assignment[node.get_label()][0]

    # Assignment of the pos and color attributes for the nx graph
    nx.set_node_attributes(nxGraph, colors, 'color')
    pos = nx.get_node_attributes(nxGraph, 'pos')
    colors = nx.get_node_attributes(nxGraph, 'color')
    node_colors = [colors[node.get_label()] for node in nodes]

    nx.draw_networkx_nodes(nxGraph, pos=pos, node_color=node_colors, node_size=220)
    nx.draw_networkx_edges(nxGraph, nx.get_node_attributes(nxGraph, 'pos'))
    nx.draw_networkx_labels(nxGraph, nx.get_node_attributes(nxGraph, 'pos'), font_size=10, font_color="white")
    plt.show()
    plt.pause(G.PAUSE)
