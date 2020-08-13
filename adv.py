from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# modifies traversal_path directly
def traverse_map(current_room, visited, back_direction=None):
    """ recursive traversal, adds steps to traversal_path as we take them """
    # Add current_room to visited
    visited.add(current_room.id)

    # Are we done visiting every room?
    if len(visited) == len(room_graph):
        return

    # Go into each exit we haven't already visited
    for direction in current_room.get_exits():
        next_room = current_room.get_room_in_direction(direction)
        if next_room.id not in visited:
            # get reverse direction
            if direction == 'n':
                back = 's'
            elif direction == 's':
                back = 'n'
            elif direction == 'e':
                back = 'w'
            else:  # direction == 'w'
                back = 'e'

            # traverse into this room
            traversal_path.append(direction)
            traverse_map(next_room, visited, back)
        
    # traverse back out of this room, if we aren't done yet
    if (back_direction is not None) and (len(visited) != len(room_graph)):
        traversal_path.append(back_direction)
    return

traverse_map(world.starting_room, set())


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
