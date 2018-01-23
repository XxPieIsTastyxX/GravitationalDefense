from math import pow, sqrt, cos, pi


GRAVITY_CONSTANT = 10
PLANET_MASS = 3200

def approx_cos(ang):
    #outputs = [1.0, 0.999, 0.999, 0.998, 0.998, 0.996, 0.995, 0.993, 0.992, 0.99, 0.987, 0.985, 0.982, 0.979, 0.975, 0.972, 0.968, 0.964, 0.96, 0.955, 0.951, 0.946, 0.94, 0.935, 0.929, 0.923, 0.917, 0.911, 0.904, 0.898, 0.891, 0.883, 0.876, 0.868, 0.86, 0.852, 0.844, 0.835, 0.827, 0.818, 0.809, 0.799, 0.79, 0.78, 0.77, 0.76, 0.75, 0.739, 0.728, 0.718, 0.707, 0.695, 0.684, 0.673, 0.661, 0.649, 0.637, 0.625, 0.612, 0.6, 0.587, 0.575, 0.562, 0.549, 0.535, 0.522, 0.509, 0.495, 0.481, 0.467, 0.453, 0.439, 0.425, 0.411, 0.397, 0.382, 0.368, 0.353, 0.338, 0.323, 0.309, 0.294, 0.278, 0.263, 0.248, 0.233, 0.218, 0.202, 0.187, 0.171, 0.156, 0.14, 0.125, 0.109, 0.094, 0.078, 0.062, 0.047, 0.031, 0.015, 0.0, -0.015, -0.031, -0.047, -0.062, -0.078, -0.094, -0.109, -0.125, -0.14, -0.156, -0.171, -0.187, -0.202, -0.218, -0.233, -0.248, -0.263, -0.278, -0.294, -0.309, -0.323, -0.338, -0.353, -0.368, -0.382, -0.397, -0.411, -0.425, -0.439, -0.453, -0.467, -0.481, -0.495, -0.509, -0.522, -0.535, -0.549, -0.562, -0.575, -0.587, -0.6, -0.612, -0.625, -0.637, -0.649, -0.661, -0.673, -0.684, -0.695, -0.707, -0.718, -0.728, -0.739, -0.75, -0.76, -0.77, -0.78, -0.79, -0.799, -0.809, -0.818, -0.827, -0.835, -0.844, -0.852, -0.86, -0.868, -0.876, -0.883, -0.891, -0.898, -0.904, -0.911, -0.917, -0.923, -0.929, -0.935, -0.94, -0.946, -0.951, -0.955, -0.96, -0.964, -0.968, -0.972, -0.975, -0.979, -0.982, -0.985, -0.987, -0.99, -0.992, -0.993, -0.995, -0.996, -0.998, -0.998, -0.999, -0.999, -0.999, -0.999, -0.999, -0.998, -0.998, -0.996, -0.995, -0.993, -0.992, -0.99, -0.987, -0.985, -0.982, -0.979, -0.975, -0.972, -0.968, -0.964, -0.96, -0.955, -0.951, -0.946, -0.94, -0.935, -0.929, -0.923, -0.917, -0.911, -0.904, -0.898, -0.891, -0.883, -0.876, -0.868, -0.86, -0.852, -0.844, -0.835, -0.827, -0.818, -0.809, -0.799, -0.79, -0.78, -0.77, -0.76, -0.75, -0.739, -0.728, -0.718, -0.707, -0.695, -0.684, -0.673, -0.661, -0.649, -0.637, -0.625, -0.612, -0.6, -0.587, -0.574, -0.562, -0.549, -0.535, -0.522, -0.509, -0.495, -0.481, -0.467, -0.453, -0.439, -0.425, -0.411, -0.397, -0.382, -0.368, -0.353, -0.338, -0.323, -0.309, -0.294, -0.278, -0.263, -0.248, -0.233, -0.218, -0.202, -0.187, -0.171, -0.156, -0.14, -0.125, -0.109, -0.094, -0.078, -0.062, -0.047, -0.031, -0.015, 0.0, 0.015, 0.031, 0.047, 0.062, 0.078, 0.094, 0.109, 0.125, 0.14, 0.156, 0.171, 0.187, 0.202, 0.218, 0.233, 0.248, 0.263, 0.279, 0.294, 0.309, 0.323, 0.338, 0.353, 0.368, 0.382, 0.397, 0.411, 0.425, 0.439, 0.454, 0.467, 0.481, 0.495, 0.509, 0.522, 0.535, 0.549, 0.562, 0.575, 0.587, 0.6, 0.612, 0.625, 0.637, 0.649, 0.661, 0.673, 0.684, 0.695, 0.707, 0.718, 0.728, 0.739, 0.75, 0.76, 0.77, 0.78, 0.79, 0.799, 0.809, 0.818, 0.827, 0.835, 0.844, 0.852, 0.86, 0.868, 0.876, 0.883, 0.891, 0.898, 0.904, 0.911, 0.917, 0.923, 0.929, 0.935, 0.94, 0.946, 0.951, 0.955, 0.96, 0.964, 0.968, 0.972, 0.975, 0.979, 0.982, 0.985, 0.987, 0.99, 0.992, 0.993, 0.995, 0.996, 0.998, 0.998, 0.999, 0.999]
    #return outputs[int(round(ang) % 400)]
    return cos(ang * pi / 200)

def vec_sum(vec1, vec2):
    vec3 = vec1[0] + vec2[0], vec1[1] + vec2[1]
    return vec3

def vec_scale(vec, num):
    vec2 = vec[0] * num, vec[1] * num
    return vec2

def norm_sqr(vec):
    total = 0
    for c in vec:
        total += pow(c, 2)
    return total

         
def move_moon(moon, time):
    new_angle = moon.angle - 400 * time / moon.period
    if new_angle < 0:
        new_angle += 400
    moon.angle = new_angle
    moon.update_pos()

def move_ship(ship, moons, time):                                                       ###  # #  # #  ###  ###  ###  ###  #
    gravity_mod = GRAVITY_CONSTANT * PLANET_MASS / pow(norm_sqr(ship.position), 1.5)    # #  # #  # #  #     #   #    #    #
    body_gravity = gravity_mod * -ship.position[0], gravity_mod * -ship.position[1]     ###  ###  ###  ###   #   #    ###  #
    new_velocity = vec_sum(ship.velocity, vec_scale(body_gravity, time))                #    # #   #     #   #   #      #   
    ship.velocity = new_velocity                                                        #    # #   #   ###  ###  ###  ###  #
    
    velocity_mag = sqrt(norm_sqr(ship.velocity))
    new_velocity = vec_sum(ship.velocity, vec_scale(ship.velocity, -ship.thrust*time/velocity_mag))
    ship.velocity = new_velocity
    
    for m in moons:
        relative_vec = vec_sum(m.position, vec_scale(ship.position, -1))
        gravity_mod = GRAVITY_CONSTANT * m.mass / pow(norm_sqr(relative_vec), 1.5)
        body_gravity = gravity_mod * relative_vec[0], gravity_mod * relative_vec[1]
        new_velocity = vec_sum(ship.velocity, vec_scale(body_gravity, time))
        ship.velocity = new_velocity
        
    new_position = vec_sum(ship.position, vec_scale(ship.velocity, time))
    ship.last_move = vec_sum(new_position, vec_scale(ship.position, -1))
    ship.position = new_position
    