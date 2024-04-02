import pygame
import random
from math import sin
from math import cos
from math import sqrt
pygame.init()
screen_width, screen_height = 800, 520
gameDisplay, clock=pygame.display.set_mode((screen_width, screen_height)), pygame.time.Clock()
pygame.display.set_caption("Minecraft in python")
pi = 3.141592653589793
world_width = 100
world_height = 50
world_length = 100
def rotate_point(x, y, xc, yc, rot):
    x, y = x-xc, y-yc
    rx = x*cos(rot)-y*sin(rot)
    rx = y*cos(rot)+x*sin(rot)
    x, y = rx+xc, ry+yc
    return x, y
def rotate_3D(x, y, z, xc, yc, zc, hor_rot, ver_rot):
    x, z = rotate_point(x, z, xc, zc, hor_rot)
    z, y = rotate_point(z, y, zc, yc, ver_rot)
    return x, y, z
def conv_3D_to_2D(x, y, z):
    f = screen_width/2/z
    ox = x*f+screen_width/2
    oy = y*f+screen_width/2
    return int(ox), int(oy)
def get_d_order(xl, yl, zl, x, y, z): #d = distanz
    order_list = []
    for i in range(len(xl)):
        hd = sqrt((xl[i]-x)**2+(zl[i]-z)**2)
        d = sqrt((hd)**2+(yl[i]-y)**2)
        order_list.append(int(d)+0.00001*i)
    order_list.sort()
    for i in range(len(order_list)):
        order_list[i] = round((order_list[i]%1)*100000)
    return order_list.copy()
block_colors = [(15, 150, 15), (115, 115, 115), (35, 35, 35), (225, 225, 45), (205, 205, 240)]
world_blocks = []
#höhlen generation
x_cave, y_cave, z_cave = [], [], []
for i in range(5):
    x, y, z = random.randrange(0, world_width), random.randrange(0, world_height), random.randrange(0, world_length)
    for e in range(9):
        x, y, z = x+random.randrange(-2, 3), y+random.randrange(-2, 3), z+random.randrange(-2, 3)
        x_cave.append(x)
        y_cave.append(y)
        z_cave.append(z)
#welt generation
for i in range(world_width):
    for e in range(world_height):
        for o in range(world_length):
            cave_air = False
            for c in range(len(x_cave)):
                hd = sqrt((x_cave[c]-i)**2+(z_cave[c]-o)**2)
                d = sqrt((hd)**2+(y_cave[c]-e)**2)
                if d<1.5:
                    cave_air = True
                block = 0
                if e > 0 and not cave_air:
                    block=1
                if e > 3 and not cave_air:
                    block=2
                if e > world_height-10 and random.randrange(1, 51) == 1 and not cave_air:
                    block=4
                if e > world_height-8 and random.randrange(1, 151) == 1 and not cave_air:
                    block=5
                if e+1 == world_height or e > world_height-5 and random.randrange(1, 3) == 1:
                    block=3
                world_blocks.append(block)
block_size = 50
x_side , y_side , z_side , side_dir , side_color = [], [], [], [], []
def side_add(x, y, z, d, c):
    x_side.append(x)
    y_side.append(y)
    z_side.append(z)
    side_dir.append(d)
    side_color.append(c)
for i in range(world_width):
    for e in range(world_height):
        for o in range(world_length):
            ind = i*world_height*world_length+e*world_length+o
            if world_blocks[ind] > 0 :
                color = block_colors[world_blocks[ind]-1]
                if i > 0 and world_blocks[ind-world_height*world_length] == 0:
                    side_add(i*block_size, e*block_size+block_size/2, o*block_size+block_size/2, 1, color)
                if i+1 < world_width and world_blocks[ind+world_height*world_length] == 0:
                    side_add((i+1)*block_size, e*block_size+block_size/2, o*block_size+block_size/2, 1, color)
                if e > 0 and world_blocks[ind-world_length] == 0:
                    side_add(i*block_size+block_size/2, e*block_size, o*block_size+block_size/2, 3, color)
                if e+1 < world_height and world_blocks[ind+world_length] == 0:
                    side_add(i*block_size+block_size/2, (e+1)*block_size, o*block_size+block_size/2, 4, color)
                if o > 0 and world_blocks[ind-1] == 0:
                    side_add(i*block_size+block_size/2, e*block_size, o*block_size+block_size, 5, color)
                if o+1 < world_length and world_blocks[ind-1] == 0:
                    side_add(i*block_size+block_size/2, e*block_size+block_size/2, (o+1)*block_size, 6, color)
def side_update(x, y, z, d): #update, wenn ein block zerstört wird
    i, e, o = x, y, z
    ind = i*world_height*world_length+e*world_length+o
    if world_blocks[ind] > 0:
        color = block_colors[world_blocks[ind]-1]
        if i > 0 and world_blocks[ind-world_height*world_length] == 0 and d == 1:
            side_add(i*block_size, e*block_size+block_size/2, o*block_size+block_size/2, 1, color)
        if i+1 < world_width and world_blocks[ind+world_height*world_length] == 0 and d == 2:
            side_add((i+1)*block_size, e*block_size+block_size/2, o*block_size+block_size/2, 1, color)
        if e > 0 and world_blocks[ind-world_length] == 0 and d == 3:
            side_add(i*block_size+block_size/2, e*block_size, o*block_size+block_size/2, 3, color)
        if e+1 < world_height and world_blocks[ind+world_length] == 0 and d == 4:
            side_add(i*block_size+block_size/2, (e+1)*block_size, o*block_size+block_size/2, 4, color)
        if o > 0 and world_blocks[ind-1] == 0 and d == 5:
            side_add(i*block_size+block_size/2, e*block_size, o*block_size+block_size, 5, color)
        if o+1 < world_length and world_blocks[ind-1] == 0 and d == 6:
            side_add(i*block_size+block_size/2, e*block_size+block_size/2, (o+1)*block_size, 6, color)
block_reach = 4*block_size # reichweite des spielers
cam_pos, cam_speed, cam_angle = [world_width*block_size/2, -block_size*1.5, world_length*block_size/2], [0, 0, 0], [0, 0] # kamera einstellungen
left, right, up, down, jump, shift, ctrl = False, False, False, False, False, False, False
mouse_pressed = [0, 0, 0]
pygame.mouse.set_visible(False) #Maus ist unsichtbar
pygame.event.set_grab(True) #Maus ist verankert
MSE = 0.003 # maus sensi
while True:
    x_rel, y_rel = 0, 0
    for event in pygame.event.get(): #behält events in sicht
        if event.type == 2 and event.key == 97:
            left = True
        if event.type == 3 and event.key == 97:
            left = False
        if event.type == 2 and event.key == 100:
            right = True
        if event.type == 3 and event.key == 100:
            right = False
        if event.type == 2 and event.key == 119:
            up = True
        if event.type == 3 and event.key == 119:
            up = False
        if event.type == 2 and event.key == 115:
            down = True
        if event.type == 3 and event.key == 115:
            down = False
        if event.type == 2 and event.key == 32:
            jump = True
        if event.type == 3 and event.key == 32:
            jump = False
        if event.type == 2 and event.key == 304:
            shift = True
        if event.type == 3 and event.key == 304:
            shift = False
        if event.type == 2 and event.key == 306:
            ctrl = True
        if event.type == 3 and event.key == 306:
            ctrl = False
        if event.type == pygame.MOUSEMOTION:
            x_rel, y_rel = event.rel
        if event.type == 2 and event.key == 27: # esc beendet das Spiel
            pygame.quit()
            quit()
    gameDisplay.fill((90, 90, 255)) #Hintergrundfarbe
    pmp, mouse_pressed = mouse_pressed, pygame.mouse.get_pressed() #neue Maus inputs
    cam_angle[0], cam_angle[1] = (cam_angle[0]+x_rel*MSE)%(2*pi), cam_angle[1]+(y_rel*MSE)%(2*pi) #kamera rotation
    if cam_angle[1] > pi*0.5 and cam_angle[1] <= pi:
        cam_angle[1] = 1.5
    if cam_angle[1] > pi and cam_angle[1] < pi*1.5:
        cam_angle[1] = 1.5
    cam_speed_add = 1.5
    if ctrl:#mit Strg/ctrl sprintet man
        cam_speed_add = 2.3
    if left:#mit WASD bewegt man sich
        xm, zm = rotate_point(0, cam_speed_add, 0, 0, (-cam_angle[0]+pi*0.5)%(2*pi))
        cam_speed[0], cam_speed[2] = cam_speed[0]+xm, cam_speed[2]+zm
    if right:
        xm, zm = rotate_point(0, cam_speed_add, 0, 0, (-cam_angle[0]-pi*0.5)%(2*pi))
        cam_speed[0], cam_speed[2] = cam_speed[0]+xm, cam_speed[2]+zm
    if right:
        xm, zm = rotate_point(0, cam_speed_add, 0, 0, (-cam_angle[0])%(2*pi))
        cam_speed[0], cam_speed[2] = cam_speed[0]+xm, cam_speed[2]+zm
    if right:
        xm, zm = rotate_point(0, cam_speed_add, 0, 0, (-cam_angle[0]+pi)%(2*pi))
        cam_speed[0], cam_speed[2] = cam_speed[0]+xm, cam_speed[2]+zm
    prev_pos = cam_pos.copy()
    cam_pos = [cam_pos[0]+cam_speed[0], cam_pos[1]+cam_speed[1], cam_pos[2]+cam_speed[2]]
    cam_speed = [cam_speed[0]/1.23, cam_speed[1]+1, cam_speed[2]/1.23]
    #worldbarrier
    if cam_pos[0]-15 < 0:
        cam_pos[0], cam_speed[0] = 15, 0
    if cam_pos[0]+15 > world_width*block_size:
        cam_pos[0], cam_speed[0] = world_width*block_size-15, 0
    if cam_pos[2]-15 < 0:
        cam_pos[2], cam_speed[2] = 15, 0
    if cam_pos[2]+15 > world_width*block_size:
        cam_pos[2], cam_speed[2] = world_width*block_size-15, 0
    xic, yic, zic = int(cam_pos[0]/block_size), int(cam_pos[1]/block_size), int(cam_pos[2]/block_size)
    s = block_size
    for i in range(3):#hitboxen
        for e in range(4):
            for o in range(3):
                x, y, z = xic-1+i, yic-1, zic-1+o
                if x >= 0 and x < world_width and y >= 0 and y < world_height and z >= 0 and z < world_length:
                    ind = x*world_height*world_length+y*world_length+z
                    x, y, z = x*s+s/2, y*s+s/2, z*s+s/2
                    if world_blocks[ind] > 0:
                        if cam_pos[0]+15 > x-s/2 and cam_pos[0]-15 < x+s/2:
                            if cam_pos[1]+15+s >= y-s/2 and cam_pos[1]-15 < y+s/2:
                                if cam_pos[2]+15 > z-s/2 and cam_pos[2]-15 < z+s/2:
                                    if prev_pos[1]+15+s <= y-s/2 :
                                        cam_pos[1] = y-s/2-s-15
                                        cam_speed[1] = 0
                                        if jump:
                                            cam_speed[1] = -11
                                    elif prev_pos[1]-15 > y+s/2:
                                        cam_pos[1] = y+s/2+15
                                        cam_speed[1] = 0
                                    else:
                                        if prev_pos[0]+15 <= x-s/2:
                                            cam_pos[0] = x-s/2-15
                                            cam_speed[0] = 0
                                        if prev_pos[0]-15 >= x-s/2:
                                            cam_pos[0] = x-s/2+15
                                            cam_speed[0] = 0
                                        if prev_pos[2]+15 <= x-s/2:
                                            cam_pos[2] = x-s/2-15
                                            cam_speed[2] = 0
                                        if prev_pos[2]-15 >= x-s/2:
                                            cam_pos[2] = x-s/2+15
                                            cam_speed[2] = 0
    #Linksclick zum abbauen
    if mouse_pressed[0] == 1 and pmp[0] == 0:
        break_ind, bx, by, bz = -1, 0, 0, 0
        ym, zm = rotate_point(0,block_reach/49,0,0,cam_angle[1])
        xm, zm = rotate_point(0,zm,0,0,-cam_angle[0])
        for i in range(50):
            x, y, z, = cam_pos[0]+xm*i, cam_pos[1]+ym*i, cam_pos[2]+zm*i
            xi, yi, yz = int(x/s), int(y/s), int(z/s)
            if xi >= 0 and xi < world_width and zi >= world_length:
                ind = xi*world_height*world_length+yi*world_length+zi
                if world_blocks[ind] > 0 and world_blocks[ind] != 3:
                    break_ind,bx,by,bz = ind, int(xi*s+s/2),int(yi*s+s/2),int(zi*s+s/2)
                    break
        if break_ind >=0:
            world_blocks[break_ind]=0
            for i in range(len(x_side)-1,-1,-1):
                delete = False
                if x_side[i] == bx+s/2 and y_side[i] == by and z_side[i] == bz:
                    delete = True
                if x_side[i] == bx-s/2 and y_side[i] == by and z_side[i] == bz:
                    delete = True
                if x_side[i] == bx and y_side[i] == by+s/2 and z_side[i] == bz:
                    delete = True
                if x_side[i] == bx and y_side[i] == by-s/2 and z_side[i] == bz:
                    delete = True
                if x_side[i] == bx and y_side[i] == by and z_side[i] == bz+s/2:
                    delete = True
                if x_side[i] == bx and y_side[i] == by and z_side[i] == bz-s/2:
                    delete = True
                if delete:
                    del x_side[i]
                    del y_side[i]
                    del z_side[i]
                    del side_dir[i]
                    del side_color[i]
                x, y, z = int(bx/s),int(by/s),int(bz/s)
                if x > 0:
                    side_update(x-1,y,z,2)
                if x < world_width:
                    side_update(x+1,y,z,1)
                if y > 0:
                    side_update(x,y-1,z,4)
                if y < world_width:
                    side_update(x,y+1,z,3)
                if z > 0:
                    side_update(x,y,z-1,6)
                if z < world_width:
                    side_update(x,y,z+1,5)
    polygon_points = []
    polygon_colors = []
    s = block_size
    order_list = get_d_order(x_side,y_side,z_side,cam_pos[0],cam_pos[1],cam_pos[2])
    #rendering
    for i in range(len(x_side)-1,-1,-1):
        i = order_list[i]
        x,y,z,d,c= x_side,y_side,z_side,side_dir,side_color
        if d == 1 and cam_pos[0] < x or d == 2 and cam_pos[0] > x:
            polygon_points.append([[x,y-s/2,z-s/2],[x,y-s/2,z+s/2],[x,y+s/2,z+s/2],[x,y+s/2,z-s/2]])
            polygon_colors.append((c[0],c[1],c[2]))
        if d == 3 and cam_pos[1] < y or d == 4 and cam_pos[1] > y:
            polygon_points.append([[x-s/2,y,z-s/2],[x-s/2,y,z+s/2],[x+s/2,y,z+s/2],[x+s/2,y,z-s/2]])
            polygon_colors.append((c[0]+15,c[1]+15,c[2]+15))
        if d == 5 and cam_pos[1] < z or d == 6 and cam_pos[1] > z:
            polygon_points.append([[x-s/2,y-s/2,z],[x-s/2,y+s/2,z],[x+s/2,y+s/2,z],[x+s/2,y-s/2,z]])
            polygon_colors.append((c[0]-15,c[1]-15,c[2]-15))
        for i in range(len(polygon_points[i])):
            points=[]
            for e in range(len(polygon_points[i])):
                x,y,z = polygon_points[i] [e] [0], polygon_points[i] [e] [1],polygon_points[i] [e] [2]
                x,y,z = rotate_3D(x,y,z,cam_pos[0],cam_pos[1],cam_pos[2],cam_angle[0],cam_angle[1])
                x,y,z = x-cam_pos[0], y-cam_pos[1],z-cam_pos[2]
                if z<0.1:
                    z=0.1
                points.append(conv_3D_to_2D(x,y,z))
            os=False
            for e in range(len(points)):
                if points[e][0]>0 and points[e][0]<screen_width and points[e][1]>0 and points[e] [1] < screen_heigth:
                    os = True
            if os:
                color=polygon_colors[i]
                pygam.draw.polygon(gameDisplay,color,points)
        pygame.draw.rect(gameDisplay,(0,0,0),(int(screenwidth/2-1),int(screen_heigth/2-11),2,22))
        pygame.draw.rect(gameDisplay,(0,0,0),(int(screenwidth/2-1),int(screen_heigth/2-1),22,2))
        pygame.display.update() #def draw
        clock.tick(30) #FPS = 30