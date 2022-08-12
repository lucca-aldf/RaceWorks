# A simulation by Lucca Limongi

import random
import time
import pygame as pg
import math
import copy

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

class Network:
    def __init__(self, variables=2, data=[]):
        if not data:

            self.weight_throttle = round(random.uniform(-1, 1), 3)
            self.bias_throttle = round(random.uniform(-500, 500), 3)
            self.weight_turning = round(random.uniform(-1, 1), 3)

            self.weight_0_throttle = round(random.uniform(-1, 1), 3)
            self.weight_1_throttle = round(random.uniform(-1, 1), 3)
            self.weight_2_throttle = round(random.uniform(-1, 1), 3)
            self.weight_3_throttle = round(random.uniform(-1, 1), 3)
            self.weight_4_throttle = round(random.uniform(-1, 1), 3)
            self.weight_5_throttle = round(random.uniform(-1, 1), 3)
            self.weight_6_throttle = round(random.uniform(-1, 1), 3)
            self.weight_7_throttle = round(random.uniform(-1, 1), 3)
            self.weight_8_throttle = round(random.uniform(-1, 1), 3)
            self.weight_speed_throttle = round(random.uniform(-1, 1), 3)

            self.weight_0_turning = round(random.uniform(-1, 1), 3)
            self.weight_1_turning = round(random.uniform(-1, 1), 3)
            self.weight_2_turning = round(random.uniform(-1, 1), 3)
            self.weight_3_turning = round(random.uniform(-1, 1), 3)
            self.weight_4_turning = round(random.uniform(-1, 1), 3)
            self.weight_5_turning = round(random.uniform(-1, 1), 3)
            self.weight_6_turning = round(random.uniform(-1, 1), 3)
            self.weight_7_turning = round(random.uniform(-1, 1), 3)
            self.weight_8_turning = round(random.uniform(-1, 1), 3)
            self.weight_speed_turning = round(random.uniform(-1, 1), 3)

        else:

            self.weight_throttle = data[0]
            self.bias_throttle = data[1]
            self.weight_turning = data[2]

            self.weight_0_throttle = data[3]
            self.weight_1_throttle = data[4]
            self.weight_2_throttle = data[5]
            self.weight_3_throttle = data[6]
            self.weight_4_throttle = data[7]
            self.weight_5_throttle = data[8]
            self.weight_6_throttle = data[9]
            self.weight_7_throttle = data[10]
            self.weight_8_throttle = data[11]
            self.weight_speed_throttle = data[12]

            self.weight_0_turning = data[13]
            self.weight_1_turning = data[14]
            self.weight_2_turning = data[15]
            self.weight_3_turning = data[16]
            self.weight_4_turning = data[17]
            self.weight_5_turning = data[18]
            self.weight_6_turning = data[19]
            self.weight_7_turning = data[20]
            self.weight_8_turning = data[21]
            self.weight_speed_turning = data[22]

        self.change_list = []
        self.data_set = [self.weight_throttle, self.bias_throttle, self.weight_turning, self.weight_0_throttle,
                         self.weight_1_throttle, self.weight_2_throttle, self.weight_3_throttle, self.weight_4_throttle,
                         self.weight_5_throttle, self.weight_6_throttle, self.weight_7_throttle, self.weight_8_throttle,
                         self.weight_speed_throttle, self.weight_0_turning, self.weight_1_turning, self.weight_2_turning,
                         self.weight_3_turning, self.weight_4_turning, self.weight_5_turning, self.weight_6_turning,
                         self.weight_7_turning, self.weight_8_turning, self.weight_speed_turning]

        if variables != 0:
            for ele in range(variables):
                n = random.randint(0, len(self.data_set) - 1)
                while n in self.change_list:
                    n = random.randint(0, len(self.data_set) - 1)
                self.change_list.append(n)

            for n in self.change_list:
                if abs(self.data_set[n]) >= 0.005:
                    self.data_set[n] = round(self.data_set[n] * random.uniform(0.98, 1.02) * ((-1) ** random.randint(1, 2)), 3)

        self.throttle_weights = [self.weight_0_throttle, self.weight_1_throttle, self.weight_2_throttle,
                            self.weight_3_throttle, self.weight_4_throttle, self.weight_5_throttle,
                            self.weight_6_throttle, self.weight_7_throttle, self.weight_8_throttle,
                            self.weight_speed_throttle]

        self.turning_weights = [self.weight_0_turning, self.weight_1_turning, self.weight_2_turning,
                            self.weight_3_turning, self.weight_4_turning, self.weight_5_turning,
                            self.weight_6_turning, self.weight_7_turning, self.weight_8_turning,
                            self.weight_speed_turning]

    def neuron(self, weights, inputs):
        output = 0
        for inp in inputs:
            output += weights[inputs.index(inp)] * inp
        return output

    def throttle_output(self, input_data):
        return self.neuron(self.throttle_weights, input_data) * self.weight_throttle + self.bias_throttle

    def turning_output(self, input_data):
        return self.neuron(self.turning_weights, input_data) * self.weight_turning



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
        self.line_0 = line_tracer_2(self.angle, self.x, self.y, track_mask)
        self.line_1 = line_tracer_2(self.angle + 15, self.x, self.y, track_mask)
        self.line_2 = line_tracer_2(self.angle + 45, self.x, self.y, track_mask)
        self.line_3 = line_tracer_2(self.angle + 75, self.x, self.y, track_mask)
        self.line_4 = line_tracer_2(self.angle + 90, self.x, self.y, track_mask)
        self.line_5 = line_tracer_2(self.angle + 270, self.x, self.y, track_mask)
        self.line_6 = line_tracer_2(self.angle + 285, self.x, self.y, track_mask)
        self.line_7 = line_tracer_2(self.angle + 315, self.x, self.y, track_mask)
        self.line_8 = line_tracer_2(self.angle + 345, self.x, self.y, track_mask)

        #trace_time = time.time() - trace_time
        input_data = (self.speed, self.line_0, self.line_1, self.line_2, self.line_3, self.line_4, self.line_5, self.line_6, self.line_7, self.line_8)

        if not self.crash:
            self.throttle = self.network.throttle_output(input_data)
            self.turning = self.network.turning_output(input_data)
            if self.angle >= 360:
                self.angle -= 360
            elif self.angle < 0:
                self.angle += 360
            else:
                pass

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
track = pg.image.load("gfx/FlashPoint Raceway Short L Mask.png")
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
        track = pg.image.load("gfx/FlashPoint Raceway Short L Mask.png")
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
        if running_cars - still_counter == 0:
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
    grid.sort(key=lambda car: (car.gap_to_cp - (car.points * 500)), reverse=False)
    print(grid[0].network.data_set, grid[0].gap_to_cp - (grid[0].points * 500))
    for car in grid:
        total_distance += car.distance

    for x in range(int(n_cars * 0.8)):
        grid.pop()
    for car in grid:
        car.reset_car()
        new_grid.append(car)
        new_grid.append(Car("gfx/Formula Rossa Car.png", 604, 486, 270, 8, 0.7, 2, 10, Network(random.randint(1, 10), car.network.data_set)))
        new_grid.append(Car("gfx/Formula Rossa Car.png", 604, 486, 270, 8, 0.7, 2, 10, Network(random.randint(1, 10), car.network.data_set)))
        new_grid.append(Car("gfx/Formula Rossa Car.png", 604, 486, 270, 8, 0.7, 2, 10, Network(random.randint(1, 10), car.network.data_set)))
        new_grid.append(Car("gfx/Formula Rossa Car.png", 604, 486, 270, 8, 0.7, 2, 10, Network(random.randint(1, 10), car.network.data_set)))
        

    end_3 = time.time()
    print(f"Gen {gen_counter}: Average of {total_distance/ n_cars} metres in {end_3 - start_3} seconds for {n_cars} cars")
    gen_counter += 1
    grid = new_grid

