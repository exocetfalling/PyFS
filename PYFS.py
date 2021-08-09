# Imports

import math
import pygame
import pygame.freetype  # Import the freetype module.

# Variables

# Polar coordinates as as commonly used in physics (ISO 80000-2:2019 convention): 
# radial distance r (distance to origin), 
# polar angle theta (angle with respect to polar axis), 
# azimuthal angle phi (angle of rotation from the initial meridian plane).

a_theta_deg = 0
a_theta_rad = 0
a_phi_deg = 0
a_phi_rad = 0
a_radial_velocity = 50

a_accel_x = 0
a_accel_y = 0
a_accel_z = 0

a_angular_accel_x = 0
a_angular_accel_y = 0
a_angular_accel_z = 0

a_airspeed_indicated = 0
a_alt = 0

a_roll_deg = 0
a_roll_rad = 0

a_alpha_rad = 0
a_beta_rad = 0

a_cl_wing = 0
a_cl_tailplane_horizontal = 0
a_cl_tailplane_vertical = 0

a_cl_elevator = 0
a_cl_aileron_left = 0
a_cl_aileron_right = 0
a_cl_rudder = 0

a_cd_wing = 0
a_dynp = 0
a_air_density = 1.3
a_airspeed_true = 50

a_lift_force_elevator = 0
a_lift_force_aileron_left = 0
a_lift_force_aileron_right = 0
a_lift_force_rudder = 0

a_lift_force_wing = 0
a_lift_force_tailplane_horizontal = 0
a_lift_force_tailplane_vertical = 0

a_drag_force_wing = 0

# Axes are defined as:
# For aircraft:
# X: left -ve, right +ve
# Y: aft -ve, right +ve
# Z: down -ve, up +ve

# For world:
# X: west -ve, east +ve
# Y: south -ve, north +ve
# Z: down -ve, up +ve

w_x_velocity = 0
w_y_velocity = 0
w_z_velocity = 0

w_vec_velocity = [0, 0, 0]

w_x_pos = 0
w_y_pos = 0
w_z_pos = 0

w_vec_pos = [0, 0, 0]

a_elevator_angle_rad = 0
a_aileron_angle_rad = 0
a_rudder_angle_rad = 0

# Lengths in m
c_dimensions_aircraft_length = 10
c_dimensions_aircraft_width = 20
c_dimensions_aircraft_height = 4

c_wing_incidence = math.pi/60

c_position_tailplane_horizontal = -9
c_position_tailplane_vertical = -9
c_position_wing = 0
c_position_elevator = -10
c_position_aileron_left = -18
c_position_aileron_right = 18
c_position_rudder = -10

# Areas in m^2
c_area_wing = 50
c_area_aileron = 10
c_area_elevator = 10
c_area_rudder = 10

# Masses in kg
c_mass_aircraft = 1000

# MOIs in kg m^2
# Using formula:
# MOI = 1/12 * mass * (length)^2
c_moi_pitch = 8333
c_moi_roll = 33333
c_moi_yaw = 8333

pygame.init()
SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 30
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()

# Functions
def Calc_Velocity_World(axis, total_vel, angle_azimuthal, angle_polar): 
    if axis == 'x':
        return (total_vel * math.sin(angle_azimuthal)) * math.sin(angle_polar)
    if axis == 'y':
        return (total_vel * math.cos(angle_azimuthal)) * math.sin(angle_polar)
    if axis == 'z':
        return (total_vel * math.cos(angle_polar)) * math.cos(angle_azimuthal)

def Calc_Force_Angular_Acc(axis, force_magnitude, distance_from_pivot):
    if (axis == 'x'):
        return c_moi_pitch * force_magnitude * distance_from_pivot
    if (axis == 'y'):
        return c_moi_roll * force_magnitude * distance_from_pivot
    if (axis == 'z'):
        return c_moi_yaw * force_magnitude * distance_from_pivot

def Calc_Angular_Vel():
    pass

def Calc_Force_Acc(force_magnitude, mass_kg):
    return force_magnitude / mass_kg

def Calc_Integral(value, time_interval):
    return value * time_interval

def Calc_Lift_Coeff(angle_alpha_rad):
    a = -0.520870722846
    b = 5.72957795131
    c = -0.520870722846

    x1 = -math.pi
    y1 = 0
    x2 = -math.pi/12
    y2 = -1.5
    x3 = -math.pi/12
    y3 = 1.5
    x4 = math.pi
    y4 = 0


    if ((angle_alpha_rad > (-math.pi)) and (angle_alpha_rad <= (-math.pi/12))):
        return (a * (angle_alpha_rad - x1) + y1)
    
    if ((angle_alpha_rad > (-math.pi/12)) and (angle_alpha_rad <= (math.pi/12))):
        return (b * (angle_alpha_rad - x2) + y2)

    if ((angle_alpha_rad > (math.pi/12)) and (angle_alpha_rad <= (math.pi))):
        return (c * (angle_alpha_rad - x3) + y3)

def Calc_Drag_Coeff(angle_rad):
    return math.sin(angle_rad)

def Convert_Angle_Rad_To_Deg(angle_rad):
    return angle_rad * 57.2958

def Convert_Angle_Deg_To_Rad(angle_deg):
    return angle_deg / 57.2958

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.



font = pygame.font.SysFont('Courier', 16)

while True:

    dt = clock.tick(FPS) / 1000
    debug_text = \
        '\nX Pos: ' + str(w_x_pos) + \
        '\nY Pos: ' + str(w_y_pos) + \
        '\nZ Pos: ' + str(w_z_pos) + \
        '\nTHETA: ' + str(a_theta_deg) + \
        '\nPHI: ' + str(a_phi_deg)
    a_phi_deg = (a_phi_deg + 360) % 360
    a_theta_deg = (a_theta_deg + 360) % 360

    a_phi_rad = Convert_Angle_Deg_To_Rad(a_phi_deg)
    a_theta_rad = Convert_Angle_Deg_To_Rad(a_theta_deg)
    a_lift_force_wing = (0.5 * a_air_density * a_airspeed_true * a_airspeed_true * c_area_wing * a_cl_wing)
    a_cl_wing = Calc_Lift_Coeff(a_alpha_rad)

    w_x_velocity = Calc_Velocity_World('x', a_radial_velocity, a_phi_rad, a_theta_rad)
    w_y_velocity = Calc_Velocity_World('y', a_radial_velocity, a_phi_rad, a_theta_rad)
    w_z_velocity = Calc_Velocity_World('z', a_radial_velocity, a_roll_rad, a_theta_rad)

    w_vec_velocity = [w_x_velocity, w_y_velocity, w_z_velocity]

    w_x_pos = w_x_pos + w_x_velocity * dt
    w_y_pos = w_y_pos + w_y_velocity * dt
    w_z_pos = w_z_pos + w_z_velocity * dt

    keys=pygame.key.get_pressed()

    if keys[pygame.K_w]:
        a_theta_deg = a_theta_deg + 10 * dt

    if keys[pygame.K_s]:
        a_theta_deg = a_theta_deg - 10 * dt

    if keys[pygame.K_a]:
        a_phi_deg = a_phi_deg - 10 * dt

    if keys[pygame.K_d]:
        a_phi_deg = a_phi_deg + 10 * dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(pygame.Color('white'))
    blit_text(screen, debug_text, (20, 20), font)
    pygame.display.update()
