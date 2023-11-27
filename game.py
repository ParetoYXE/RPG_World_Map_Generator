import pygame
import random
import math
from map_gen import display_world_with_info



def main(world, towns_info):
    pygame.init()

    world_size = len(world)
    tiles_around_player = 10  # Adjust as needed
    tile_size = 800 // tiles_around_player  # Adjust screen size as needed
    player_location = random.randint(0, world_size ** 2)
    player_x = player_location % world_size
    player_y = math.floor(player_location / world_size)


    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    print("Welcome to the Adventure Game!")
    print("Explore the world and interact with towns.")

    world_map_key = {
        '1.0': pygame.transform.scale(pygame.image.load('tree.png'), (tile_size, tile_size)),  # Use the image for forests
        '-1.0': (0, 0, 255),
        '0.5': (128, 128, 128),
        '0.0': (0, 128, 0),
        'Town':pygame.transform.scale(pygame.image.load('house.png'), (tile_size, tile_size))
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_location += world_size
                elif event.key == pygame.K_s:
                    player_location -= world_size
                elif event.key == pygame.K_d:
                    player_location += 1
                elif event.key == pygame.K_a:
                    player_location -= 1
                elif event.key == pygame.K_e:
                    run = False

        # Update player location on overworld
        player_x = player_location % world_size
        player_y = math.floor(player_location / world_size)



        # Render a simple representation using Pygame
        screen.fill((0, 128, 0))  # Clear the screen

        # Draw tiles around the player
        for y in range(player_y - tiles_around_player // 2, player_y + tiles_around_player // 2):
            for x in range(player_x - tiles_around_player // 2, player_x + tiles_around_player // 2):
                if 0 <= x < world_size and 0 <= y < world_size:
                    color_or_image = world_map_key[str(world[y][x])]

                    if isinstance(color_or_image, tuple):  # If it's a color
                        pygame.draw.rect(screen, color_or_image, ((x - player_x + tiles_around_player // 2) * tile_size, (y - player_y + tiles_around_player // 2) * tile_size, tile_size, tile_size))
                    else:  # If it's an image
                        screen.blit(color_or_image, ((x - player_x + tiles_around_player // 2) * tile_size, (y - player_y + tiles_around_player // 2) * tile_size))

        # Draw towns within the visible area
        for town_info in towns_info:
            town_x, town_y = town_info['position']
            if (player_x - tiles_around_player // 2) <= town_x <= (player_x + tiles_around_player // 2) and \
               (player_y - tiles_around_player // 2) <= town_y <= (player_y + tiles_around_player // 2):
                screen.blit(world_map_key['Town'], ((int(town_x) - player_x + tiles_around_player // 2) * tile_size, (int(town_y) - player_y + tiles_around_player // 2) * tile_size))

        # Draw player as a red dot
        pygame.draw.circle(screen, (255, 0, 0), (tiles_around_player * tile_size // 2, tiles_around_player * tile_size // 2), 2)

        pygame.display.flip()
        clock.tick(30)  # Adjust the frame rate as needed

    pygame.quit()


if __name__ == "__main__":
    # Your map generation code here

    display_world_with_info(world, town_locations)

    main(world, town_locations)
