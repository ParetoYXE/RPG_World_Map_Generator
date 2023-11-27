import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from scipy.sparse.csgraph import minimum_spanning_tree
from matplotlib.patches import Ellipse

fig, ax = plt.subplots()
# Example name array
name_array = ["Oaksville", "Maplewood", "Riverdale", "Hilltop", "Meadowbrook", "Greenville",  "Cedarville", "Meadowridge", "Stonehaven", "Harborview", "Maplewood", "Greenfield",
    "Silverbrook", "Pinecrest", "Willowgrove", "Clearwater", "Hillside", "Frostholm",
    "Sunset Valley", "Brookside", "Riverside", "Falcon's Nest", "Oakhaven", "Highland",
    "Moonlight Hollow", "Whitewood", "Starlight Peaks", "Grassland", "Elmwood",
    "Dawn's Haven", "Shadow Springs", "Goldenfields", "Birchwood", "Stormwatch",
    "Sylvan Glade", "Silvermere", "Crimson Hollow", "Bluewater", "Ivydale", "Wheatridge",
    "Wildwood", "Thunderpeak", "Shadowmere", "Autumn Ridge", "Duskwood", "Firelight",
    "Emberfall", "Frostfall", "Summerhaven", "Springbrook", "Mistwood", "Willowridge",
    "Ironforge", "Rusthaven", "Windy Hollow", "Snowpeak"]

def generate_blank_world(size):
    return np.zeros((size, size))


def display_world_with_info(world, towns_info, title="World"):

    for y in range(world.shape[0]):
        for x in range(world.shape[1]):
            if world[y, x] == 1.0:
                ellipse = Ellipse((x + 0.5, y + 0.5), width=0.8, height=0.8, angle=0, color='green')
                ax.add_patch(ellipse)
            elif world[y, x] == -1.0:
                ellipse = Ellipse((x + 0.5, y + 0.5), width=0.8, height=0.8, angle=0, color='blue')
                ax.add_patch(ellipse)

    for town_info in towns_info:
        town_x, town_y = town_info['position']
        town_name = town_info['name']
        town_population = town_info['population']

        # Place text beside the town marker
        plt.text(town_x + 0.5, town_y + 0.5, f"{town_name}\nPop: {town_population}", color='black', ha='right', va='bottom')

    ax.set_xlim(0, world.shape[1])
    ax.set_ylim(0, world.shape[0])
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.title(title)

    plt.show()

def generate_forest(world, num_trees=150, max_age=10, spread_probability=0.2,world_size=50):
    tree_age = np.zeros((world_size, world_size), dtype=int)

    for _ in range(num_trees):
        # Randomly choose a starting point
        start_x = np.random.randint(world_size)
        start_y = np.random.randint(world_size)

        # Simulate tree growth
        for age in range(max_age):
            # Fill in the tile with trees (green value)
            world[start_y, start_x] = 1.0  # Set the value to represent a tree

            # Randomly spread to neighboring tiles
            if np.random.rand() < spread_probability:
                neighbors = [
                    (start_x - 1, start_y),
                    (start_x + 1, start_y),
                    (start_x, start_y - 1),
                    (start_x, start_y + 1)
                ]

                # Choose a random neighbor
                neighbor_x, neighbor_y = neighbors[np.random.randint(len(neighbors))]

                # Check boundaries to avoid going out of bounds
                if 0 <= neighbor_x < world_size and 0 <= neighbor_y < world_size:
                    start_x, start_y = neighbor_x, neighbor_y
            else:
                break  # Stop growing with a certain probability


def simulate_population_growth(world, towns_info, num_years=10):
    for year in range(num_years):
        # Calculate distances between towns
        town_positions = np.array([town_info['position'] for town_info in towns_info])
        distances = distance.cdist(town_positions, town_positions, 'euclidean')

        # Create a minimum spanning tree
        tree = minimum_spanning_tree(distances)

        # Update populations based on distance and connections
        for i, town_info in enumerate(towns_info):
            connected_towns = [j for j in range(len(towns_info)) if tree[i, j] != 0]
            total_population = sum(towns_info[j]['population'] for j in connected_towns) + town_info['population']
            new_population = int(total_population / (len(connected_towns) + 1))  # Distribute equally among connected towns
            town_info['population'] = new_population


def generate_rivers(world, num_rivers=3, max_length=50, flow_deviation=0.2, cluster_radius=10,world_size=50):
    # Choose a central point for the river clusters
    cluster_center_x = world_size // 2
    cluster_center_y = world_size // 2

    for _ in range(num_rivers):
        # Randomly choose a starting point within the cluster radius
        start_x = int(np.clip(np.random.normal(cluster_center_x, cluster_radius), 0, world_size - 1))
        start_y = int(np.clip(np.random.normal(cluster_center_y, cluster_radius), 0, world_size - 1))

        # Randomly choose a flow direction
        flow_direction = np.random.uniform(0, 2 * np.pi)

        # Simulate river flow
        for step in range(max_length):
            # Fill in the tile with water (blue value)
            world[start_y, start_x] = -1.0  # Set the value to represent water

            # Move in the preferred flow direction with some deviation
            direction_x = np.cos(flow_direction) + np.random.uniform(-flow_deviation, flow_deviation)
            direction_y = np.sin(flow_direction) + np.random.uniform(-flow_deviation, flow_deviation)

            # Update the current position
            start_x = int(np.clip(start_x + direction_x, 0, world_size - 1))
            start_y = int(np.clip(start_y + direction_y, 0, world_size - 1))

def generate_random_town_name(used_names):
    available_names = list(set(name_array) - set(used_names))
    if available_names:
        return np.random.choice(available_names)
    else:
        return None

def generate_random_population():
    # Generate a random population based on a normal distribution
    mean_population = 500
    std_dev_population = 150
    return int(np.random.normal(mean_population, std_dev_population))


def generate_towns(world, num_towns=5, min_distance=10, marker='s', color='red', world_size=50):
    towns = []  # Keep track of town locations

    for _ in range(num_towns):
        # Randomly choose a starting point
        town_x = np.random.randint(world_size)
        town_y = np.random.randint(world_size)

        # Check if the location is suitable for a town (in a clearing and near water)
        if world[town_y, town_x] == 0.0:  # Check if the tile is empty (no forest or river)
            # Check if the location is near water (within a certain distance)
            water_nearby = np.any(world[
                max(0, town_y - min_distance): min(world_size, town_y + min_distance + 1),
                max(0, town_x - min_distance): min(world_size, town_x + min_distance + 1)
            ] == -1.0)

            if water_nearby:
                # Plot a marker for the town
                plt.scatter(town_x + 0.5, town_y + 0.5, marker=marker, color=color)
                towns.append([town_x + 0.5, town_y + 0.5])

    return np.array(towns)

def generate_town_info(world, town_locations):
    towns_info = []

    used_names = []

    for town_loc in town_locations:
        town_x, town_y = int(town_loc[0]), int(town_loc[1])

        # Generate town name
        town_name = generate_random_town_name(used_names)
        if town_name:
            used_names.append(town_name)
        else:
            break  # No more available names

        # Generate town population
        town_population = generate_random_population()

        towns_info.append({
            'position': (town_x + 0.5, town_y + 0.5),
            'name': town_name,
            'population': town_population
        })

    return towns_info



def generate_dungeon(world, towns, max_attempts=1000, min_distance=5, marker='X', color='purple', world_size=50):
    dungeon_location = None
    attempts = 0

    while dungeon_location is None and attempts < max_attempts:
        dungeon_x = np.random.randint(world_size)
        dungeon_y = np.random.randint(world_size)

        # Ensure dungeon is far enough from other towns
        if not any(np.linalg.norm(np.array([dungeon_x, dungeon_y]) - np.array(town)) < min_distance for town in towns):
            dungeon_location = [dungeon_x + 0.5, dungeon_y + 0.5]
            plt.scatter(dungeon_location[0], dungeon_location[1], marker=marker, color=color)

        attempts += 1

    return np.array(dungeon_location)


def generate_bandit_camps(world, num_bandit_camps=5, min_distance=5, marker='^', color='orange',world_size=50):
    for _ in range(num_bandit_camps):
        # Randomly choose a starting point
        camp_x = np.random.randint(world_size)
        camp_y = np.random.randint(world_size)

        # Check if the location is suitable for a bandit camp (away from towns and near roads)
        if world[camp_y, camp_x] == 0.0:  # Check if the tile is empty (no forest or river)
            # Check if the location is away from towns and near roads
            if np.all(world[
                max(0, camp_y - min_distance): min(world_size, camp_y + min_distance + 1),
                max(0, camp_x - min_distance): min(world_size, camp_x + min_distance + 1)
            ] == 0.0):  # Check if there are no towns nearby
                # Plot a marker for the bandit camp
                plt.scatter(camp_x + 0.5, camp_y + 0.5, marker=marker, color=color)

def generate_goblin_camps(world, num_goblin_camps=5, min_distance=5, marker='v', color='green',world_size=50):
    for _ in range(num_goblin_camps):
        # Randomly choose a starting point
        camp_x = np.random.randint(world_size)
        camp_y = np.random.randint(world_size)

        # Check if the location is suitable for a goblin camp (deep in the woods)
        if world[camp_y, camp_x] == 1.0:  # Check if the tile has forest
            # Check if the location is deep in the woods
            if np.all(world[
                max(0, camp_y - min_distance): min(world_size, camp_y + min_distance + 1),
                max(0, camp_x - min_distance): min(world_size, camp_x + min_distance + 1)
            ] == 1.0):  # Check if the tile is surrounded by forest
                # Plot a marker for the goblin camp
                plt.scatter(camp_x + 0.5, camp_y + 0.5, marker=marker, color=color)

def generate_roads(world, towns, road_value=0.5):
    num_towns = len(towns)

    # Calculate distances between towns
    distances = distance.cdist(towns, towns, 'euclidean')

    # Create a minimum spanning tree
    tree = minimum_spanning_tree(distances)

    # Add roads to the world
    for i in range(num_towns):
        for j in range(i + 1, num_towns):
            if tree[i, j] != 0:
                # Generate a road between towns
                road = np.linspace(towns[i], towns[j], int(tree[i, j]), endpoint=False)[1:]
                for point in road:
                    x, y = point.astype(int)
                    world[y, x] = road_value

    # Draw roads as black lines
    for i in range(num_towns):
        for j in range(i + 1, num_towns):
            if tree[i, j] != 0:
                road = np.linspace(towns[i], towns[j], int(tree[i, j]), endpoint=False)[1:]
                road_x, road_y = road.T.astype(int)
                plt.plot(road_x, road_y, color='black')
