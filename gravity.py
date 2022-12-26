import math

vel = 780
gravity = -9.81 * 1.35

xpos = 0
ypos = 0

xtarget = 960
ytarget = 61

for theta_d in (i / 1000 for i in range(0, 90 * 1000)):
    theta = math.radians(theta_d)
    xvel = vel * math.cos(theta)
    yvel_initial = vel * math.sin(theta)

    t = (xtarget - xpos) / xvel
    ypos_hit = ypos + yvel_initial * t + 0.5 * gravity * (t ** 2)

    off_by = ypos_hit - ytarget
    if abs(off_by) < 0.1:
        print(theta_d, off_by, math.sin(theta) * (xtarget-xpos))

# We know ypos_hit = ytarget, and t
# t**2 = (xtarget - xpos) ** 2 / xvel ** 2
# ytarget = ypos + yvel_initial * ((xtarget - xpos) / xvel) + (0.5 * gravity * ((xtarget - xpos) ** 2) / (xvel ** 2))
# ytarget = ypos + vel*sin(theta) * ((xtarget - xpos) / (vel*cos(theta)))) + (0.5 * gravity * ((xtarget - xpos) ** 2) / (vel*(cos(theta)) ** 2))

# Simplify using ypos = 0, xpos = 0

# ytarget = vel*sin(theta) * (xtarget / (vel*cos(theta)))) + (0.5 * gravity * (xtarget ** 2) / (vel*(cos(theta)) ** 2))







