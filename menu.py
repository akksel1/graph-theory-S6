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
        print("2 - Check if it is a cycle")
        print("3 - Check if it is negative")
        print("4 - Compute ranks")
        print("5 - Compute earliet date, latest date and floats")
        print("6 - Compute critical path and display it")
        print("7 - Select another graph")
        choice = input("Select an option #: ")
        if choice is '1':
            graph.print_constraint_table()
        elif choice is '2':
            if(graph.check_cycle() is False):
                print("No Cycle detected.")
            else:
                print("Cycle detected.")
        elif choice is '3':
            if(graph.check_negative() is False):
                print("Negative weighted edges detected.")
            else:
                print("No negative weighted edges detected.")
        elif choice is '4':
            graph.get_ranks()
        elif choice is '5':
            print("5")
        elif choice is '6':
            print("6")
        elif choice is '7':
            stop = True

    menu()
    return








