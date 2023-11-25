import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from scipy.sparse.csgraph import minimum_spanning_tree


def generate_blank_world(size):
    return np.zeros((size, size))

def display_world(world, title="World"):
    plt.imshow(world, cmap='terrain', interpolation='bilinear', vmax=1.0, vmin=-1.0)
    plt.colorbar()
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
