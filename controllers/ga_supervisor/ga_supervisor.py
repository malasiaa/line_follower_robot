from controller import Supervisor
import random
import time
# For logging
import os
import sys
sys.path.append(r'/home/malasiaa/Documents/Github/line_follower_mujoco')
from utils.config import GENERATIONS, POP_SIZE, GENOME_SIZE, MAX_SPEED, TIME_STEP


supervisor = Supervisor()

# ——— Logging ———
# Setup logging path
project_path = supervisor.getProjectPath()
results_dir = os.path.join(project_path, "results")
os.makedirs(results_dir, exist_ok=True)

# Open log file and redirect prints
log_path = os.path.join(results_dir, "supervisor_log.txt")
log_file = open(log_path, "w")
sys.stdout = log_file
sys.stderr = log_file


# Setting communication
emitter = supervisor.getDevice("emitter")
emitter.setChannel(3)

receiver = supervisor.getDevice("receiver")
receiver.setChannel(4)
receiver.enable(TIME_STEP)

time_step = int(supervisor.getBasicTimeStep())

robot_node = supervisor.getFromDef("Nice_Epuck")
print("[Supervisor] >>> GA Supervisor has started!")
print("[Supervisor] GENOME WILL BE SENT TO:", robot_node.getDef())


def random_genome():
    return [random.uniform(-MAX_SPEED, MAX_SPEED) for _ in range(GENOME_SIZE)]


def evaluate_genome(genome):
    # 1) WAIT for “READY” from robot
    print("[Supervisor] Waiting for READY signal…")
    while supervisor.step(TIME_STEP) != -1:
        while receiver.getQueueLength() == 0:
            print("[Supervisor] Waiting...")
            # Advance simulation
            if supervisor.step(TIME_STEP) == -1:
                # end of simulation
                return 0.0
                
        raw = receiver.getData()       # this is bytes, e.g. b"READY"
        if raw == "READY":
            print("[Supervisor] Received READY; now sending genome.")
    
        else:
            # if it was something else, ignore and keep waiting
            print(f"[Supervisor] Ignored unexpected message: '{msg}'")
        
        # 2) Send genome
        genome_str = ",".join(f"{g:.4f}" for g in genome)
        print(genome_str)
        emitter.send(genome_str.encode("utf-8"))
        #print("sent")
        
        # 3) Step and wait for “fitness:” reply for a fixed number of steps
        fitness = 0.0
             
        while receiver.getQueueLength() > 0:
            receiver.nextPacket()
            if supervisor.step(TIME_STEP) == -1:
                return 0.0
            
        while receiver.getQueueLength() == 0:
            if supervisor.step(TIME_STEP) == -1:
                return 0.0
            pass
            
        reply = receiver.getData()
        receiver.nextPacket()
        if reply.startswith("fitness:"):
            fitness = float(reply.split(",")[0].split(":")[1])
            print(f"[Supervisor] Fitness received: {fitness}")
            distance = float(reply.split(",")[1].split(":")[1])
            print(f"[Supervisor] Distance received: {distance}")
            
        # 4) Reset before returning
        supervisor.simulationResetPhysics()
        supervisor.simulationReset()
        supervisor.step(TIME_STEP)  # apply the reset
        break
        
    return fitness, distance

def run_generation(population):
    """
    1) Evaluate each genome in `population` via evaluate_genome(genome)
    2) Collect fitnesses and select the top 2 (elitism)
    3) Produce a new_population via crossover + mutation
    4) Return (new_population, best_fitness)
    """
    fitnesses = []
    distanceses = []
    # 1) Evaluate
    for idx, genome in enumerate(population):
        print(f"[Supervisor] Evaluating individual {idx}")
        f, dist = evaluate_genome(genome)
        distanceses.append(dist)
        fitnesses.append(f)
        if supervisor.step(TIME_STEP) == -1:
            return 0.0

    # 2) Sort by fitness descending
    ranked = sorted(zip(fitnesses, population), key=lambda x: x[0], reverse=True)
    best_fitness, best_genome = ranked[0]
    second_fitness, second_genome = ranked[1]
    print(f"[Supervisor] Top fitness this gen = {best_fitness:.4f}, {best_genome}")
    ranked_dist = sorted(zip(distanceses, population), key=lambda x: x[0], reverse=True)
    best_dist, dist_genome = ranked_dist[0]
    print(f"[Supervisor] Top distance this gen = {best_dist:.4f}, {dist_genome}")
    
    # 3) Build next generation (elitism + crossover + mutation)
    new_population = [best_genome, second_genome]
    while len(new_population) < POP_SIZE:
        # Simple tournament among the top two
        p1, p2 = random.sample([best_genome, second_genome], 2)
        cp = random.randint(1, GENOME_SIZE - 1)
        child = p1[:cp] + p2[cp:]
        # mutation step
        for i in range(GENOME_SIZE):
            if random.random() < 0.1:  # mutation rate
                child[i] += random.uniform(-1.0, 1.0)
                child[i] = max(min(child[i], MAX_SPEED), -MAX_SPEED)
                if supervisor.step(TIME_STEP) == -1:
                    return 0.0
        new_population.append(child)
        if supervisor.step(TIME_STEP) == -1:
            return 0.0
            
    return new_population, best_fitness

# ——— Variables to store  best results ———
best_overall_fitness = -float("inf") # worst possible scenario - still playing with fitness func, it may go neg
best_overall_genome = []


# ——— MAIN GA LOOP ———
population = [random_genome() for _ in range(POP_SIZE)]

for gen in range(GENERATIONS):
    print(f"\n[Supervisor] === Generation {gen} ===")
    population, best_fitness = run_generation(population)
    
    if best_fitness > best_overall_fitness:
        best_overall_fitness = best_fitness
        best_overall_genome = population[0]  # Best genome always at index 0

# stopping simulation
supervisor.simulationQuit(0)   
print("[Supervisor] Simulation Finished!")

# ——— Outputs ———
# Print best genome and fitness
print("\n[Supervisor] >>> BEST GENOME FOUND:")
print(f"[Supervisor] Fitness: {best_overall_fitness:.4f}")
print("[Supervisor] Genome:", [round(g, 4) for g in best_overall_genome])

# Save to file
best_genome_path = os.path.join(results_dir, "best_genome.txt")
with open(best_genome_path, "w") as f:
    f.write(f"Best Fitness: {best_overall_fitness:.4f}\n")
    f.write("Best Genome:\n")
    f.write(",".join(f"{g:.4f}" for g in best_overall_genome))

print("[Supervisor] Best genome saved to 'best_genome.txt!'")

# Flushing logs
log_file.flush()
log_file.close()


