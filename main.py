# A simulation by Lucca Limongi

import random as rd
import time
import pygame as pg
import math
from core import *


def distance_two_points(pointA, pointB):
    a_x, a_y = pointA
    b_x, b_y = pointB
    return (((a_x - b_x) ** 2) + ((a_y - b_y) ** 2)) ** 0.5


def line_tracer_2(angle, start_x, start_y, mask):
    x = int(start_x)
    y = int(start_y)

    if angle >= 360:
        angle -= 360

    angle = math.radians(angle)
    angle = round(angle, 1)

    if (45 > angle > 0 or 225 > angle > 135 or 360 > angle > 315) and angle != 180:
        if angle > 270 or angle < 90:
            n = 1
        else:
            n = -1
        dx = math.tan(angle)
        while True:
            if mask.get_at((int(x), int(y))) == 1:
                break
            y -= n
            x += dx * n

    elif (135 > angle > 45 or 315 > angle > 225) and angle != 90 and angle != 270:
        if angle < 180:
            n = 1
        else:
            n = -1
        dy = math.tan(angle) ** -1
        while True:
            if mask.get_at((int(x), int(y))) == 1:
                break
            x += n
            y -= dy * n
            # pg.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 1, 1)

    elif angle == 0 or angle == 180:
        if angle == 0:
            n = 1
        else:
            n = -1
        while True:
            if mask.get_at((int(x), int(y))) == 1:
                break
            y -= n
            # pg.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 1, 1)

    elif angle == 90 or angle == 270:
        if angle == 90:
            n = 1
        else:
            n = -1
        while True:
            if mask.get_at((int(x), int(y))) == 1:
                break
            x += n
            # pg.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 1, 1)
    return distance_two_points((int(x), int(y)), (int(start_x), int(start_y)))

def print_text(text, coords):
    text_print = font.render(text, False, (0, 0, 0))
    screen.blit(text_print, coords)


class Car(pg.sprite.Sprite):
    def __init__(self, image, x_coord, y_coord, angle, top_speed, acceleration, brake, turning_angle, network):
        global gen_counter

        self.network = network
        self.id = self.network.get_data()[2]
        self.throttle = 0
        self.turning = 0

        self.top_speed = top_speed
        self.acceleration = acceleration
        self.brake = brake
        self.turning_angle = turning_angle

        self.crash = False
        self.angle = self.original_angle = angle
        self.rad_angle = math.radians(self.angle)
        self.x = self.x_coord = x_coord
        self.y = self.y_coord = y_coord
        self.speed = 0
        self.age = 0

        self.original_image = pg.image.load(f"{image}")
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.center

        self.distance = 0
        self.gap_to_cp = 0
        self.points = 0

    def get_data(self):
        return self.network.get_data()

    def update_car(self):
        global track_mask
        

        if self.crash:
            return
        
        else:
            self.age += 1
            if self.age > 10 and self.speed == 0:
                self.crash = True
                return


            self.image = pg.transform.rotate(self.original_image, -self.angle)

            self.mask = pg.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            dump, dump, self.width, self.height = self.rect
            "%.3f" % self.angle

            
            input_data = [
            self.speed,
            math.log2(line_tracer_2(self.angle, self.x, self.y, track_mask)),
            math.log2(line_tracer_2(self.angle + 15, self.x, self.y, track_mask)),
            math.log2(line_tracer_2(self.angle + 45, self.x, self.y, track_mask)),
            math.log2(line_tracer_2(self.angle + 90, self.x, self.y, track_mask)),
            math.log2(line_tracer_2(self.angle + 270, self.x, self.y, track_mask)),
            math.log2(line_tracer_2(self.angle + 315, self.x, self.y, track_mask)),
            math.log2(line_tracer_2(self.angle + 345, self.x, self.y, track_mask))
            ]

            self.throttle, self.turning = self.network.feedforward(input_data)


            self.angle = self.angle % 360

            if self.throttle > 1:
                self.throttle = 1
            elif self.throttle < -1:
                self.throttle = -1

            if self.throttle > 0:
                self.speed += self.acceleration * self.throttle
            else:
                self.speed += self.brake * self.throttle

            if self.turning > 1:
                self.turning = 1
            elif self.turning < -1:
                self.turning = -1

            if self.speed > self.top_speed:
                self.speed = self.top_speed
            elif self.speed < 0:
                self.speed = 0

            if self.speed > 1:
                self.angle += (self.turning_angle / self.speed) * self.turning
            elif self.speed > 0.5:
                self.angle += self.turning_angle * self.turning
            else:
                pass

            if self.angle >= 360:
                self.angle -= 360
            elif self.angle < 0:
                self.angle += 360
            else:
                pass

            self.distance += self.speed

            self.rad_angle = math.radians(self.angle)
            self.x += math.sin(self.rad_angle) * self.speed
            self.y -= math.cos(self.rad_angle) * self.speed

            self.pos_x = self.x - self.width / 2
            self.pos_y = self.y - self.height / 2
            #screen.blit(self.image, (int(self.pos_x), int(self.pos_y)))


            if track_mask.overlap(self.mask, ((int(self.pos_x), int(self.pos_y)))):
                self.crash = True

            for cp in cp_list:
                cp_x, cp_y = cp
                if self.points % len(cp_list) == cp_list.index(cp):
                    if cp_x > 0 and cp_y > 0:
                        if self.x > cp_x and self.y > cp_y:
                            self.points += 1
                    elif cp_x < 0 and cp_y > 0:
                        if self.x < -cp_x and self.y > cp_y:
                            self.points += 1
                    elif cp_x > 0 and cp_y < 0:
                        if self.x > cp_x and self.y < -cp_y:
                            self.points += 1
                    elif cp_x < 0 and cp_y < 0:
                        if self.x < cp_x and self.y < cp_y:
                            self.points += 1


    def fitness(self):
        return (math.pow(self.distance, 3) / self.age) * (1 - (self.speed / self.top_speed))

                            
    def reset_car(self): # Deprecated
        self.x = self.x_coord
        self.y = self.y_coord
        self.speed = 0
        self.crash = False
        self.angle = self.original_angle
        self.points = 0
        self.distance = 0



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
Network.set_gene_mutation_chance(0.05)
Network.set_mutation_strength_factor(0.25)
Network.set_mutation_noise_factor(0.15)

def new_car(data=[], mutate=False):
    return Car("gfx/Formula Rossa Car.png", 604, 486, 270, 8, 0.7, 2, 10, Network(data, mutate))

grid = []
for x in range(n_cars):
    grid.append(new_car())
    
best_car = grid[0]
REPRODUCTION_METHOD = BestReproduce(Network.reproduce, new_car)

screen.fill((96, 96, 96))
track = pg.image.load(f"gfx/{track_name} Mask.png")
track_mask = pg.mask.from_surface(track)
screen.blit(track, (0, 0))
pg.display.update()


running = True
while running:
    start_3 = time.time()

    running_cars = n_cars
    game_tick = 0

    while running_cars > 0 and game_tick < 200 and running:
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

    grid.sort(key=lambda car: (car.fitness()), reverse=True)
    print(f"Gen {gen_counter}: Best car ran {grid[0].distance} metres")
    print("Stuff:")
    for car in grid:
        total_distance += car.distance

    # Reprodution and mutation
    
    
    grid = REPRODUCTION_METHOD.generate(population=grid, top_immunity_count=25, couples_count=0, top_mutation_factor=1)

    end_3 = time.time()
    #print(f"Gen {gen_counter}: Average of {total_distance/ n_cars} metres")# in {end_3 - start_3} seconds for {n_cars} cars")
    gen_counter += 1
    best_car = grid[0]
    print("##############################")