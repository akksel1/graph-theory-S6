import utilities as utils
from graph import Graph

def main():
    raw_data = utils.extract_data("table 10")
    graph_8 = Graph(data=raw_data, name="Graph 10")
    graph_8.print_constraint_table()
    graph_8.print_graph()
    return 0

if __name__ == "__main__":
    main()