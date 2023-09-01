import numpy as np
from collections import deque

INFINITY = float("inf")


def write_road_nodes_to_file(file, pts):
    for i in range(len(pts) - 1):
        pt1 = (pts[i][0], pts[i][1], pts[i][2])
        pt2 = (pts[i + 1][0], pts[i + 1][1], pts[i + 1][2])
        dist = np.sqrt(
            np.power(pt1[0] - pt2[0], 2)
            + np.power(pt1[1] - pt2[1], 2)
            + np.power(pt1[2] - pt2[2], 2)
        )
        file.write(str(pt1) + "; ")
        file.write(str(pt2) + "; ")
        file.write(str(dist) + "\n")


# https://github.com/dmahugh/dijkstra-algorithm
class Graph:
    def __init__(self, filename, split_symbol="; "):
        """Reads graph definition and stores it. Each line of the graph
        definition file defines an edge by specifying the start node,
        end node, and distance, delimited by spaces.
        Stores the graph definition in two properties which are used by
        Dijkstra's algorithm in the shortest_path method:
        self.nodes = set of all unique nodes in the graph
        self.adjacency_list = dict that maps each node to an unordered set of
        (neighbor, distance) tuples.
        """

        # Read the graph definition file and store in graph_edges as a list of
        # lists of [from_node, to_node, distance]. This data structure is not
        # used by Dijkstra's algorithm, it's just an intermediate step in the
        # creation of self.nodes and self.adjacency_list.
        graph_edges = []
        with open(filename) as fhandle:
            for line in fhandle:
                edge_from, edge_to, cost, *_ = line.strip().split(split_symbol)
                graph_edges.append((edge_from, edge_to, float(cost)))

        self.nodes = set()
        for edge in graph_edges:
            self.nodes.update([edge[0], edge[1]])

        self.adjacency_dict = {node: set() for node in self.nodes}
        for edge in graph_edges:
            self.adjacency_dict[edge[0]].add((edge[1], edge[2]))


    def shortest_path(self, start_node, end_node):
        """Uses Dijkstra's algorithm to determine the shortest path from
        start_node to end_node. Returns (path, distance).
        """

        is_start_node_valid = start_node in self.nodes
        assert is_start_node_valid, f"Failed to locate the start coordinate: not in the graph."
        is_end_node_valid = end_node in self.nodes
        assert is_end_node_valid, f"Failed to locate the end coordinate: not in the graph."
        unvisited_nodes = self.nodes.copy()  # All nodes are initially unvisited.

        # Create a dictionary of each node's distance from start_node. We will
        # update each node's distance whenever we find a shorter path.
        distance_from_start = {
            node: (0 if node == start_node else INFINITY) for node in self.nodes
        }

        # Initialize previous_node, the dictionary that maps each node to the
        # node it was visited from when the the shortest path to it was found.
        previous_node = {node: None for node in self.nodes}

        while unvisited_nodes:
            # Set current_node to the unvisited node with shortest distance
            # calculated so far.
            current_node = min(
                unvisited_nodes, key=lambda node: distance_from_start[node]
            )
            unvisited_nodes.remove(current_node)

            # If current_node's distance is INFINITY, the remaining unvisited
            # nodes are not connected to start_node, so we're done.
            if distance_from_start[current_node] == INFINITY:
                break

            # For each neighbor of current_node, check whether the total distance
            # to the neighbor via current_node is shorter than the distance we
            # currently have for that node. If it is, update the neighbor's values
            # for distance_from_start and previous_node.
            for neighbor, distance in self.adjacency_dict[current_node]:
                new_path = distance_from_start[current_node] + distance
                if new_path < distance_from_start[neighbor]:
                    distance_from_start[neighbor] = new_path
                    previous_node[neighbor] = current_node

            if current_node == end_node:
                break  # we've visited the destination node, so we're done

        # To build the path to be returned, we iterate through the nodes from
        # end_node back to start_node. Note the use of a deque, which can
        # appendleft with O(1) performance.
        path = deque()
        current_node = end_node
        while previous_node[current_node] is not None:
            path.appendleft(current_node)
            current_node = previous_node[current_node]
        path.appendleft(start_node)

        return path, distance_from_start[end_node]


if __name__ == '__main__':
    #     filename = graph definition file
    #     start/end = path to be calculated
    #     path = shortest path
    #     distance = distance of path

    filename = "road_nodes.txt"
    split_symbol = "; "
    # start_node_x = input("Please enter the START x-coordinate: ")
    # start_node_y = input("Please enter the START y-coordinate: ")
    # start_node_z = input("Please enter the START z-coordinate: ")
    # start_node = "(" + start_node_x + ", " + start_node_y + ", " + start_node_z + ")"
    start_node = input("Please enter the START coordinate in \"(x, y, z)\": ")
    print(f'You entered START node is {start_node}')
    # end_node_x = input("Please enter the END x-coordinate: ")
    # end_node_y = input("Please enter the END y-coordinate: ")
    # end_node_z = input("Please enter the END z-coordinate: ")
    # end_node = "(" + end_node_x + ", " + end_node_y + ", " + end_node_z + ")"
    end_node = input("Please enter the END coordinate in \"(x, y, z)\": ")
    print(f'You entered END node is {end_node}')

    graph = Graph(filename, split_symbol)
    path, distance = graph.shortest_path(start_node, end_node)

    print('The shortest path: {0}'.format(path))
    print('The total distance: {0}'.format(distance))
