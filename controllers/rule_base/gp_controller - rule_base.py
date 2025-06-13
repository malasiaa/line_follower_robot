from controller import Robot

# Create the robot instance and setup
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# Ground sensors
sensor_names = ['gs0', 'gs1', 'gs2']  # left, center, right
ground_sensors = []
for name in sensor_names:
    sensor = robot.getDevice(name)
    sensor.enable(timestep)
    ground_sensors.append(sensor)

# Constants
MAX_SPEED = 6.28  # or whatever your max motor speed is
THRESHOLD = 1000  # Below = black, above = white

# Main loop
while robot.step(timestep) != -1:
    # Read sensor values
    sensor_values = [sensor.getValue() for sensor in ground_sensors]
    print("Raw sensor values:", sensor_values)
    
    # Convert to binary (0 = black, 1 = white)
    binary = [1 if v > THRESHOLD else 0 for v in sensor_values]
    left, center, right = binary

    # Behavior rules
    if center == 0 and left == 1 and right == 1:
        # on track, go straight
        left_motor.setVelocity(0.5 * MAX_SPEED)
        right_motor.setVelocity(0.5 * MAX_SPEED)
    elif left == 0:
        # black on left, turn left
        left_motor.setVelocity(0.1 * MAX_SPEED)
        right_motor.setVelocity(0.5 * MAX_SPEED)
    elif right == 0:
        # black on right, turn right
        left_motor.setVelocity(0.5 * MAX_SPEED)
        right_motor.setVelocity(0.1 * MAX_SPEED)
    else:
        # lost, stop or reverse slowly
        left_motor.setVelocity(0.0)
        right_motor.setVelocity(0.0)

