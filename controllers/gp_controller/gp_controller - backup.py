from controller import Robot
import time

TIME_STEP = 32
SENSOR_THRESHOLD = 1300

# Map 3 binary sensor readings (l, c, r) to an index 0–7
def sensors_to_index(l, c, r):
    return (l << 2) | (c << 1) | r

robot = Robot()

# Receiver (to get genome from supervisor)
receiver = robot.getDevice("receiver")
receiver.setChannel(3)
receiver.enable(TIME_STEP)

# Emitter (to send fitness back)
emitter = robot.getDevice("emitter")
emitter.setChannel(4)

# Motors and sensors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

ir_left = robot.getDevice("gs0")
ir_center = robot.getDevice("gs1")
ir_right = robot.getDevice("gs2")

ir_left.enable(TIME_STEP)
ir_center.enable(TIME_STEP)
ir_right.enable(TIME_STEP)

loop_count = 0
while robot.step(TIME_STEP) != -1:        
    # Wait for genome
    times_attempt = 2
    for _ in range(times_attempt):   # 2 steps = ~64 ms
        emitter.send("READY".encode("utf-8"))
        print("[Robot]   Sent READY")
        if robot.step(TIME_STEP) == -1:
            quit(0)
    
    
    #emitter.send("READY".encode("utf-8"))
    #print("[Robot]   Sent READY")
    
    while receiver.getQueueLength() == 0:
        print("waiting genome")
        if robot.step(TIME_STEP) == -1:
            quit(0)
        pass   
            
    if receiver.getQueueLength() > 0:
        message = receiver.getData()
        receiver.nextPacket()
        print("Genome received:", message)   
        genome = [float(x) for x in message.split(",")]
    
    left_motor.setPosition(float("inf"))
    right_motor.setPosition(float("inf"))
    
    # Evaluate genome
    max_steps = 500
    fitness = 0.0
    
    for step in range(max_steps):
        if robot.step(TIME_STEP) == -1:
            break
    
        # Read IR sensors and binarize
        l = int(ir_left.getValue()   < SENSOR_THRESHOLD)
        c = int(ir_center.getValue() < SENSOR_THRESHOLD)
        r = int(ir_right.getValue()  < SENSOR_THRESHOLD)
    
        idx = sensors_to_index(l, c, r)
    
        left_speed  = abs(genome[2 * idx])
        right_speed = abs(genome[2 * idx + 1])
    
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
    
        # --- Fitness: reward being on track + moving fast ---
        speed = ((left_speed) + (right_speed)) / 2
    
        if c == 1:
            fitness += 1.0 + speed  # Bonus for tracking while fast
        elif l == 1 or r == 1:
            fitness += 0.1  # Small reward for being close to the line
        else:
            fitness -= 20  # Penalize for being completely off
    
        # Optional: cap fitness to avoid explosions
        fitness = max(fitness, 0)
        
        print(f"Step {step} | IR: {l},{c},{r} | idx: {idx} | L_speed: {left_speed:.2f}, R_speed: {right_speed:.2f} | Fitness: {fitness:.2f}")
    
    # Send fitness back to supervisor
    msg = f"fitness:{fitness}"
    emitter.send(msg.encode("utf-8"))
    print("Fitness sent back:", msg)
    loop_count += 1
    if loop_count == 20*10:
        print("Closing ebuck controller")
        break
    