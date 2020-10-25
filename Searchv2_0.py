from sokoban_map import SokobanMap
import os
import heapq
import operator
import time
from collections.abc import MutableSet

class Search():
    def __init__(self, filename):
        """ Initialises the Sokoban game and creates the first search node. """
        filepath = os.path.join('testcases',filename)
        # Create an instance of the Sokoban game
        self.soko_map = SokobanMap(filepath)
        self.obstacle_map = self.soko_map.obstacle_map
        self.tgt_positions = self.soko_map.tgt_positions

        # Set initial game parameters
        self.starting_box_pos = self.soko_map.box_positions
        self.starting_player_pos = (self.soko_map.player_x,
                                    self.soko_map.player_y)

        # Set this initial game as the first node to explore
        self.startNode = Node(self,self.starting_player_pos[0],
                              self.starting_player_pos[1],
                              self.starting_box_pos)
        self.valid_coordinates = []


    def UniformCostSearch(self):
        """
        Performs UCS on the instance of the Sokoban Game.

        The Priority Queue (pq) is sorted such that the lowest cost nodes are
        stored at the start of the list.
        """
        visitedNodes = NodeSet()
        pq = []
        nodes_generated = 1
        # Insert tuple (cumulative cost, node(id), node, path) into priority queue
        heapq.heappush(pq,(0,id(self.startNode),self.startNode,[]))
      
        while not len(pq)==0:
            cost, node_id, current_node, path = heapq.heappop(pq)
            
            if self.is_complete(current_node):
            # Output path found and number of nodes generated, on fringe, number of nodes explored
                return (path,nodes_generated,len(pq),len(visitedNodes))
            # check node isnt already marked as visited
            
            if current_node not in visitedNodes:
                visitedNodes.add(current_node) 
                # if not self.is_deadlock(current_node):
                if not self.is_deadlock(current_node):
                    # skip children if this condition is unsolvable
                    for child in current_node.get_successors():
                        nodes_generated += 1
                        # add node to unexplored if not already visited
                        heapq.heappush(pq,(cost+1,id(child[0]),
                                           child[0],path+[child[1]]))


    def AStarSearch(self):
        """
        Performs A* on the instance of the Sokoban Game.

        The Priority Queue (pq) is sorted such that the lowest cost nodes are
        stored at the start of the list.
        """
        visitedNodes = NodeSet()
        pq = []
        nodes_generated = 1
        # insert tuple (cumulative cost, node, path) into priority queue
        heapq.heappush(pq,(0, 0, id(self.startNode), self.startNode, []))

        while not len(pq) == 0:
            h_cost, cost, node_id, current_node, path = heapq.heappop(pq)
            
            if self.is_complete(current_node):
                # Output path, nodes generated, nodes on fringe, nodes explored
                return (path, nodes_generated, len(pq), len(visitedNodes))
            
            if current_node not in visitedNodes:
                visitedNodes.add(current_node) 
                # if not self.is_deadlock(current_node):
                if not self.is_deadlock(current_node):
                    # skip children if this condition is unsolvable
                    for child in current_node.get_successors():
                        nodes_generated += 1
                        heapq.heappush(pq,
                                (cost + self.heuristic_cost(child[0]),cost+0.25,
                                id(child[0]), child[0], path + [child[1]]))
    
    # def get_dead_squares(self): # TODO: try to implement this approach. currently not working really
    #     walls = self.obstacle_map
    #     targets = self.tgt_positions
    #     reachable_pos = []
    #     print(targets)
    #     print("Num targets:", len(targets))
        
    #     for (ty, tx) in targets:
    #         print("target at (", tx, ",", ty,")")
    #         by, bx = ty, tx #place box at target

    #         # check which positions box can be pulled to
    #         for pull in ['l','r','u','d']:
    #             #by, bx = ty, tx
    #             if pull == 'l':
    #                 if walls[by][bx-1] != '#':
    #                     bx = bx-1
    #                     reachable_pos.append((bx,by))
    #             if pull == 'r':
    #                 if walls[by][bx+1] != '#':
    #                     bx = bx+1
    #                     reachable_pos.append((bx,by))
    #             if pull == 'u':
    #                 if walls[by-1][bx] != '#':
    #                     by = by-1
    #                     reachable_pos.append((bx,by))
    #             if pull == 'd':
    #                 if walls[by+1][bx] != '#':
    #                     by = by+1
    #                     reachable_pos.append((bx,by))

    #         print(reachable_pos)




    def is_complete(self, node):
        finished = True
        for i in node.box_positions:
            if i not in self.tgt_positions:
                finished = False
        return finished


    def check_on_target(self, bx, by):
        """ Returns True if the box coordinates passed in are on a target. """
        on_target = False
        for (ty, tx) in self.tgt_positions:
            # if the box is on a target, this is fine
            if (bx, by) == (tx, ty):
                on_target = True
        return on_target

    def heuristic_cost(self, node):
        """
        Returns the heuristic cost from root node to current node

        v1.2 - Manhattan distance from box to nearest target
        """
        score = 0
        target_positions = self.tgt_positions[:]
        px, py = node.get_player_pos()
        mintx, minty = 0, 0

        for bx, by in node.box_positions:
            distance = float("inf") # Set distance to be infinity to start
            for tx, ty in target_positions:
                man_dist = abs(bx - tx) + abs(by - ty)
                if man_dist < distance:
                    distance = man_dist
                    mintx, minty = tx, ty
            target_positions.remove((mintx, minty))
            score += distance
        return score

    def is_deadlock(self, node):
        """ Determines whether the game is unwinnable. """
        lvlMap = self.obstacle_map
        boxMap = node.box_positions
        tgtMap = self.tgt_positions
        on_deadlock = False

        for by, bx in tuple(boxMap):
            # Check if box is cornered by walls and or blocks
            if (lvlMap[by][bx - 1] == '#' or (by,bx - 1) in boxMap) or \
            (lvlMap[by][bx + 1] == '#' or (by,bx + 1) in boxMap):
                if (lvlMap[by - 1][bx] == '#' or (by - 1,bx) in boxMap) or \
                (lvlMap[by + 1][bx] == '#' or (by + 1,bx) in boxMap):
                    on_deadlock = True
                
            # Check BB ;  #B  ;  BB  scenarios and their rotations
            #       #B    #B     BB
            elif ((by,bx+1) in boxMap or (by+1,bx) in boxMap):
                 if ((lvlMap[by+1][bx+1] == '#' or (by+1,bx+1) in boxMap) and \
                     (lvlMap[by][bx+1] == '#' or (by,bx+1) in boxMap)) or \
                    ((lvlMap[by+1][bx-1] == '#' or (by+1,bx-1) in boxMap) and \
                     (lvlMap[by][bx-1] == '#' or (by,bx-1) in boxMap)):
                     on_deadlock = True

            elif ((by,bx-1) in boxMap or (by-1,bx) in boxMap):
                 if ((lvlMap[by-1][bx-1] == '#' or (by-1,bx-1) in boxMap) and \
                     (lvlMap[by][bx-1] == '#' or (by,bx-1) in boxMap)) or \
                    ((lvlMap[by-1][bx+1] == '#' or (by-1,bx+1) in boxMap) and \
                     (lvlMap[by][bx+1] == '#' or (by,bx+1) in boxMap)):
                     on_deadlock = True
 
            # check  B# scenario and its rotations
            #       #B
            elif ((by+1,bx) in boxMap and lvlMap[by][bx+1] == '#' and lvlMap[by+1][bx-1] == '#' and lvlMap[by][bx-1] == ' ' and lvlMap[by+1][bx+1] == ' ') or \
                ((by+1,bx) in boxMap and lvlMap[by][bx-1] == '#' and lvlMap[by+1][bx+1] == '#' and lvlMap[by][bx+1] == ' ' and lvlMap[by+1][bx-1] == ' ') or \
                ((by,bx+1) in boxMap and lvlMap[by-1][bx] == '#' and lvlMap[by+1][bx+1] == '#' and lvlMap[by-1][bx+1] == ' ' and lvlMap[by+1][bx] == ' ') or \
                ((by,bx+1) in boxMap and lvlMap[by-1][bx+1] == '#' and lvlMap[by+1][bx] == '#' and lvlMap[by-1][bx] == ' ' and lvlMap[by+1][bx+1] == ' '):
                on_deadlock = True

            
            elif bx+2 < self.soko_map.x_size and by+2 < self.soko_map.y_size and bx-2 >= 0 and by-2 >= 0:
        
                # # check ##  ,  #B ,  ## , B# 
                #         # #   # B   # #   B #
                #          BB   ##    BB     ##
                if (lvlMap[by-1][bx-1] == ' ' and lvlMap[by-1][bx] == '#' and lvlMap[by-1][bx-2] == '#' and lvlMap[by-2][bx-1] == '#' and lvlMap[by-2][bx-2] == '#' and (by, bx-1) in boxMap) or \
                    (lvlMap[by+1][bx-1] == ' ' and lvlMap[by][bx-1] == '#' and lvlMap[by+1][bx-2] == '#' and lvlMap[by+2][bx-1] == '#' and lvlMap[by+2][bx-2] == '#' and (by+1, bx) in boxMap) or \
                    (lvlMap[by-1][bx+1] == ' ' and lvlMap[by-1][bx] == '#' and lvlMap[by-1][bx+2] == '#' and lvlMap[by-2][bx+1] == '#' and lvlMap[by-2][bx+2] == '#' and (by, bx+1) in boxMap) or \
                    (lvlMap[by+1][bx+1] == ' ' and lvlMap[by][bx+1] == '#' and lvlMap[by+1][bx+2] == '#' and lvlMap[by+2][bx+1] == '#' and lvlMap[by+2][bx+2] == '#' and (by+1, bx) in boxMap):
                    on_deadlock = True

                # check ##  , #B  ,  ## , B#
                #       # B   B #   B #  # B
                #        B#    ##   #B   ##
                elif (lvlMap[by][bx+1] == '#' and lvlMap[by-1][bx-1] == '#' and lvlMap[by-2][bx-1] == '#' and lvlMap[by-2][bx] == '#' and (by-1,bx+1) in boxMap) or \
                    (lvlMap[by][bx-1] == '#' and lvlMap[by+1][bx+1] == '#' and lvlMap[by+2][bx+1] == '#' and lvlMap[by+2][bx] == '#' and (by+1,bx-1) in boxMap) or \
                    (lvlMap[by][bx-1] == '#' and lvlMap[by-1][bx+1] == '#' and lvlMap[by-2][bx+1] == '#' and lvlMap[by-2][bx] == '#' and (by-1,bx-1) in boxMap) or \
                    (lvlMap[by][bx+1] == '#' and lvlMap[by+1][bx-1] == '#' and lvlMap[by+2][bx-1] == '#' and lvlMap[by+2][bx] == '#' and (by+1,bx+1) in boxMap):
                    on_deadlock = True

                # check ##  , BB  ,  ## , BB
                #       # B   B #   B #  # B
                #        BB    ##   BB   ##
                elif ((by,bx+1) in boxMap and lvlMap[by-1][bx-1] == '#' and lvlMap[by-2][bx-1] == '#' and lvlMap[by-2][bx] == '#' and (by-1,bx+1) in boxMap) or \
                    ((by,bx-1) in boxMap and lvlMap[by+1][bx+1] == '#' and lvlMap[by+2][bx+1] == '#' and lvlMap[by+2][bx] == '#' and (by+1,bx-1) in boxMap) or \
                    ((by,bx-1) in boxMap and lvlMap[by-1][bx+1] == '#' and lvlMap[by-2][bx+1] == '#' and lvlMap[by-2][bx] == '#' and (by-1,bx-1) in boxMap) or \
                    ((by,bx+1) in boxMap and lvlMap[by+1][bx-1] == '#' and lvlMap[by+2][bx-1] == '#' and lvlMap[by+2][bx] == '#' and (by+1,bx+1) in boxMap):
                    on_deadlock = True

            if on_deadlock:
                # Check if block is on a target
                if not self.check_on_target(bx,by):
                    return True
            

        return False

class NodeSet(MutableSet):
    def __init__(self):
        self.elements = set()

    def __iter__(self):
         return iter(self.elements)

    def __contains__(self, other_node):
        for e in self.elements:
            if e.player_x == other_node.player_x and \
            e.player_y == other_node.player_y and \
            e.box_positions == other_node.box_positions:
                return True
        return False

    def __len__(self):
        return len(self.elements)

    def add(self,item):
        self.elements.add(item)

    def discard(self,item):
        self.elements.remove(item)



class Node(Search):
    def __init__(self, root, player_x, player_y, box_positions):
        self.successors = []
        self.root = root
        self.player_x = player_x
        self.player_y = player_y
        self.box_positions = box_positions
        self.directions = {'u':(0, -1), 'r':( 1, 0), 'd':(0,  1), 'l':(-1, 0)}

    def get_successors(self):
        """
        Generates all states that can be reached from the current state.
        """
        moves = self.get_valid_moves()
        self.successors = [(Node(self.root,moves[m][0],moves[m][1],
                                 moves[m][2]), m) for m in moves]
        return self.successors

    def get_player_pos(self):
        return self.player_x, self.player_y

    def get_valid_moves(self):
        """
        Checks which moves are valid.
        Adapted from supplied code
        """

        valid_moves = {}

        for move, (dx, dy) in self.directions.items():
            new_box_positions = self.box_positions[:]

            if self.root.obstacle_map[self.player_y + dy][self.player_x + dx] == '#':
                continue
            else:
                new_x = self.player_x + dx
                new_y = self.player_y + dy
                if (new_y, new_x) in self.box_positions:
                    if self.root.obstacle_map[new_y + dy][new_x + dx] == '#' or\
                    (new_y + dy, new_x + dx) in self.box_positions:
                        continue
                    else:
                        new_box_positions.remove((new_y, new_x))
                        new_box_positions.append((new_y + dy, new_x + dx))

            valid_moves[move] = (new_x,new_y,new_box_positions)

        return valid_moves
        

