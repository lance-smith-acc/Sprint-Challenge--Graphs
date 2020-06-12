from room import Room
from player import Player
from world import World
from util import Stack

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
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Helper function, return the path traversed as we traverse it
def travel_path(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'

def nextRoom(room):
    return player.current_room.get_room_in_direction(room)

# Set the stack for our paths
paths = Stack()
visited = set()

# While we haven't visited all the rooms
while len(visited) < len(world.rooms):

    # Reset the path
    path = []
    # Set the exits for the current room
    exits = player.current_room.get_exits()
    # Visit the current room
    visited.add(player.current_room)
   
    # For each exit in the current room, add the exit to the path if we haven't visited it yet
    for exit in exits:
        if nextRoom(exit) not in visited:
            path.append(exit)
    
    # If found a new path, move to one of the unvisited rooms at random and update our path
    if len(path) > 0:
        move = random.randint(0, len(path) - 1)
        paths.push(path[move])
        traversal_path.append(path[move])
        player.travel(path[move])

    # If we've run out of path to explore, back it up
    else:
        deadEnd = paths.pop()
        traversal_path.append(travel_path(deadEnd))
        player.travel(travel_path(deadEnd))
        


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
