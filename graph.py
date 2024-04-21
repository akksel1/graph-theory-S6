from tabulate import tabulate
import networkx as nx
import matplotlib.pyplot as plt
import re
from collections import defaultdict


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
        #store each line of the raw data in the line_table table.
        line_table = self.__data.split("\n")

        #Sometimes last line is empty so we remove it.
        if line_table[-1] == "" :
            line_table.pop(line_table.index(line_table[-1]))
        
        #Temp dict that will associates tasks with their duration.
        task_dur = {}

        #Adding all the tasks to the graph and storing their duration.
        for line in  line_table :

            #retrieves task name 
            task_name = line.split(" ")[0]

            #retrieves task duration
            task_duration = line.split(" ")[1]

            self.__graph.update({task_name:[]})

            task_dur.update({task_name:task_duration})

        #iterating through each of the lines.
        for line in  line_table :

            #retrieves task name 
            task_name = line.split(" ")[0]

            #retrieves task duration
            task_duration = line.split(" ")[1]

            #retrieves task constraints (if any) and store them in a temporary variable 
            task_constraints_temp = line.split(" ")[2:len(line.split(" "))]

            #Sometimes there is a missing space in the files so task_constraint_temp is emtpy.
            if len(task_constraints_temp) == 0 :
                task_constraints_temp.append("")
            
            #if task has no constraints, the table looks like [''], so we are replacing it by ['None'] to match the example in appendix.
            if task_constraints_temp[0] == "":
                task_constraints = "None"

            else :
                #create a string to store constraints in the way they are printed on the appendix example (1, 2, 3...).
                task_constraints = ""
                
                #iterate through each constraint to add them to the string.
                for constraint in task_constraints_temp :
                    task_constraints += constraint + ", "

                    #Adding the vertice and its weight to the graph
                    if constraint != "" :
                        self.__graph[constraint].append({task_name:task_dur[constraint]})
                
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
        #Initialize the dictionnary where we will store the task_name (key) and the rank (value)
        ranks_dic = {}

        #Go through the constraint table data twice in order to get the number of predecessors & successors of each task
        for(task_name1, task_duration, task_constraints) in self.__constraint_table_data :
            for(task_name2, task_duration, task_constraints) in self.__constraint_table_data :
                for constraint in task_constraints :
                    #If the both task_name are equal, then the ranks will be +1 each time we have a new constraint
                    if task_name1 == task_name2 :
                        if task_constraints != "None":
                            if constraint != "," and constraint!= " ":
                                ranks_dic[task_name1] = ranks_dic.get(task_name1, 0) + 1
                    #If we find among the predecessor of another task, the task itsself, then its rank will be +1
                    else :
                        if constraint == task_name1 :
                            if constraint != "None" :
                                if constraint != "," and constraint != " ":
                                 ranks_dic[task_name1] = ranks_dic.get(task_name1, 0) + 1
        for key in ranks_dic.keys():
            print("The rank of", key, "is", ranks_dic[key])
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



    def get_value_matrix(self):
        value_matrix = [[0 for j in range(len(self.__constraint_table_data)+3)] for i in range(len(self.__constraint_table_data)+3)]
        #Initalize the Matrix with the Index from 0 to the number of vertices, with a * everywhere else
        for i in range(len(value_matrix)):
            for j in range(len(value_matrix)):
                if i == 0 or j == 0:
                    if i == 1 or j == 1:
                        value_matrix[i][j] = 0
                    elif i == len(value_matrix) or j == len(value_matrix):
                        value_matrix[i][j] = len(value_matrix) + 1
                    elif i ==0 and j!=0:
                        value_matrix[i][j] = j - 1
                    elif j ==0 and i!=0:
                        value_matrix[i][j] = i - 1
                    elif i==0 and j==0:
                        value_matrix[i][j] = ' '

                else :
                    value_matrix[i][j] = '*'

        #Setting up the predecessor set which will tell us the vertices who has no successor, then they will be automatically directed to the output/end vertex of the graph
        predecessors = set()
        all_task = set()
        for i in range(len(self.__constraint_table_data)):
            all_task.add(i + 1)
        for (task_name1, task_duration, task_constraints) in self.__constraint_table_data:
            if task_constraints != "None":
                numbers = re.findall(r'\d+', task_constraints)
                task_constraints = [int(num) for num in numbers]
                for constraint in task_constraints:
                    if constraint != "," and constraint != " " and constraint and task_constraints != "None":
                        predecessors.add(constraint)
        predecessors = set(map(int, predecessors))
        no_predeccessor = all_task - predecessors

        #Going through the constraint table data in order to fill up the value matrix
        for(task_name1, task_duration, task_constraints) in self.__constraint_table_data :

            #If there is a constraint, we take the task_duration of the constraint and put it in the value matrix
            if task_constraints != "None" :
                numbers = re.findall(r'\d+', task_constraints)
                task_constraints = [int(num) for num in numbers]
                for constraint in task_constraints:
                        for (task_name2, task_duration, task_constraints) in self.__constraint_table_data:
                                if(constraint == int(task_name2) ):
                                    value_matrix[int(constraint) + 1][int(task_name1) +1 ] =int(task_duration)
            #Else, we just say that as the vertex has no constraint, he will be a possible start/input from the ficticious task 0
            else :
                value_matrix[1][int(task_name1)+1] = 0
        #For those who doesn't have any successor, they will be linked to the end/output ficticious task N+1
        for (task_name, task_duration, task_constraints) in self.__constraint_table_data:
            if (int(task_name) in no_predeccessor) :
                    value_matrix[int(task_name)+1][len(self.__constraint_table_data) +2 ] =task_duration

        for i in range(len(value_matrix)):
            print('\n')
            for j in range(len(value_matrix)):
                print(value_matrix[i][j], end='     ')
        return value_matrix

    def get_earliest_date(self):
            vertices = [task_name[0] for task_name in self.__constraint_table_data]
            print(vertices)
            # Initialize a dictionary to store the earliest start time for each vertex
            earliest_start = {vertex: 0 for vertex in vertices}

            # Initialize a dictionary to store the cumulative duration for each vertex
            cumulative_duration = {vertex: 0 for vertex in vertices}

            # Create a dictionary to store the predecessors for each vertex
            predecessors_dict = defaultdict(list)
            for task, duration, *constraints in self.__constraint_table_data:
                for constraint in constraints:
                    predecessors_dict[task].append(constraint)

            # Topological sorting
            for vertex in vertices:
                if not predecessors_dict[vertex]:  # If the vertex has no predecessors
                    continue

                # Calculate the earliest start time for the current vertex
                earliest_start_time = max(
                    earliest_start[constraint] + cumulative_duration[constraint] for constraint in
                    predecessors_dict[vertex])
                earliest_start[vertex] = earliest_start_time

                # Update the cumulative duration for the current vertex
                cumulative_duration[vertex] = earliest_start_time + int(duration)
            print(earliest_start)
            return earliest_start




