from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def build_graph(current_room, graph):
    """ recursive depth first traversal, builds the traversal_graph """
    # Add current_room to the graph
    graph[current_room.id] = {}

    # Go into each exit we haven't already visited
    for direction in current_room.get_exits():
        # get the room in that direction
        next_room = current_room.get_room_in_direction(direction)

        # add it to current_room's graph entry
        graph[current_room.id][next_room.id] = direction

        # if we haven't visited next_room yet, do so
        if next_room.id not in graph:
            build_graph(next_room, graph)
        
    return graph

# traveral_graph is structure {0: {4: 'n', 8: 's', 3: 'w', 1: 'e'}, ...}
# keys are the room id's, values are a dict of connected rooms and the directions they are in
traversal_graph = build_graph(player.current_room, {})

print(traversal_graph)

def find_closest_unvisited(start_room, visited):
    """
    performs a breath-first search
    returns the path to the closest unvisited room as a list of room id's
    """
    # Set up the queue and a visited set for this search
    v = set()
    q = deque()
    q.append([start_room])  # queue contains path lists

    while len(q) > 0:
        path = q.popleft()
        v.add(path[-1]) # mark this room as visited for the bfs
        
        # if this room isn't in visited, return the path to it
        if path[-1] not in visited:
            return path

        # else, add neighbors to the queue
        for room in traversal_graph[path[-1]].keys():
            if room not in v:
                new_path = path.copy()
                new_path.append(room)
                q.append(new_path)

# Fill traversal_path
traversal_path = []
visited = set()
visited.add(player.current_room.id)
while len(visited) < len(traversal_graph): # loop until we've visited every room
    # Find the path to the closest unvisited room
    next_path = find_closest_unvisited(player.current_room.id, visited)

    # Move along that path (first room in next_path is the room we're already in)
    for room in next_path[1:]:
        next_move = traversal_graph[player.current_room.id][room]
        traversal_path.append(next_move)
        player.travel(next_move)

    # Mark this room as visited
    visited.add(player.current_room.id)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
