import utilities as utils
from graph import Graph

def menu():
    choice=False

    print("\t----- GRAPH THEORY PROJECT -----\n\nSelect a graph:\n")
    for i in range(1,15):
        print(i,"- Graph #",i)
    print("15 - Graph Cycle #15")
    print("16 - Graph No Cycle #16")
    print("17 - Graph Negative #17")

    while choice is False:
        graphNb = input("Enter a graph number: ")

        if 0 < int(graphNb) < 18:
            choice = True
            menu2(int(graphNb))
        else:
            choice = False
            print("Graph not found. Error\n")


def menu2(graphNb):
    stop = False

    #Load the graph
    file_name = "table " + str(graphNb)
    raw_data = utils.extract_data(file_name)
    graph_name = "Graph " + str(graphNb)
    graph = Graph(data=raw_data, name=graph_name)
    graph.print_graph()

    while stop is False :
        # Print menu
        print("\n\n\n\t----- GRAPH", graphNb, "-----\n")
        print("1 - Display the Graph")
        print("2 - Display the Value Matrix")
        print("3 - Check if it is a cycle")
        print("4 - Check if it is negative")
        print("5 - Compute ranks")
        print("6 - Compute earliet date, latest date and floats")
        print("7 - Compute critical path and display it")
        print("8 - Select another graph")
        choice = input("Select an option #: ")
        if choice is '1':
            graph.print_constraint_table()
        elif choice is '2':
            graph.get_value_matrix()
        elif choice is '3':
            print("\n\n")
            if(graph.check_cycle() is False):
                print("\n\nNo Cycle detected.")
            else:
                print("\n\nCycle detected.")
        elif choice is '4':
            if(graph.check_negative() is True):
                print("Negative weighted edges detected.")
            else:
                print("No negative weighted edges detected.")
        elif choice is '5':
            graph.get_ranks()
        elif choice is '6':
            print("5")
        elif choice is '7':
            if(graph.check_cycle() is False and graph.check_negative() is False):
                graph.print_critical_paths()
            else:
                if graph.check_cycle() is True:
                    print("\n\nERROR: Cycle detected.")
                if graph.check_negative() is True:
                    print("\n\nERROR: Negative weighted edges detected. .")

        elif choice is '8':
            stop = True

    menu()
    return








