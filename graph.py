from tabulate import tabulate
import networkx as nx
import matplotlib.pyplot as plt
import re
from collections import defaultdict, deque


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

    def get_ranks(self):
        rank = defaultdict(int)
        incoming_edges = defaultdict(int)

        successors = defaultdict(list)

        for task, _, *constraints in self.__constraint_table_data:
            rank[task] = 1
            incoming_edges[task] = 0
            for constraint in constraints:

                constraints_list = constraint.split(', ')
                for constraint_vertex in constraints_list:
                    if constraint_vertex != 'None' and constraint_vertex != '':
                        successors[constraint_vertex.strip()].append(task)
                        incoming_edges[task] += 1
        initial_queue = deque(task for task in rank if incoming_edges[task] == 0)
        queue = initial_queue.copy()
        while queue:
            vertex = queue.popleft()
            for successor in successors[vertex]:
                incoming_edges[successor] -= 1
                rank[successor] = max(rank[successor], rank[vertex] + 1)
                if incoming_edges[successor] == 0:
                    queue.append(successor)
        for key,value in rank.items():
            print("Rank of", key, "is", value)
        return rank



    def calculate_earliest_dates(self,rank_dict):

        # Créer un dictionnaire pour stocker les dates de début les plus tôt
        earliest_start = {}

        # Initialiser les dates de début pour les tâches sans contraintes (rang = 0)
        for task, rank in rank_dict.items():
            if rank == 0:
                earliest_start[task] = 0
        sorted_tasks = sorted(rank_dict.items(), key=lambda x: x[1])
        print(sorted_tasks)

        # Calculer les dates de début les plus tôt pour chaque tâche
        for task1, _ in sorted_tasks:
            for task, duration, *constraints in self.__constraint_table_data:
                if task1 == task :
                    print(task1,task)
                    # Récupérer les dates de début des tâches précédentes
                    start_times = []
                    for constraint in constraints[0].split(','):
                        constraint = constraint.strip()
                        print(constraint)
                    if constraint in earliest_start:
                        start_times.append(earliest_start[constraint] + int(duration))

            # Calculer la date de début la plus tôt si des contraintes ont été trouvées
                    if start_times:
                        earliest_start[task] = max(start_times)
                    else :
                        earliest_start[task] = 0
                        print(earliest_start[task], "earliest_task", task)
        print (earliest_start)
        return earliest_start






