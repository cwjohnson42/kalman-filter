from robot import get_robot_position
from commands import get_speed, where_robot, where_markers, where_all
from math import atan2

ADDRESS = ("0.0.0.0", 55555)

commands.open_connection(ADDRESS)

markers = where_markers()

for marker_number in markers:
    if (marker_number == "time" or marker_number == "robot"):
        continue
    waypoints.append(markers[marker_number]["center"])

states = []
timestamps = []

while len(waypoints) > 0:
    robot_speed = get_speed()
    diff = robot_speed[1] - robot_speed[0]
    states.append([robot_speed[0], robot_speed[1], diff])
    timestamps.append(float(where_all()['time']))
    if len(states) > 8:
        states.pop(0)
        timestamps.pop(0)
    sensor_position = get_robot_position()
    sensor_orientation = where_robot()['orientation']
    angle = atan2(sensor_orientation[1], sensor_orientation[0])
    (x, y, new_angle) = get_estimated_position(states, [sensor_position[0], sensor_position[1], angle])
    if follow_vector((waypoints[0][0], waypoints[0][1]), (x, y), new_angle):
        waypoints.pop(0)
    sleep(.05) #the follow_vector also sleeps for 0.05 seconds
