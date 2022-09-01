# A simulation by Lucca Limongi

import random as rd
import time
import pygame as pg
import math
from core import *

def print_text(text, coords):
    text_print = font.render(text, False, (0, 0, 0))
    screen.blit(text_print, coords)


# Initialize pygame
pg.init()

# Clock set-up
CLOCK = pg.time.Clock()

# Display
pg.display.init()

# Game loop
running = True

# Screen setting
pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 0)
screen = pg.display.set_mode((1200, 600))

# Title and Icon
pg.display.set_caption("gfx/Race Works")
icon = pg.image.load("gfx/RaceWorksIcon.png")
pg.display.set_icon(icon)

# Font
font = pg.font.SysFont('century', 18)

render_all = True
track_name = "FlashPoint Raceway Short L"
gen_counter = 0
cp_list = [(-585, 480), (-450, 480), (-230, 480), (150, -465), (175, -455), (270, -415), (410, -370), (1200, -600)]

n_cars = 250 #int(input(""))

Network.set_individual_mutation_chance(1)
Network.set_crossover_chance(1)
Network.set_crossover_bias(0.5)
Network.set_gene_mutation_chance(0.15)
Network.set_mutation_strength_factor(0.05)
Network.set_mutation_noise_factor(0.05)

grid = []
for x in range(n_cars):
    grid.append(Car())
    
best_car = grid[0]
REPRODUCTION_METHOD = BestReproduce(Network.reproduce, Car, Network)

screen.fill((96, 96, 96))
track = pg.image.load(f"gfx/{track_name} Mask.png")
track_mask = pg.mask.from_surface(track)
Car.set_track_mask(track_mask)
screen.blit(track, (0, 0))
pg.display.update()


running = True
while running:
    start_3 = time.time()

    running_cars = n_cars
    game_tick = 0

    while running_cars > 0 and game_tick < 1000 and running:
        #CLOCK.tick(60)
        game_tick += 1

        for event in pg.event.get():
            if event.type == pg.quit:
                running = False


        screen.fill((96, 96, 96))
        track = pg.image.load(f"gfx/{track_name} Mask.png")
        track_mask = pg.mask.from_surface(track)
        screen.blit(track, (0, 0))
        print_text(f"{game_tick} / {gen_counter}", (550, 410))
        
        for car in grid:
            if not car.crash:
                car.update_car()
                if car.crash:
                    running_cars -= 1
                if render_all:
                    screen.blit(car.image, (int(car.pos_x), int(car.pos_y)))

        if not render_all:
            screen.blit(best_car.image, (int(best_car.pos_x), int(best_car.pos_y)))

        pg.display.update()

    
        # Check to close app
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            running = False

    total_distance = 0
    for car in grid:
        car.gap_to_cp = distance_two_points(cp_list[car.points], (car.x, car.y))

    grid.sort(key=lambda car: (car.distance), reverse=True)
    Car.set_max_distance(grid[0].distance)
    print(f"Gen {gen_counter}: Best car ran {grid[0].distance} metres")

    grid.sort(key=lambda car: (car.fitness()), reverse=True)

    for car in grid:
        total_distance += car.distance

    # Reprodution and mutation
    
    grid = REPRODUCTION_METHOD.generate(population=grid[:100], top_immunity_count=20, reproduction_count=100, couples_count=100, pressure_count=n_cars, top_mutation_factor=1)
    end_3 = time.time()
    print(f"Gen {gen_counter}: Average of {total_distance/ n_cars} metres")# in {end_3 - start_3} seconds for {n_cars} cars")
    gen_counter += 1
    best_car = grid[0]
    print("")