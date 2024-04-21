import utilities as utils
from graph import Graph

def main():
    raw_data = utils.extract_data("table 11")
    graph_11 = Graph(data=raw_data, name="Graph 11")
    graph_11.print_constraint_table()
    graph_11.print_graph()
    graph_11.get_ranks()
    graph_11.get_value_matrix()


    return 0

if __name__ == "__main__":
    main()