from controller import Robot
import time
# For logging
import os
import sys
sys.path.append(r'/home/malasiaa/Documents/Github/line_follower_mujoco')
from utils.config import GENERATIONS, POP_SIZE, MAX_STEPS, TIME_STEP, SENSOR_THRESHOLD

robot = Robot()

# ——— Logging ———
# Setup logging path
project_path = robot.getProjectPath()
results_dir = os.path.join(project_path, "results")
os.makedirs(results_dir, exist_ok=True)

# Open log file and redirect prints
log_path = os.path.join(results_dir, "robot_log.txt")
log_file = open(log_path, "w")
sys.stdout = log_file
sys.stderr = log_file

# Map 3 binary sensor readings (l, c, r) to an index 0–7
def sensors_to_index(l, c, r):
    return (l << 2) | (c << 1) | r #bitwise operators

# Setting communication
# Receiver (to get genome from supervisor)
receiver = robot.getDevice("receiver")
receiver.setChannel(3)
receiver.enable(TIME_STEP)

# Emitter (to send initial handshake "READY" and fitness back)
emitter = robot.getDevice("emitter")
emitter.setChannel(4)

# Motors and sensors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

# IR sensors
ir_left = robot.getDevice("gs0")
ir_center = robot.getDevice("gs1")
ir_right = robot.getDevice("gs2")
ir_left.enable(TIME_STEP)
ir_center.enable(TIME_STEP)
ir_right.enable(TIME_STEP)

# Motor position (to calculate distance)
left_position_sensor = left_motor.getPositionSensor()
right_position_sensor = right_motor.getPositionSensor()
left_position_sensor.enable(TIME_STEP)
right_position_sensor.enable(TIME_STEP)
# To calculate distance
WHEEL_RADIUS = 0.02

# ——— MAIN LOOP ———
def main_loop (generations, pop_size):
    loop_count = 0
    
    while robot.step(TIME_STEP) != -1:        
        
        times_attempt = 2
        for _ in range(times_attempt):   # 2 steps = ~64 ms
            emitter.send("READY".encode("utf-8"))
            print("[Robot] Sent READY")
            if robot.step(TIME_STEP) == -1:
                quit(0)
                
        # Wait for genome
        while receiver.getQueueLength() == 0:
            print("[Robot] Waiting genome...")
            if robot.step(TIME_STEP) == -1:
                quit(0)
            pass   
                
        if receiver.getQueueLength() > 0:
            message = receiver.getData()
            receiver.nextPacket()
            print("[Robot] Genome received:", message)   
            genome = [float(x) for x in message.split(",")]
        
        left_motor.setPosition(float("inf"))
        right_motor.setPosition(float("inf"))
        
        initial_left_position = left_position_sensor.getValue()
        initial_right_position = right_position_sensor.getValue()

        # Evaluate genome
        max_steps = MAX_STEPS
        fitness = 0.0
        
        for step in range(max_steps):
            if robot.step(TIME_STEP) == -1:
                break
        
            # Read IR sensors and binarize
            l = int(ir_left.getValue()   < SENSOR_THRESHOLD)
            c = int(ir_center.getValue() < SENSOR_THRESHOLD)
            r = int(ir_right.getValue()  < SENSOR_THRESHOLD)
        
            idx = sensors_to_index(l, c, r)
            
            # Selecting genome according with binary readings
            left_speed  = abs(genome[2 * idx])
            right_speed = abs(genome[2 * idx + 1])
        
            left_motor.setVelocity(left_speed)
            right_motor.setVelocity(right_speed)
        
            # --- Fitness: reward being on track + moving fast ---
            speed = ((left_speed) + (right_speed)) / 2
        
            if c == 1:
                fitness += 1.0 + speed  # Bonus for tracking while fast
            elif l == 1 and r == 1:
                fitness += 0.1  # Small reward for being close to the line
            elif speed > 6:
                fitness += 2
            else:
                fitness -= 20  # Penalize for being completely off
        
            # Optional: cap fitness to avoid explosions
            fitness = max(fitness, 0)
            
            # Calculating distance
            current_left_position = left_position_sensor.getValue()
            current_right_position = right_position_sensor.getValue()
            delta_left = current_left_position - initial_left_position
            delta_right = current_right_position - initial_right_position
            # Distance per wheel
            distance_left = delta_left * WHEEL_RADIUS
            distance_right = delta_right * WHEEL_RADIUS
            # AVG Distance
            distance_traveled = (distance_left + distance_right) / 2.0
            
            print(f"[Robot] Step {step} | IR: {l},{c},{r} | idx: {idx} | L_speed: {left_speed:.2f}, R_speed: {right_speed:.2f} | Fitness: {fitness:.2f} | Distance: {distance_traveled:.2f}")
        

        
        # Send fitness back to supervisor
        msg = f"fitness:{fitness}, distance: {distance_traveled}"
        emitter.send(msg.encode("utf-8"))
        print("[Robot] Fitness sent back:", msg)
        loop_count += 1
        if loop_count == generations*pop_size : #Generations * popsize
            print("[Robot] Closing ebuck controller.")
            break
    
    # Flushing logs
    log_file.flush()
    log_file.close()


generations, pop_size = GENERATIONS, POP_SIZE
main_loop(generations, pop_size)