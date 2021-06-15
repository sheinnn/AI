import sys
import help


def ids(src, target, maxDepth, graph):
    count = 0
    for i in range(1, maxDepth):
        found, count = help.DLS(graph, src, target, i, count)
        if found is not None:
            totalCost = found.g
            path_to_goal = [found]  # the path to the goal ends with the current node (obviously)
            prev_node = found  # set the previous node to be the current node (this will changed with each iteration)

            while prev_node.node != src.node:  # go back up the path using parents, and add to path
                parent = prev_node.parent
                path_to_goal.append(parent)
                prev_node = parent

            path_to_goal.reverse()  # reverse the path
            strPath = help.find_path(path_to_goal)
            s = " "
            seq = (strPath, str(totalCost), str(count))
            output = s.join(seq)
            return output
    return "no path"



def ucs(graph, start, goal):
    visited = [start.node]  # list of visited nodes
    q = help.PriorityQueue()  # we store vertices in the (priority) queue as tuples with cumulative cost
    q.put(0, start, 0, 0)  # add the starting node, this has zero *cumulative* cost
    parents = {start: None}  # this dictionary contains the parent of each node, necessary for path construction
    totalNode = 0
    while not q.empty():  # while the queue is nonempty
        dequeued_item = q.get()
        current_node = dequeued_item[1]  # get node at top of queue
        current_node_priority = dequeued_item[0]  # get the cumulative priority for later

        if current_node.node == goal.node:  # if the current node is the goal
            totalCost = current_node_priority
            path_to_goal = [current_node]  # the path to the goal ends with the current node (obviously)
            prev_node = current_node  # set the previous node to be the current node (this will changed with each iteration)

            while prev_node != start:  # go back up the path using parents, and add to path
                parent = parents[prev_node]
                path_to_goal.append(parent)
                prev_node = parent

            path_to_goal.reverse()  # reverse the path
            strPath = help.find_path(path_to_goal)
            s = " "
            seq = (strPath, str(totalCost), str(totalNode))
            output = s.join(seq)
            return  output # return it

        else:
            pref = 0
            help.find_neighbors(current_node, graph)
            for child in current_node.neighbors:  # otherwise, for each adjacent node
                if child.node not in visited:  # if it is not visited
                    visited.append(child.node)  # mark it as visited
                    parents[child] = current_node  # set the current node as the parent of child
                    q.put(current_node_priority + child.cost, child, totalNode, pref)  # and enqueue it with *cumulative* priority
                pref += 1
        totalNode += 1
    return "no path"


def aStar(graph, start, goal):
    # Create lists for open nodes and closed nodes
    open = help.PriorityQueue()
    closed = []
    # Add the start node
    open.put(0, start, 0, 0)
    parents = {start: None}  # this dictionary contains the parent of each node, necessary for path construction
    totalNode = 0
    # Loop until the open list is empty
    while not open.empty():
        # Get the node with the lowest cost
        dequeued_item = open.get()
        current_node = dequeued_item[1]  # get node at top of queue
        f = dequeued_item[0]
        # Add the current node to the closed list
        closed.append(current_node.node)

        # Check if we have reached the goal, return the path
        if current_node.node == goal.node:
            totalCost = current_node.g
            path_to_goal = [current_node]  # the path to the goal ends with the current node (obviously)
            prev_node = current_node  # set the previous node to be the current node (this will changed with each iteration)

            while prev_node != start:  # go back up the path using parents, and add to path
                parent = parents[prev_node]
                path_to_goal.append(parent)
                prev_node = parent

            path_to_goal.reverse()  # reverse the path
            strPath = help.find_path(path_to_goal)
            s = " "
            seq = (strPath, str(totalCost), str(totalNode))
            output = s.join(seq)
            return output  # return it
        pref = 0
        # Loop neighbors
        help.find_neighbors(current_node, graph)
        for child in current_node.neighbors:
            # Check if the neighbor is in the closed list
            if child.node not in closed:
                # Generate heuristics (Manhattan distance)
                child.g = current_node.g + child.cost
                child.h = abs(goal.x - child.x) + abs(goal.y - child.y)
                child.f = child.g + child.h
                # Check if neighbor is in open list and if it has a lower f value
                if open.add_to_open(child):
                    # Everything is green, add neighbor to open list
                    open.put(child.f, child, totalNode, pref)
                    parents[child] = current_node  # set the current node as the parent of child
                pref += 1
        totalNode += 1
    # Return None, no path is found
    return "no path"


def idaStar(start, goal, graph):
    loop =True
    start.h = abs(goal.x - start.x) + abs(goal.y - start.y)
    limit = start.h
    path = [start]
    posPath = [start.node]
    start.g = 0
    start.f = start.h
    globalCount = 0
    while loop:
        count = 0
        found, solution, loop, globalCount= help.dfs_f(start, path,posPath, limit, goal, graph, globalCount, count)
        if found == "PATH FOUND":
            totalCost = solution[-1].g
            strPath = help.find_path(solution)
            s = " "
            seq = (strPath, str(totalCost), str(globalCount))
            output = s.join(seq)
            return output  # return
        if found == sys.maxsize:
            return "no path"
        limit = found
    return "no path"


def dispatch():
    result= ""
    f = open("input.txt", "r")
    algoType = str(f.readline().strip())
    src = [int(s) for s in ((f.readline().strip()).split(","))]
    target = [int(s) for s in ((f.readline().strip()).split(","))]
    size = int(f.readline())
    arr = []
    for x in range(size):
        arr.append(f.readline().strip())
    f.close()
    graph = help.readGraph(arr)
    start = help.Node(src, graph)
    goal = help.Node(target, graph)
    if algoType == 'IDS':
        result = ids(start, goal, 20, graph)
    elif algoType == "UCS":
        result = ucs(graph, start, goal)
    elif algoType == "ASTAR":
        result = aStar(graph, start, goal)
    elif algoType == "IDASTAR":
        result = idaStar(start, goal, graph)
    file = open("output.txt", "w")
    file.write(result)
    file.close()

dispatch()
