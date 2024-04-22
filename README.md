# RPG_World_Map_Generator

The World Generation Tool is a Python-based utility designed to create dynamic and intricate game worlds for 2D role-playing games. Its primary features include the random generation of expansive terrains, featuring forests, rivers, towns, and roads, reminiscent of classic open-world RPGs. The tool utilizes a combination of procedural algorithms to produce diverse landscapes, ensuring each playthrough offers a unique and immersive gaming experience.

# Key Features

Terrain Generation:

* Create vast and varied landscapes with forests, clearings, and hills.
Dynamically generate rivers that wind through the terrain.

Town and Road Generation:

* Place towns in clearings near water sources.
Connect towns with a network of roads, forming a graph-like structure.

Dynamic Map Elements:

* Simulate forests with organic clusters of trees that grow and spread.
Generate rivers with random paths, contributing to the natural flow of the world.

Interactive Towns:

* Populate towns with distinct markers for easy identification.
Automatically generate roads connecting all towns, enhancing accessibility.

Customizable Parameters:

* Adjust various parameters, such as the number of towns, tree growth, river flow, etc.
Flexibility to tailor the generated world to fit specific game requirements.


# Example Use

Clone the repository and install dependencies.
Utilize the provided functions to generate and display diverse game worlds.

Usage Example:

```python
from map_gen import generate_blank_world, generate_forest, generate_rivers, generate_roads, display_world_with_info, generate_towns, generate_town_info

world_size = 50
world = generate_blank_world(world_size)

generate_forest(world, num_trees=200, max_age=10, spread_probability=1)
generate_rivers(world, num_rivers=10, max_length=500, flow_deviation=0.8, cluster_radius=1)

town_locations = generate_towns(world, num_towns=50, min_distance=10, marker='s', color='red')
generate_roads(world, town_locations)

town_info = generate_town_info(world, town_locations)

display_world_with_info(world, town_info, title="World with Towns and Roads")
```
