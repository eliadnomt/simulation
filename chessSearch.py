"""
    Author: Cordelia Montgomery
    Date: Friday 23 October 2020
"""

class Board():
    def __init__(self):
        self.centre_nodes = []
        self.adjacent_nodes = []
        self.converted_nodes = {}
        self.occupied_nodes = {}

    def find_centres(self):
        """ Finds the centre node IDs of a 8x8 board"""
        self.centre_nodes = []
        board_length = 8
        root = (board_length * 2) + 1

        for i in range(root, (board_length + 1) * 2 * root, 2 * root):
            for j in range(2, 2 * (board_length + 1), 2):
                self.centre_nodes.append(i + j)
        return self.centre_nodes

    def pos_convert(self):
        """ Makes a dictionary of all positions where e.g. key = 'A5', value = 121"""
        pos_list = open("locations.txt", "r")
        location = []
        for x in pos_list:
            location.append(x[:2])

        for i in range(0, len(location)):
            self.converted_nodes[location[i]] = self.centre_nodes[i]

        pos_list.close()
        return self.converted_nodes

    def obstacle_pos_convert(self):
        """ Takes in obstacles as letter+number and converts to our node system"""
        ob_list = open("occupied.txt", "r")
        obstacles = []
        for x in ob_list:
            obstacles.append(x[:2])

        for node in obstacles:
            self.occupied_nodes[node] = self.converted_nodes[node]
        ob_list.close()
        return self.occupied_nodes

    def find_adjacents(self, centre_node):
        """ Finds the adjacent node IDs to a single centre node """
        ul = centre_node - 18
        um = centre_node - 17
        ur = centre_node - 16
        l = centre_node - 1
        r = centre_node + 1
        bl = centre_node + 16
        bm = centre_node + 17
        br = centre_node + 18
        adjacent = [ul, um, ur, l, r, bl, bm, br]

        for node in adjacent:
            self.adjacent_nodes.append(node)

        return self.adjacent_nodes


class Search(Board):
    def __init__(self, board_pos):
        self.board_pos = board_pos



class ShortestPath(Search):
    def __init__(self, source, dest, board_pos):
        self.available = []
        self.source = source
        self.dest = dest
        self.board_pos = board_pos
        self.directions = {'um': (0, -1), 'ul': (-1, -1), 'ur': (1, -1), \
                           'l': (-1, 0), 'r':(1, 0), \
                           'bm':(0, 1), 'bl': (-1, 1), 'br':(1, 1)}

    def get_valid_moves(self):
        valid_moves = {}

        for move, (dx, dy) in self.directions.items():
            new_board_pos = self.board_pos[:]


    def get_available(self):
        """
        Generates all locations that can be reached from the current location
        """


#    def findCost(self, path):
chess = Board()
cen = chess.find_centres()
print(len(cen))
print("All node IDs are", chess.pos_convert())
print("Occupied node IDs are", chess.obstacle_pos_convert())
print("Adjacent to node A8 are", chess.find_adjacents(cen[0]))



