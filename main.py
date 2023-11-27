import numpy as np
import matplotlib.pyplot as plt
from map_gen import generate_blank_world, generate_forest, generate_rivers, generate_roads, display_world_with_info,generate_towns, generate_dungeon, generate_bandit_camps, generate_goblin_camps, generate_town_info,simulate_population_growth
from game import main
# Set the world size
world_size = 100




# Generate a blank world
world = generate_blank_world(world_size)

# Generate features on the world
generate_forest(world, num_trees=500, max_age=20, spread_probability=1, world_size=100)
generate_rivers(world,num_rivers=20, max_length=1000, flow_deviation=0.8, cluster_radius=1,world_size=100)

# Generate towns on the world in clearings near water
town_locations = generate_towns(world, num_towns=100, min_distance=3, marker='s', color='red',world_size=100)

# Generate town information
towns_info = generate_town_info(world, town_locations)

# Generate roads connecting all towns
generate_roads(world, town_locations)

generate_bandit_camps(world, num_bandit_camps=100, min_distance=1, marker='^', color='orange',world_size=100)
generate_goblin_camps(world, num_goblin_camps=500, min_distance=1, marker='v', color='green',world_size=100)

# Generate a dungeon
dungeon_location = generate_dungeon(world, towns=town_locations, min_distance=5, marker='X', color='purple')

# Display the world with towns and roads
#display_world_with_info(world, towns_info, title="World with Features")

main(world,towns_info)
