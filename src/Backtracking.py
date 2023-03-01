COLORS = {'red', 'green', 'blue'}  # TODO: aggiungere anche k4

# CON GRAPH SI INTENDE UN DIZIONARIO CHE HA COME CHIAVE CIASCUN NODO E COME VALORE LA LISTA DEI NODI ADIACENTI AL NODO
def backtrack_fc(graph, assignment):
    if check_assignment_complete(graph, assignment) is True:
        return assignment

    var = select_unassigned_variable(graph, assignment)

    for value in order_domain_values(graph, var, assignment):
        if check_value_consistent(value, graph, assignment):
            assignment[var] = value
            inferences = forward_checking(graph, var, assignment)
            if inferences is not None:
                assignment = inferences
                result = backtrack_fc(graph, assignment)
                if result is not None:
                    return result
        else:
            assignment[var].remove(value)
    return None


def backtrack_mac(graph, assignment):
    return


def check_value_consistent(value, graph, assignment):
    neighbors_consistent_list = []  # lista che indica per ogni nodo se tutti i nodi vicini sono consistenti

    # Verifica che se ciascun nodo ha il dominio con tutti i colori siamo nella iterazione iniziale e quindi si ha consistenza
    for colors in assignment.values():
        n_colors = len(colors)
        if n_colors != len(COLORS):
            break
        else:
            return True



    for node, neighbors in graph.items():
        n_neighbors = len(neighbors)
        for neighbor in neighbors:
            if neighbor in assignment:
                for color in assignment[neighbor]:
                    if color != value:
                        neighbors_consistent_list.append(True)
            if len(neighbors_consistent_list) == n_neighbors:  # tutti i nodi adiacenti sono consistenti
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
    #TODO: manca euristica per il primo valore!

    unassigned_var = [node for node in graph if len(assignment[node]) > 1]

    # il nodo con il dominio minore
    return min(unassigned_var, key=lambda node: len(assignment[node]))


def order_domain_values(graph, var, assignment):
    domain = assignment[var]
    neighbors = graph[var]  # tutti i nodi adiacenti a var
    n_assigned = {value: 0 for value in domain}  # inizializza a 0 il contatore di quante volte è stato assegnato quel colore

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
    partial_assignment = dict(assignment)

    # Check for conflicts with adjacent variables
    for neighbor in graph[var]:
        if partial_assignment[var] in partial_assignment[neighbor]:
            chosen_color = partial_assignment[var]
            partial_assignment[neighbor].remove(chosen_color)
            if partial_assignment[neighbor] is None:
                return None

    return partial_assignment


def mac(graph, var, assignment):
    return
