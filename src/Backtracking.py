import matplotlib.pyplot as plt
import networkx as nx

COLORS = {'red', 'green', 'blue'}  # TODO: aggiungere anche k4


# CON GRAPH SI INTENDE UN DIZIONARIO CHE HA COME CHIAVE CIASCUN NODO E COME VALORE LA LISTA DEI NODI ADIACENTI AL NODO
def backtrack_fc(nxGraph, graph, assignment, nodes):
    if check_assignment_complete(graph, assignment) is True:
        return assignment

    var = select_unassigned_variable(nxGraph, graph, assignment)

    if var is not None:
        for value in order_domain_values(graph, var, assignment):
            if check_value_consistent(var, value, graph, assignment):
                assignment[var] = [value]
                inferences = forward_checking(graph, var, assignment)
                if inferences is not None:
                    assignment = inferences
                    result = backtrack_fc(nxGraph, graph, assignment, nodes)
                    if result is not None:
                        return result
            else:
                assignment[var].remove(value)

    return None


def backtrack_mac(nxGraph, graph, assignment):
    if check_assignment_complete(graph, assignment) is True:
        return assignment

    var = select_unassigned_variable(nxGraph, graph, assignment)

    if var is not None:
        for value in order_domain_values(graph, var, assignment):
            if check_value_consistent(var, value, graph, assignment):
                assignment[var] = [value]
                inferences = mac(graph, var, assignment)
                if inferences is not False:
                    result = backtrack_mac(nxGraph, graph, assignment)
                    if result is not None:
                        return result
            else:
                assignment[var].remove(value)

    return None


def check_value_consistent(var, value, graph, assignment):
    neighbors_consistent_list = []  # lista che indica per ogni nodo se tutti i nodi vicini sono consistenti

    # Verifica che se ciascun nodo ha il dominio con tutti i colori siamo nella iterazione iniziale e quindi si ha consistenza
    for colors in assignment.values():
        n_colors = len(colors)
        if n_colors != len(COLORS):  # se il numero di colori è diverso allora si fanno gli altri controlli
            break
        else:
            return True

    # for node, neighbors in graph.items():
    #     n_neighbors = len(neighbors)
    #     for neighbor in neighbors:
    #         if neighbor in assignment:
    #             for color in assignment[neighbor]:
    #                 if color != value:
    #                     neighbors_consistent_list.append(True)
    #         if len(neighbors_consistent_list) == n_neighbors:  # tutti i nodi adiacenti sono consistenti
    #             return True

    for neighbors in graph[var]:
        for neighbor in neighbors:
            if value == assignment[neighbor]:
                return False

    return True


def check_assignment_complete(graph, assignment):
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
    i = 0
    for node in graph:
        if len(assignment[node]) == 3:
            i += 1

    # nel caso di prima iterazione (tutti i domini hanno lunghezza 3) si considera il nodo col grado maggiore
    if i == len(graph):
        unassigned_var = sorted(nxGraph.degree, key=lambda x: x[1], reverse=True)
        return unassigned_var[0][0]

    unassigned_var = [node for node in graph if len(assignment[node]) > 1]

    # se non ci sono più variabili disponibili con più di un valore nel dominio, la ricerca fallisce
    if not unassigned_var:
        return None

    # il nodo con il dominio minore
    return min(unassigned_var, key=lambda n: len(assignment[n]))


def order_domain_values(graph, var, assignment):
    domain = assignment[var]
    neighbors = graph[var]  # tutti i nodi adiacenti a var
    n_assigned = {value: 0 for value in
                  domain}  # inizializza a 0 il contatore di quante volte è stato assegnato quel colore

    # controlla per ogni nodo vicino a var se è stato assegnato un colore. in tal caso
    # incrementa il numero di assegnamenti di quel colore
    for neighbor in neighbors:
        if neighbor in assignment:
            colors = assignment[neighbor]
            for color in colors:
                if color in n_assigned:
                    n_assigned[color] += 1

    # ritorna la lista dei colori in ordine crescente
    return sorted(domain, key=lambda value: n_assigned[value])


def forward_checking(graph, var, assignment):
    # Create a copy of the current assignment to modify
    partial_assignment = assignment.copy()

    # Check for conflicts with adjacent nodes
    for neighbor in graph[var]:
        if partial_assignment[var] in partial_assignment[neighbor]:
            chosen_color = partial_assignment[var]
            partial_assignment[neighbor].remove(chosen_color)
            if partial_assignment[neighbor] is None:
                return None

    return partial_assignment


def mac(graph, var, assignment):
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
    arcs = []
    for node in graph:
        for neighbor in graph[node]:
            arcs.append((node, neighbor))

    return arcs
