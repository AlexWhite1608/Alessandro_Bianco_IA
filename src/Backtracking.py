import random

colors = {'red', 'green', 'blue'} # TODO: aggiungere anche k4

# CON GRAPH SI INTENDE UN DIZIONARIO CHE HA COME CHIAVE CIASCUN NODO E COME VALORE LA LISTA DEI NODI ADIACENTI AL NODO
def backtrack(graph, assignment):

    if check_assignment_complete(graph, assignment) is True:
        return assignment

    var = select_unassigned_variable(graph, assignment)

    for value in order_domain_values(graph, var, assignment):
        if check_value_consistent(value, graph, assignment):
            assignment[var] = value

    print(assignment)

    return


def check_value_consistent(value, graph, assignment):
    neighbors_consistent_list = [] # lista che indica per ogni nodo se tutti i nodi vicini sono consistenti

    if len(assignment.keys()) == 0:
        return True

    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor in assignment and assignment[neighbor] != value:
                neighbors_consistent_list.append(True)
            if len(neighbors_consistent_list) == len(neighbors):    # tutti i nodi adiacenti sono consistenti
                return True

    return False


def check_assignment_complete(graph, assignment):

    for node in graph:
        if node not in assignment:
            return False
        for neighbor in graph[node]:
            if neighbor in assignment and assignment[node] == assignment[neighbor]:
                return False

    return True


def select_unassigned_variable(graph, assignment):

    if len(assignment.keys()) == 0:
        #TODO: DEGREE HEURISTIC per fare iniziare
        return list(graph.keys())[0]



    unassigned_var = [node for node in graph if len(assignment[node]) > 1]

    # il nodo con il dominio minore
    return min(unassigned_var, key=lambda node: len(assignment[node]))



def order_domain_values(graph, var, assignment):

    domain = list(colors)
    neighbors = graph[var]  # tutti i nodi adiacenti a var
    n_assigned = {value: 0 for value in domain} # inizializza a 0 il contatore di quante volte è stato assegnato quel colore

    # controlla per ogni nodo vicino a var se è stato assegnato un colore. in tal caso
    # incrementa il numero di assegnamenti di quel colore
    for neighbor in neighbors:
        if neighbor in assignment:
            value = assignment[neighbor]
            if value in n_assigned:
                n_assigned[value] += 1

    # ritorna la lista dei colori in ordine crescente
    return sorted(domain, key=lambda value: n_assigned[value])


def forward_checking(graph, var, assignment):
    return


def mac(graph, var, assignment):
    return
