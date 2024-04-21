from tabulate import tabulate
import networkx as nx
import matplotlib.pyplot as plt
import copy
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

        #Same as the previous graph but modified to have a critical path (node 0 and node n+1).
        self.__critical_graph = {}

        #raw data (from graph file).
        self.__data  = data

        #graph's name.
        self.__name = name

        #constraint table data (rows) variable.
        self.__constraint_table_data = []

        #constraint table headers (columns).
        self.__constraint_table_headers = ["Task", "Duration", "Constraints"]

        #Dict that will associates tasks with their duration.
        self.__task_dur = {}

        #Will store constraint table as the same way graph is stored :
        """{
            "1"(Node name) : (Predecessors)["2"(Predecessor Node name), ...], 
            ...
        }"""
        self.__raw_constraint_table = {}

        #Will store critcal paths.
        self.__critical_paths = []

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
        

        #Adding all the tasks to the graph and storing their duration.
        for line in  line_table :

            #retrieves task name 
            task_name = line.split(" ")[0]

            #retrieves task duration
            task_duration = line.split(" ")[1]

            self.__graph.update({task_name:[]})

            self.__task_dur.update({task_name:task_duration})

        #iterating through each of the lines.
        for line in  line_table :

            #retrieves task name 
            task_name = line.split(" ")[0]

            #retrieves task duration
            task_duration = line.split(" ")[1]

            #retrieves task constraints (if any) and store them in a temporary variable 
            task_constraints_temp = line.split(" ")[2:len(line.split(" "))]

            #Adding the task in the raw constraint table.
            self.__raw_constraint_table.update({task_name:[]})

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

                    #Adding the vertice and its weight to the graph.
                    if constraint != "" :
                        self.__graph[constraint].append({task_name:self.__task_dur[constraint]})

                        #Adding the constraint to the raw constraint table.
                        self.__raw_constraint_table[task_name].append(constraint)
                
                #remove the last ", " for the table to look good.
                task_constraints = task_constraints[0:len(task_constraints)-2]

            #populate the constraint_table data variable.
            self.__constraint_table_data.append([task_name, task_duration, task_constraints])

        self.__compute_critical_path()

    def __compute_critical_path(self) :
        """
        Compute the critical paths from the graph.
        """

        #Getting the name of the n+1 node.
        exit_node = str(len(self.__graph)+1)
        
        def find_no_predecessors_nodes() :
            """
            Returns the list of all nodes without predecessors in a graph.
            """
            node_list = []
            
            #Iterates through each node of the constraint table.
            for node in self.__raw_constraint_table :

                #If the tasks has no constraints (node has no predecessors):
                if len(self.__raw_constraint_table[node]) == 0 :

                    #Adds the node to the list.
                    node_list.append(node)

            return node_list
        
        def find_no_sucessors_nodes() :
            """
            Returns the list of all nodes without successors un a graph
            """
            node_list = []

            #Iterates through each node of the graph.
            for node in self.__graph :

                #If the node has no successor :
                if len(self.__graph[node]) == 0 :

                    #Adds the node to the list.
                    node_list.append(node)

            return node_list
        
        def add_entry_exit_nodes() :
            """
            Adds the 0 and n+1 nodes to the graph (critical_graph).
            """
        
            #Find nodes with no predecessors.
            no_pre = find_no_predecessors_nodes()
           
            #find nodes with no successors.
            no_suc = find_no_sucessors_nodes()

            #Initializing the critical graph sith the same values as the graph.
            self.__critical_graph = copy.deepcopy(self.__graph) #Here we make sure to copy the variable so the changes on critical graph won't affect the classic graph.
            

            #Adds the node 0 to the critical graph.
            self.__critical_graph.update({'0':[]})

            #Adds the n+1 node to the critical graph.
            self.__critical_graph.update({exit_node:[]})
            
            #Adding verticies going from node 0:
            for node in no_pre :
                
                #The weight is 0.
                self.__critical_graph['0'].append({node:"0"})

            #Adding verticies going to node n+1:
            for node in no_suc :
                
                #Retrieving the weight from task_dur.
                self.__critical_graph[node].append({exit_node:self.__task_dur[node]})

        def simplify_graph():
            """
            Gets rid of the weights.
            """
            simplified_graph = {}
            for node, edges in self.__critical_graph.items():
                simplified_graph[node] = []
                for edge in edges:
                    for target, weight in edge.items():
                        simplified_graph[node].append(target)
            return simplified_graph

        def find_paths(graph, start, end, path=[]):
            """
            Recursive function that get all paths from a starting node to an end node.
            """
            path = path + [start]
            if start == end:
                return [path]
            if start not in graph:
                return []
            paths = []
            for node in graph[start]:
                if node not in path:  # Avoid cycles
                    newpaths = find_paths(graph, node, end, path)
                    for newpath in newpaths:
                        paths.append(newpath)
            return paths
        
        def path_length(path) :
            """
            Compute the length of a path (adds all its weights).
            """

            length = 0

            #Iterating through all the path -1 as the exit node has no weight.
            for i in range(len(path)-1) :

                #Entry node (0) has no weight on its vertices so we can skeep it.
                if path[i] != "0" :
                    length += int(self.__task_dur[path[i]])

            return length

        #Adding entry and exit nodes.
        add_entry_exit_nodes()

        #Simplify the graph 
        simp_crit_graph = simplify_graph()

        #Retrieves all paths from entry to exit node (0 to n+1)
        all_paths_entry_to_exit = find_paths(simp_crit_graph, '0', exit_node)
        
        #Will store all lengths
        all_lengths = []

        #Getting all paths length
        for path in all_paths_entry_to_exit :
            all_lengths.append(path_length(path))
       
        #Retrieving the max length
        #max_length = max(all_lengths)

        if all_lengths:
            max_length = max(all_lengths)
            # logic to handle found paths
        else:
            max_length = 0  # or appropriate error handling
            print("No paths found from entry to exit nodes.")

        #Adding critical paths to the correct variable:
        for i in range(len(all_lengths)) :
            if all_lengths[i] == max_length :
                self.__critical_paths.append(all_paths_entry_to_exit[i])


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

    def print_critical_paths(self) :
        """
        Plots the critical graph and higlights critical paths.
        """
        print("Critical paths :", self.__critical_paths)
        #Will store each node that is on a critical path.
        critical_nodes = set()

        #Creates a list to hold tuples of edges in critical paths
        critical_edges = []

        for path in self.__critical_paths:

            critical_nodes.update(path)

            # Add edge tuples to the list
            critical_edges.extend([(path[i], path[i+1]) for i in range(len(path)-1)])

        #Creates a new graph plot.
        plotted_graph = nx.DiGraph()

        #Iterates through the graph structure
        for node in self.__critical_graph :
            
            #Adds each node to the plot.
            plotted_graph.add_node(node)

            #Iterates through each edge of the node.
            for edge in self.__critical_graph[node]:

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
        node_colors = ['red' if node in critical_nodes else 'skyblue' for node in plotted_graph]
        edge_colors = ['red' if (u, v) in critical_edges or (v, u) in critical_edges else 'black' for u, v in plotted_graph.edges()]

        nx.draw(plotted_graph, pos, ax=ax, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=2000, font_size=16, font_color="black")
        
        #Indicate to use the weights as edge label.
        edge_labels = nx.get_edge_attributes(plotted_graph, 'weight')

        #Draws the edges.
        nx.draw_networkx_edge_labels(plotted_graph, pos, edge_labels=edge_labels)

        #Sets the plot title.
        ax.set_title(self.__name+" Critical Paths Representation (in red)", fontsize=20, fontweight='bold')

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
        '''
        Function that checks if there is any cycle on the graph. Returns a boolean:
            False: No Cycle detected
            True: Cycle detected
        '''
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
                    print("Eliminating vertex #",vertex)
                    constraint_table_cp.pop(i)
                    constraint_list.pop(i)
                    print("Remaining vertices:")
                    for a in range(0,len(constraint_table_cp)):
                        print("Vertex #",constraint_table_cp[a][0])
                    changeCpt+=1
                i+=1

        if len(constraint_list) > 1 :
            return True
        return False


    def check_negative(self):
        '''
        Function that checks if there is any negative weighted edges on the graph. Returns a boolean:
            False: Negative edges detected
            True: No Negative edges detected
        '''
        i=0
        negative = False

        #Cross the graph
        while negative is False and i < len(self.__constraint_table_data):
            # Check the sign of duration
            if int(self.__constraint_table_data[i][1])<0:
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
        return rank

    def compute_earliest_dates(self, rank):
        predecessors_dict = {}

        # Iterate through the constraint table data
        for task, _, *constraints in self.__constraint_table_data:
            # Extract task name and constraints
            task_name = task
            task_constraints = constraints

            # Split constraints string into a list if it exists
            if task_constraints[0] != "None":
                task_constraints = [constraint.strip() for constraint in task_constraints[0].split(',')]
            else:
                task_constraints = []

            # Populate predecessors dictionary
            predecessors_dict[task_name] = task_constraints
        # Initialize a dictionary to store the earliest start times of each task
        earliest_start = {}
        successors = defaultdict(list)


        # Iterate through the tasks in topological order (based on rank)
        for task, duration, *_ in sorted(self.__constraint_table_data, key=lambda x: rank[x[0]]):
            # Compute earliest start time for the current task
            earliest_start_time = 0
            for constraint in predecessors_dict[task]:
                # Compute earliest finish time of the predecessor
                predecessor_finish_time = earliest_start.get(constraint, 0) + int(
                    self.__constraint_table_data[int(constraint) - 1][1])
                # Update earliest start time if necessary
                earliest_start_time = max(earliest_start_time, predecessor_finish_time)

            # Update earliest start time of the current task
            earliest_start[task] = earliest_start_time
        return earliest_start

    def compute_latest_dates(self,earliest):
        tasks = {}
        for item in self.__constraint_table_data:
            task_name = item[0]
            duration = int(item[1])
            constraints = item[2].split(', ') if item[2] != 'None' else []
            tasks[task_name] = {
                'duration': duration,
                'constraints': constraints,
                'predecessors': [],
                'earliest': earliest.get(task_name),  # Assuming EST is provided or calculated elsewhere
                'latest': None,
                'float' : None
            }

        for task in tasks:
            for other_task in tasks:
                if task in tasks[other_task]['constraints']:
                    tasks[task]['predecessors'].append(other_task)
        # Calculate EFT based on EST and duration and find the maximum EFT
        max_earliest = 0
        for task, details in tasks.items():
            if details['earliest'] is not None:
                earliest = details['earliest'] + details['duration']
                max_earliest = max(max_earliest, earliest)
            else:
                print(f"Error: EST not set for task {task}")
                return
        for task, details in tasks.items():
            details['latest'] = max_earliest - details['duration']

        sorted_tasks = sorted(tasks.keys())
        for task in reversed(sorted_tasks):
                latest_start = float('inf')
                for successor in tasks:
                    if task in tasks[successor]['constraints']:
                        latest_start = min(latest_start, tasks[successor]['latest'] - tasks[task]['duration'])
                tasks[task]['latest'] = latest_start if latest_start != float('inf') else tasks[task]['earliest']
                tasks[task]['float'] = tasks[task]['latest'] - tasks[task]['earliest']
        for task, details in tasks.items():
            print(f"Task {task}: Earliest Date = {details['earliest']}, Latest Date = {details['latest']}, Float = {details['float']}")



