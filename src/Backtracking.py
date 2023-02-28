colors = {'red', 'green', 'blue'} # TODO: aggiungere anche k4

# CON GRAPH SI INTENDE UN DIZIONARIO CHE HA COME CHIAVE CIASCUN NODO E COME VALORE LA LISTA DEI NODI ADIACENTI AL NODO
def backtrack(graph, assignment):

    if check_assignment_complete(assignment) is True:
        return assignment

    var = select_unassigned_variable(graph, assignment)

    return
    

def check_assignment_complete(assignment):
    return


def select_unassigned_variable(graph, assignment):
    unassigned_var = [node for node in graph if len(assignment[node]) > 1]

    # il nodo con il dominio minore
    return min(unassigned_var, key=lambda node: len(assignment[node]))



def order_domain_values(graph, var, assignment):
    return


def forward_checking(graph, var, assignment):
    return


def mac(graph, var, assignment):
    return
