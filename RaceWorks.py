# A simulation by Lucca Limongi

import random as rd
import time
import pygame as pg
import math
from core import *

n_cars = 250 #int(input(""))

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
        self.throttle = 0
        self.turning = 0

        self.distance = 0
        self.gap_to_cp = 0
        self.age = 0
        self.points = 0
        self.crash = False
        self.angle = self.original_angle = angle
        self.rad_angle = math.radians(self.angle)
        self.original_image = pg.image.load(f"{image}")
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.x = self.x_coord = x_coord
        self.y = self.y_coord = y_coord
        self.rect.center = (self.x, self.y)
        self.top_speed = top_speed
        self.acceleration = acceleration
        self.brake = brake
        self.speed = 0
        self.turning_angle = turning_angle
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.center

    def update_car(self):
        global track_mask
        global running_cars

        #total_time = time.time()
        self.image = pg.transform.rotate(self.original_image, -self.angle)

        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        dump, dump, self.width, self.height = self.rect
        "%.3f" % self.angle

        #trace_time = time.time()
        #time.sleep(0.001)
        input_data = [
        self.speed,
        self.angle,
        line_tracer_2(self.angle, self.x, self.y, track_mask),
        line_tracer_2(self.angle + 15, self.x, self.y, track_mask),
        line_tracer_2(self.angle + 45, self.x, self.y, track_mask),
        line_tracer_2(self.angle + 90, self.x, self.y, track_mask),
        line_tracer_2(self.angle + 270, self.x, self.y, track_mask),
        line_tracer_2(self.angle + 315, self.x, self.y, track_mask),
        line_tracer_2(self.angle + 345, self.x, self.y, track_mask)
        ]

        if not self.crash:
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
            running_cars -= 1

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

        #total_time = time.time() - total_time

        #print(total_time, trace_time)
        #print(f"Time percent spent on line tracing: {100 * total_time / trace_time}%")
    def reset_car(self):
        self.x = self.x_coord
        self.y = self.y_coord
        self.speed = 0
        self.crash = False
        self.angle = self.original_angle
        self.points = 0
        self.distance = 0
        self.age -= 1

    def eliminate_car(self):
        global new_grid

        if self.points == 0:
            pass

        else:
            new_grid.append(self)















gen_counter = 0
cp_list = [(-585, 480), (-450, 480), (-230, 480), (150, -465), (175, -455), (270, -415), (410, -370), (1200, -600)]
grid = []
for x in range(n_cars):
    grid.append(Car("gfx/Formula Rossa Car.png", 604, 486, 270, 8, 0.7, 2, 10, Network()))

screen.fill((96, 96, 96))
track = pg.image.load("gfx/FlashPoint Raceway Short LC Mask.png")
track_mask = pg.mask.from_surface(track)
screen.blit(track, (0, 0))
pg.display.update()


running = True
while running:
    running_cars = n_cars
    start_3 = time.time()
    game_tick = 0
    while running_cars > 0 and game_tick < 500 and running:
        CLOCK.tick(60)
        game_tick += 1
        start_4 = time.time()
        for event in pg.event.get():
            if event.type == pg.quit:
                running = False

        #print(f"----------------Tick {game_tick}----------------")
        #tick_time = time.time()
        screen.fill((96, 96, 96))
        track = pg.image.load("gfx/FlashPoint Raceway Short LC Mask.png")
        track_mask = pg.mask.from_surface(track)
        screen.blit(track, (0, 0))
        print_text(f"{game_tick} / {gen_counter}", (550, 410))
        #print(f"P0 {time.time() - tick_time}")
        for car in grid:
            if not car.crash:
                car.update_car()
        #print(f"P1 {time.time() - tick_time}")
            

        screen.blit(grid[0].image, (int(grid[0].pos_x), int(grid[0].pos_y)))
        #print(f"P2 {time.time() - tick_time}")

        pg.display.update()
        #print(f"P3 {time.time() - tick_time}")
        
        still_counter = 0
        if game_tick > 20:
            for car in grid:
                if car.speed <= 0.25 and not car.crash:
                    still_counter += 1
        if running_cars == still_counter:
            break
        end_4 = time.time()
        # print(f"{end_4 - start_4} seconds tick")
    
        #Check to close app
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            running = False

    new_grid = []
    total_distance = 0
    
    for car in grid:
        car.gap_to_cp = distance_two_points(cp_list[car.points], (car.x, car.y))

    grid.sort(key=lambda car: (car.distance), reverse=True)
    #print(grid[0].network.network_weights, grid[0].gap_to_cp - (grid[0].points * 500))
    for car in grid:
        total_distance += car.distance

    for x in range(10):
        grid.pop()
    for x in range(10):
        grid[x].reset_car()
        new_grid.append(grid[x])
        new_grid.append(Car("gfx/Formula Rossa Car.png", 604, 486, 270, 8, 0.7, 2, 10, Network(grid[x].network.network_weights, True)))

    for x in range(10, n_cars - 10):
        grid[x].reset_car()
        grid[x].network.mutate()
        new_grid.append(grid[x])
        

    end_3 = time.time()
    print(f"Gen {gen_counter}: Average of {total_distance/ n_cars} metres in {end_3 - start_3} seconds for {n_cars} cars")
    gen_counter += 1
    grid = new_grid

