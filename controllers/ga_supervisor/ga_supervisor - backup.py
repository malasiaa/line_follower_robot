from controller import Supervisor
import random
import time

print(">>> GA Supervisor has started!")

POP_SIZE = 10
GENOME_SIZE = 16  # 8 sensor states × 2 motor speeds
GENERATIONS = 20
MAX_SPEED = 6.28  # Example max motor speed
TIME_STEP = 32

supervisor = Supervisor()
emitter = supervisor.getDevice("emitter")
emitter.setChannel(3)


receiver = supervisor.getDevice("receiver")
receiver.setChannel(4)
receiver.enable(TIME_STEP)

time_step = int(supervisor.getBasicTimeStep())

robot_node = supervisor.getFromDef("Nice_Epuck")

if robot_node is None:
    print("ERROR: supervisor.getFromDef(\"Nice_Epuck\") returned None!")
    quit(1)
else:
    print("GENOME WILL BE SENT TO:", robot_node.getDef())


def random_genome():
    return [random.uniform(-MAX_SPEED, MAX_SPEED) for _ in range(GENOME_SIZE)]


def evaluate_genome(genome):
    # 1) WAIT for “READY” from robot
    print("[Supervisor] Waiting for READY signal…")
    while supervisor.step(TIME_STEP) != -1:
        while receiver.getQueueLength() == 0:
            print("waiting")
            # Advance simulation
            if supervisor.step(TIME_STEP) == -1:
                # end of simulation
                return 0.0
                
        raw = receiver.getData()       # this is bytes, e.g. b"READY"
        if raw == "READY":
            print("[Supervisor] Received READY; now sending genome.")
    
        else:
            # if it was something else, ignore and keep waiting
            print(f"[Supervisor]   Ignored unexpected message: '{msg}'")
        
        # 2) Send genome
        genome_str = ",".join(f"{g:.4f}" for g in genome)
        print(genome_str)
        emitter.send(genome_str.encode("utf-8"))
        print("sent")
        
        # 3) Step and wait for “fitness:” reply for a fixed number of steps
        fitness = 0.0
       
        print("Number of packets:", receiver.getQueueLength())
        while receiver.getQueueLength() > 0:
            receiver.nextPacket()
            if supervisor.step(TIME_STEP) == -1:
                return 0.0
            
        while receiver.getQueueLength() == 0:
            if supervisor.step(TIME_STEP) == -1:
                return 0.0
            pass
            
        print("AFTER ")
        print("Number of packets:", receiver.getQueueLength())
        

        reply = receiver.getData()
        receiver.nextPacket()
        if reply.startswith("fitness:"):
            fitness = float(reply.split(":")[1])
            
        print("AFTER THE AFTER")
        print("Number of packets:", receiver.getQueueLength())
        # 4) Reset before returning
        supervisor.simulationResetPhysics()
        supervisor.simulationReset()
        supervisor.step(TIME_STEP)  # apply the reset
        break
        
    return fitness

def run_generation(population):
    """
    1) Evaluate each genome in `population` via evaluate_genome(genome)
    2) Collect fitnesses and select the top 2 (elitism)
    3) Produce a new_population via crossover + mutation
    4) Return (new_population, best_fitness)
    """
    fitnesses = []
    # 1) Evaluate
    for idx, genome in enumerate(population):
        print(f"[Supervisor] Evaluating individual {idx}")
        f = evaluate_genome(genome)
        fitnesses.append(f)
        if supervisor.step(TIME_STEP) == -1:
            return 0.0

    # 2) Sort by fitness descending
    ranked = sorted(zip(fitnesses, population), key=lambda x: x[0], reverse=True)
    best_fitness, best_genome = ranked[0]
    second_fitness, second_genome = ranked[1]
    print(f"[Supervisor] Top fitness this gen = {best_fitness:.4f}")

    # 3) Build next generation (elitism + crossover + mutation)
    new_population = [best_genome, second_genome]
    while len(new_population) < POP_SIZE:
        # Simple tournament among the top two
        p1, p2 = random.sample([best_genome, second_genome], 2)
        cp = random.randint(1, GENOME_SIZE - 1)
        child = p1[:cp] + p2[cp:]
        # mutation step
        for i in range(GENOME_SIZE):
            if random.random() < 0.1:  # 10% mutation rate
                child[i] += random.uniform(-1.0, 1.0)
                child[i] = max(min(child[i], MAX_SPEED), -MAX_SPEED)
                if supervisor.step(TIME_STEP) == -1:
                    return 0.0
        new_population.append(child)
        if supervisor.step(TIME_STEP) == -1:
            return 0.0
            
    return new_population, best_fitness

# ——— MAIN GA LOOP ———
population = [random_genome() for _ in range(POP_SIZE)]

for gen in range(GENERATIONS):
    print(f"\n=== Generation {gen} ===")
    population, best_fitness = run_generation(population)
print("Simulation Finished!")



