import sys

def readGraph(arr):
    graph = [[]*len(arr)] * len(arr)
    for i in range(len(arr)):
        graph[i] = [int(s) for s in (arr[i].split(","))]
    return graph


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

        # for checking if the queue is empty
    def empty(self):
        return len(self.queue) == 0


    def size(self):
        return len(self.queue)

    # for inserting an element in the queue
    def put(self, pCost, node, createTime, pref):
        self.queue.append((pCost, node, createTime, pref))

    # for popping an element based on Priority
    def get(self):
        try:
            prio = 0
            for i in range(len(self.queue)):
                if self.queue[i][0] < self.queue[prio][0]:
                    prio = i
                elif self.queue[i][0] == self.queue[prio][0]:
                    if self.queue[i][2] < self.queue[prio][2]:
                        prio = i
                    elif self.queue[i][2] == self.queue[prio][2]:
                        if self.queue[i][3] < self.queue[prio][3]:
                            prio = i
            item = self.queue[prio]
            del self.queue[prio]
            return item
        except IndexError:
            exit()

    # Check if a neighbor should be added to open list
    def add_to_open(self, neighbor):
        for i in range(len(self.queue)):
            if neighbor.node == self.queue[i][1].node and neighbor.f >= self.queue[i][1].f:
                return False
        return True



class Node:
    def __init__(self, node, graph):
        self.node = node
        self.x = node[0]
        self.y = node[1]
        self.cost = graph[self.x][self.y]
        self.neighbors = []
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = None

    def add_neighbour(self, node):
        self.neighbors.append(node)



def DLS(graph, node, goal, limit, count):
    frontier = [node]
    while len(frontier) != 0:
        node = frontier.pop(0)
        count += 1
        if node.node == goal.node:
            return node, count
        if node.g < limit:
            node.neighbors.clear()
            find_neighbors(node,graph)
            for child in node.neighbors:
                child.g = (node.g + 1)
                child.parent = node
            newFront = node.neighbors
            newFront.extend(frontier)
            frontier = newFront
    return None,count


def dfs_f(node, path, posPath, f_limit, goal, graph, globalCount, count):
    node.h = abs(goal.x - node.x) + abs(goal.y - node.y)
    new_f = node.g + node.h
    if count >= 20:
        print("ok")
        return new_f, path, False, globalCount
    if new_f > f_limit:
        return new_f, path, True, globalCount
    if node.node == goal.node:
        return "PATH FOUND", path, True, globalCount
    min = sys.maxsize
    node.neighbors.clear()
    find_neighbors(node, graph)
    for child in node.neighbors:
        path.append(child)
        posPath.append(child.node)
        child.g = child.cost + node.g
        count += 1
        solution, path, loop, globalCount = dfs_f(child, path, posPath, f_limit, goal, graph, globalCount+1, count)
        if solution == "PATH FOUND":
            return "PATH FOUND", path, True, globalCount
        elif loop == False:
            return solution, path, False, globalCount
        elif solution < min:
            min = solution
        path.pop()
        posPath.pop()
    return min, path, True, globalCount



def find_neighbors(node,graph):
    if node.x == 0 and node.y == 0 and len(graph) != 1:
        n1 = Node([0, 1], graph)
        n2 = Node([1, 1], graph)
        n3 = Node([1, 0], graph)
        if n1.cost != -1:
            node.add_neighbour(n1)
        if n2.cost != -1 and n1.cost != -1 and n3.cost != -1:
            node.add_neighbour(n2)
        if n3.cost !=-1:
            node.add_neighbour(n3)
    elif node.x == 0 and node.y > 0:
        n3 = Node([1, node.y], graph)
        n4 = Node([1, node.y - 1], graph)
        n5 = Node([0, node.y - 1], graph)
        if node.y < len(graph) - 1:
            n1 = Node([0, node.y+1], graph)
            n2 = Node([1, node.y+1], graph)
            if n1.cost != -1:
                node.add_neighbour(n1)
            if n2.cost != -1 and n1.cost != -1 and n3.cost != -1:
                node.add_neighbour(n2)
        if n3.cost != -1:
            node.add_neighbour(n3)
        if n4.cost != -1 and n3.cost != -1 and n5.cost != -1:
            node.add_neighbour(n4)
        if n5.cost != -1:
            node.add_neighbour(n5)
    elif node.y == 0 and node.x > 0:
        n1 = Node([node.x, 1], graph)
        n7 = Node([node.x-1, 0], graph)
        n8 = Node([node.x-1, node.y + 1], graph)
        if n1.cost != -1:
            node.add_neighbour(n1)
        if node.x < len(graph) - 1:
            n2 = Node([node.x+1, node.y+1], graph)
            n3 = Node([node.x+1, 0], graph)
            if n2.cost != -1 and n1.cost != -1 and n3.cost != -1:
                node.add_neighbour(n2)
            if n3.cost != -1:
                node.add_neighbour(n3)
        if n7.cost != -1:
            node.add_neighbour(n7)
            if n8.cost != -1 and n1.cost != -1:
                node.add_neighbour(n8)
    elif node.x == len(graph) - 1 and node.y == len(graph) - 1 and len(graph) != 1:
        n5 = Node([node.x, node.y-1], graph)
        n6 = Node([node.x-1, node.y-1], graph)
        n7 = Node([node.x-1, node.y],graph)
        if n5.cost != -1:
            node.add_neighbour(n5)
        if n6.cost != -1 and n5.cost != -1 and n7.cost != -1:
            node.add_neighbour(n6)
        if n7.cost != -1:
            node.add_neighbour(n7)
    elif node.x == len(graph)-1 and node.y != len(graph)-1:
        n1 = Node([node.x, node.y+1],graph)
        n5 = Node([node.x, node.y-1],graph)
        n6 = Node([node.x-1, node.y-1],graph)
        n7 = Node([node.x-1, node.y],graph)
        n8 = Node([node.x-1, node.y+1],graph)
        if n1.cost != -1:
            node.add_neighbour(n1)
        if n5.cost != -1:
            node.add_neighbour(n5)
            if n6.cost != -1 and n7.cost != -1:
                node.add_neighbour(n6)
        if n7.cost != -1:
            node.add_neighbour(n7)
            if n8.cost != -1 and n1.cost != -1:
                node.add_neighbour(n8)
    elif node.y == len(graph)-1 and node.x != len(graph)-1:
        n3 = Node([node.x + 1, node.y], graph)
        n4 = Node([node.x+1, node.y - 1], graph)
        n5 = Node([node.x, node.y - 1], graph)
        n6 = Node([node.x - 1, node.y - 1], graph)
        n7 = Node([node.x - 1, node.y], graph)
        if n3.cost != -1:
            node.add_neighbour(n3)
            if n4.cost != -1 and n5.cost != -1:
                node.add_neighbour(n4)
        if n5.cost !=-1:
            node.add_neighbour(n5)
            if n6.cost != -1 and n7.cost != -1:
                node.add_neighbour(n6)
        if n7.cost != -1:
            node.add_neighbour(n7)
    elif node.y != len(graph)-1 and node.x != len(graph)-1:
        n1 = Node([node.x, node.y + 1], graph)
        n2 = Node([node.x + 1, node.y + 1], graph)
        n3 = Node([node.x + 1, node.y], graph)
        n4 = Node([node.x+1, node.y - 1], graph)
        n5 = Node([node.x, node.y - 1], graph)
        n6 = Node([node.x - 1, node.y - 1], graph)
        n7 = Node([node.x - 1, node.y], graph)
        n8 = Node([node.x-1, node.y+1], graph)
        if n1.cost != -1:
            node.add_neighbour(n1)
            if n2.cost != -1 and n3.cost != -1:
                node.add_neighbour(n2)
        if n3.cost != -1:
            node.add_neighbour(n3)
            if n4.cost != -1 and n5.cost != -1:
                node.add_neighbour(n4)
        if n5.cost != -1:
            node.add_neighbour(n5)
            if n6.cost != -1 and n7.cost != -1:
                node.add_neighbour(n6)
        if n7.cost != -1:
            node.add_neighbour(n7)
            if n8.cost != -1 and n1.cost != -1:
                node.add_neighbour(n8)


def find_path(nodePath):
    strPath = ""
    for i in range(1,len(nodePath)):
        if nodePath[i].x == nodePath[i-1].x:
            if nodePath[i].y == nodePath[i-1].y + 1:
                strPath += "R"
            elif nodePath[i].y == nodePath[i-1].y - 1:
                strPath += "L"
        elif nodePath[i].y == nodePath[i-1].y:
            if nodePath[i].x == nodePath[i-1].x + 1:
                strPath += "D"
            elif nodePath[i].x == nodePath[i-1].x - 1:
                strPath += "U"
        elif nodePath[i].x == nodePath[i-1].x + 1:
            if nodePath[i].y == nodePath[i-1].y + 1:
                strPath += "RD"
            elif nodePath[i].y == nodePath[i-1].y - 1:
                strPath += "LD"
        elif nodePath[i].x == nodePath[i-1].x - 1:
            if nodePath[i].y == nodePath[i-1].y + 1:
                strPath += "RU"
            elif nodePath[i].y == nodePath[i-1].y - 1:
                strPath += "LU"
        strPath += "-"
    strPath = strPath[:len(strPath)-1]
    return strPath