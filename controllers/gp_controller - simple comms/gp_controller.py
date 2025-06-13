from controller import Robot

TIME_STEP = 32

robot = Robot()
receiver = robot.getDevice("receiver")
receiver.enable(TIME_STEP)

while robot.step(TIME_STEP) != -1:
    if receiver.getQueueLength() > 0:
        message = receiver.getString()
        print(f"E-puck received: {message}")
        receiver.nextPacket()
