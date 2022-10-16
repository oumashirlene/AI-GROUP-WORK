import networkx as nx

#####################################################################################################
#POPULATING THE GRAPH WITH NODES AND THEIR WEIGHTED EDGES
#####################################################################################################

def populateGraph():
    # Add All The Nodes To The Graph In Positions Similar To The Representation
        # 'pos' variable dictates where each node is drawn
    G.add_node('SportsComplex', pos=(0,6))
    G.add_node('Siwaka', pos=(2,6))
    G.add_node('Phase1A', pos=(4,6))
    G.add_node('Phase1B', pos=(4,4))
    G.add_node('STC', pos=(4,2))
    G.add_node('Phase2', pos=(6,4))
    G.add_node('J1', pos=(8,4))
    G.add_node('Phase3', pos=(8,2))
    G.add_node('ParkingLot', pos=(8,0))
    G.add_node('Mada', pos=(10,4))

    # Add All The Edges
        # G.add_edge(source, target, weight)
    G.add_edge('SportsComplex', 'Siwaka', weight=450)
    G.add_edge('Siwaka', 'Phase1A', weight=10)
    G.add_edge('Siwaka', 'Phase1B', weight=230)
    G.add_edge('Phase1A', 'Phase1B', weight=100)
    G.add_edge('Phase1A', 'Mada', weight=850)
    G.add_edge('Phase1B', 'Phase2', weight=112)
    G.add_edge('Phase1B', 'STC', weight=50)
    G.add_edge('Phase2', 'J1', weight=600)
    G.add_edge('Phase2', 'Phase3', weight=500)
    G.add_edge('STC', 'Phase2', weight=50)
    G.add_edge('STC', 'ParkingLot', weight=250)
    G.add_edge('J1', 'Mada', weight=200)
    G.add_edge('Phase3', 'ParkingLot', weight=350)
    G.add_edge('Mada', 'ParkingLot', weight=700)

#####################################################################################################
#BREADTH FIRST SEARCH
#####################################################################################################

def bfs(startNode, goal):
    explored = {}
    frontier = []
    bfs_result = []

    # Add all the nodes in the graph to the 'explored' dictionary with a value of 'False'
    for node in G.nodes:
        explored[node] = False
    
    # Change the startNode to True in the 'explored' dictionary
    explored[startNode] = True
    frontier.append(startNode) # Add startNode to end of the list (queue structure)

    # while the frontier is not empty
    while frontier:
        curr_node = frontier.pop(0) # Pop the first element in the list (queue structure)
        bfs_result.append(curr_node)

        if curr_node == goal:
            return bfs_result

        for node in G.neighbors(curr_node):
            if not explored[node]:
                explored[node] = True
                frontier.append(node)

    # Return false if no path is found
    return False

def drawBFS():
    # Generate BFS Path From The Sports Complex To Parking Lot
    bfs_path = bfs('SportsComplex', 'ParkingLot')

    if bfs_path == False:
        print('Path Not Found!')
        return 0
    
    print('BFS Traversal Path: ', '->'.join(bfs_path))
    color_map = []
    # for all the nodes in the graph, assign the color green if it's part of the path , else, blue
    for node in G.nodes:
        if node in bfs_path:
            color_map.append('green')
        else:
            color_map.append('blue')
    
    # Draw the Graph
    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, verticalalignment='bottom')
    nx.draw(G, pos, node_size=2500, node_color=color_map, with_labels=True)
    plt.title('BREADTH FIRST SEARCH TRAVERSAL PATH(GREEN)')
    plt.show()

#####################################################################################################
# UNIFORM COST SEARCH
#####################################################################################################

def path_cost(path):
    total_cost = 0
    for (node, cost) in path:
        total_cost += cost
    return total_cost, path[-1][0] # Return total cost and the label of the last node in the path

def ucs(startNode, goal):
    explored = {}
    frontier = [[(startNode, 0)]]

    # Add all the nodes in the graph to the 'explored' dictionary with a value of 'False'
    for node in G.nodes:
        explored[node] = False
    
    # While the frontier is not empty
    while frontier:
        # sort the frontier(ascending) by the cost of the path
        frontier.sort(key=path_cost)
        ucs_result = frontier.pop(0) # Pop the one with the least cost
        curr_node = ucs_result[-1][0] # The current node is the last node in the ucs path

        if explored[curr_node]:
            continue
        
        explored[curr_node] = True

        if curr_node == goal:
            return ucs_result
        else:
            for node in G.neighbors(curr_node):
                new_path = ucs_result.copy()
                new_path.append((node, G[curr_node][node]['weight']))
                frontier.append(new_path)
    
    # return false if path is not found
    return False

def drawUCS():
    # Generate UCS Path From The Sports Complex To Parking Lot
    ucs_path = ucs('SportsComplex', 'ParkingLot')

    if ucs_path == False:
        print('Path Not Found!')
        return 0
    
    ucs_path_fin = []
    # ucs_path holds data eg: ('Siwaka', 450) so need to parse out the node labels without the cost
    for i in range(len(ucs_path)):
        ucs_path_fin.append(ucs_path[i][0])

    print('UCS Traversal Path: ', '->'.join(ucs_path_fin))
    color_map = []
    # for all the nodes in the graph, assign the color green if it's part of the path , else, blue
    for node in G.nodes:
        if node in ucs_path_fin:
            color_map.append('green')
        else:
            color_map.append('blue')
    
    # Draw the Graph
    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, verticalalignment='bottom')
    nx.draw(G, pos, node_size=2500, node_color=color_map, with_labels=True)
    plt.title('UNIFORM COST SEARCH TRAVERSAL PATH(GREEN)')
    plt.show()

#####################################################################################################

#####################################################################################################

# Create A Graph And Assign It To 'G' Variable
G = nx.Graph()
populateGraph()

# Dialogue Options To Choose Which Path The User Wants To See
isValid = False
while not isValid:
    choice = input('Enter 1 for BFS Path or 2 for UCS Path: ')
    if choice == '1':
        isValid = True
        drawBFS()
    elif choice == '2':
        isValid = True
        drawUCS()
    else:
        print('Invalid Choice!! Try Again!')