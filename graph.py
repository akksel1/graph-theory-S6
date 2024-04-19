from tabulate import tabulate
import networkx as nx
import matplotlib.pyplot as plt


class Graph :

    def __init__(self, data, name) :
        """
        Graph constructor.
        Takes raw data from graph file as constructor paramaters and the graph's name.
        Then builds the constraint table and the graph itself from the raw data.
        """

        #Where the graph is stored itself
        #The structure is as it follows :
        """
        graph = {
            "1"(Node name) : (Vertices)[{"2"(Adjacent Node name):"9"(Weight)}, ...], 
            ...
        }
        """
        self.__graph = {}

        #raw data (from graph file).
        self.__data  = data

        #graph's name.
        self.__name = name

        #constraint table data (rows) variable.
        self.__constraint_table_data = []

        #constraint table headers (columns).
        self.__constraint_table_headers = ["Task", "Duration", "Constraints"]

        #Executing necessary function to build the graph and its constraint table.
        self.__build()

    def __build(self) :
        """
        Iterate through raw data and fills __constraint_table_data variable and graph variable.
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

            #Adding the task to the graph.
            self.__graph.update({task_name:[]})
            
            #if task has no constraints, the table looks like [''], so we are replacing it by ['None'] to match the example in appendix.
            if task_constraints_temp[0] == "":
                task_constraints = "None"

            else :
                #create a string to store constraints in the way they are printed on the appendix example (1, 2, 3...).
                task_constraints = ""
                
                #iterate through each constraint to add them to the string.
                for constraint in task_constraints_temp :
                    task_constraints += constraint + ", "

                    #Adding the vertice and its seight to the graph
                    if constraint != "" :
                        self.__graph[task_name].append({constraint:task_duration})
                
                #remove the last ", " for the table to look good.
                task_constraints = task_constraints[0:len(task_constraints)-2]

            #populate the constraint_table data variable.
            self.__constraint_table_data.append([task_name, task_duration, task_constraints])



    def print_graph(self) :
        """
        Plots the graph.
        """

        #Creates a new graph plot.
        plotted_graph = nx.DiGraph()

        #Iterates through the graph structure
        for node in self.__graph :
            
            #Adds each node to the plot.
            plotted_graph.add_node(node)

            #Iterates through each edge of the node.
            for edge in self.__graph[node]:

                #Retrieves the next node.
                adjacent_node = list(edge.keys())[0]

                #Gets the weight.
                weight = edge[adjacent_node]

                #Adds the edge to the plot.
                plotted_graph.add_edge(node, adjacent_node, weight=weight)
        
        #Create the plot interface
        fig, ax = plt.subplots(figsize=(10, 7))

        #Gives the graph plot a circular shape, for it to be clear.
        pos  = nx.circular_layout(plotted_graph)

        #Draws the graph on the plot.
        nx.draw(plotted_graph, pos, ax=ax, with_labels=True, node_color='skyblue', node_size=2000, edge_color='k', font_size=16, font_color="black")
        
        #Indicate to use the weights as edge label.
        edge_labels = nx.get_edge_attributes(plotted_graph, 'weight')

        #Draws the edges.
        nx.draw_networkx_edge_labels(plotted_graph, pos, edge_labels=edge_labels)

        #Sets the plot title.
        ax.set_title(self.__name+" Visual Representation", fontsize=20, fontweight='bold')

        #Sets the plot windows name.
        plt.get_current_fig_manager().set_window_title('Graph Visualization Window')

        #Plots the result.
        plt.show()

    def print_constraint_table(self) :
        """
        Prints the constraint table using the tabulate module.
        """

        # Adds a title.
        print("\t", self.__name, "constraint table")

        # Prints the table.
        print(tabulate(self.__constraint_table_data, headers=self.__constraint_table_headers, tablefmt="simple_grid"))

    def get_ranks(self):

        """
        Returns the ranks of the constraint table.

        """
        print(self.__constraint_table_data)

        ranks_dic = {}

        for(task_name1, task_duration, task_constraints) in self.__constraint_table_data :
            print (task_name1, task_duration, task_constraints)
            for(task_name2, task_duration, task_constraints) in self.__constraint_table_data :
                print(task_name2, task_duration, task_constraints)
                for constraint in task_constraints :
                    if task_name1 == task_name2 :
                        if task_constraints != "None":
                            if constraint != "," and constraint!= " ":
                                ranks_dic[task_name1] = ranks_dic.get(task_name1, 0) + 1
                    else :
                        if constraint == task_name1 :
                            if constraint != "None" :
                                if constraint != "," and constraint != " ":
                                 ranks_dic[task_name1] = ranks_dic.get(task_name1, 0) + 1
        return ranks_dic
      
    def check_cycle(self):
        # Create a copy of constraint table
        constraint_table_cp = self.__constraint_table_data.copy()

        # Store Constraints in a new list
        constraint_list = []
        for i in range(0, len(constraint_table_cp)):
            myTxt = constraint_table_cp[i][2]
            if ", " in myTxt:
                constraint_list.append(myTxt.split(", "))
            else:
                constraint_list.append(myTxt)

        # Eliminating vertex that have no predecessors algorithm
        i = 0
        #Counts the nb of changes in constraint_table_cp
        changeCpt = 1
        #Condition to end the algo
        while len(constraint_table_cp) > 1 and changeCpt > 0:
            changeCpt = 0
            i = 0

            # Cross the graph
            while i < len(constraint_table_cp):
                vertex = constraint_table_cp[i][0]
                # Does this vertex appears in any constraint ?
                isIn = False
                j = 0
                while isIn == False and j < len(constraint_list):
                    if vertex in constraint_list[j]:
                        isIn = True
                    j+=1

                #If not, remove the vertex from the graph
                if isIn == False:
                    constraint_table_cp.pop(i)
                    constraint_list.pop(i)
                    changeCpt+=1
                i+=1

        if len(constraint_list) > 1 :
            return True
        return False

    def check_negative(self):
        i=0
        negative = False

        #Cross the graph
        while negative is False and i < len(self.__constraint_table_data):
            # Check the sign of duration
            if int(self.__constraint_table_data[i][1])<0 :
                negative = True
            i+=1
        return negative






