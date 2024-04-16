import utilities as utils
from graph import Graph

def main():
    raw_data = utils.extract_data("table 8")
    graph_8 = Graph(data=raw_data, name="Graph 8")
    graph_8.print_constraint_table()
    return 0

if __name__ == "__main__":
    main()