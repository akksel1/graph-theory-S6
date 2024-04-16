from tabulate import tabulate

class Graph :

    def __init__(self, data, name) :
        """
        Graph constructor.
        Takes raw data from graph file as constructor paramaters and the graph's name.
        Then builds the constraint table and the graph itself from the raw data.
        """

        #raw data (from graph file).
        self.__data  = data

        #graph's name.
        self.__name = name

        #constraint table data (rows) variable.
        self.__constraint_table_data = []

        #constraint table headers (columns).
        self.__constraint_table_headers = ["Task", "Duration", "Constraints"]

        #Executing necessary function to build the graph and its constraint table.
        self.__build_constraint_table()
        self.__build_graph()

    def __build_constraint_table(self) :
        """
        Iterate through raw data and fills __constraint_table_data variable.
        """
        #store each line of the raw data in the line_table table, removing the last one as it is always empty.
        line_table = self.__data.split("\n")[:len( self.__data.split("\n"))-1]

        #iterating through each of the lines.
        for line in  line_table :

            #retrieves task name 
            task_name = line.split(" ")[0]

            #retrieves task duration
            task_duration = line.split(" ")[1]

            #retrieves task constraints (if any) and store them in a temporary variable 
            task_constraints_temp = line.split(" ")[2:len(line.split(" "))]
            
            #if task has no constraints, the table looks like [''], so we are replacing it by ['None'] to match the example in appendix.
            if task_constraints_temp[0] == "":
                task_constraints = "None"

            else :
                #create a string to store constraints in the way they are printed on the appendix example (1, 2, 3...).
                task_constraints = ""
                
                #iterate through each constraint to add them to the string.
                for constraint in task_constraints_temp :
                    task_constraints += constraint + ", "
                
                #remove the last ", " for the table to look good.
                task_constraints = task_constraints[0:len(task_constraints)-2]

            #populate the constraint_table data variable.
            self.__constraint_table_data.append([task_name, task_duration, task_constraints])


    def __build_graph(self) :
        pass

    def print_constraint_table(self) :
        """
        Prints the constraint table using the tabulate module.
        """
        print("\t", self.__name, "constraint table")
        print(tabulate(self.__constraint_table_data, headers=self.__constraint_table_headers, tablefmt="simple_grid"))
