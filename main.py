import numpy as np
import matplotlib.pyplot as plt
from map_gen import generate_blank_world, generate_forest, generate_rivers, generate_roads, display_world,generate_towns, generate_dungeon

# Set the world size
world_size = 50

# Generate a blank world
world = generate_blank_world(world_size)

# Generate features on the world
generate_forest(world, num_trees=200, max_age=10, spread_probability=1)
generate_rivers(world,num_rivers=10, max_length=500, flow_deviation=0.8, cluster_radius=1)

# Generate towns on the world in clearings near water
town_locations = generate_towns(world, num_towns=10, min_distance=5, marker='s', color='red')

# Generate roads connecting all towns
generate_roads(world, town_locations)


# Generate a dungeon
dungeon_location = generate_dungeon(world, towns=town_locations, min_distance=5, marker='X', color='purple')

# Display the world with towns and roads
display_world(world, title="World with Towns and Roads")
