## Line Follower Robot (Webots) – Genetic Algorithm

This project involves training an e-puck robot using evolutionary computation, specifically Genetic Algorithms (GAs), to autonomously follow a path in a simulated environment.

It features a Webots simulation of a training setup for a line-following robot (E-puck) whose controller parameters are optimized using a GA. The robot runs a simple reactive controller (lookup table) that maps binary ground infrared sensor readings to wheel speeds. 
The GA evolves the speed pairs (genome) for each reading, according to the fitness received. The fitness is designed to maximize the speed at which the robot goes around the track. 

It includes ready-to-run controllers, utilities, and a sample world for evaluating performance on a track.
<div align="center">
  <img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/40360a25-42a3-4368-9045-11c362291982" />
</div>  

### Key features
- **Webots world** with an E-puck on a line track (`webots/worlds/line_tracking.wbt`).
- **Controllers** for both evolutionary training and execution (with logging and without):
  - `gp_controller`: runs a genome-parameterized reactive controller on the robot.
  - `ga_supervisor`: evaluates populations, assigns genomes, and logs fitness.
- **Utilities and config** in `webots/controllers/utils/` to adjust experiment settings.

## Repository structure
```
controllers/
  ga_supervisor/                 # GA-driven supervisor
  ga_supervisor - no_logging/    # Supervisor variant without disk logging
  ga_supervisor - simple comms/  # Minimal communications variant
  gp_controller/                 # Robot-side reactive controller (genome-parameterized)
  gp_controller - no_logging/    # Controller variant without disk logging
  gp_controller - simple comms/  # Minimal communications variant
  rule_base/                     # Example rule-based controller
  utils/                         # Shared config and helpers
protos/                          # E-puck and track protos
worlds/                          # line_tracking.wbt world file
requirements.txt                 # Python requirements for controllers
```

## Requirements
- Webots
- Python
- Packages required in `requirements.txt`:

## Quickstart
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Open Webots and load the world `webots/worlds/line_tracking.wbt`.
3. In the scene tree:
   - Set the Supervisor node's controller to `ga_supervisor` (or a variant).
   - Set the E-puck robot's controller to `gp_controller` (or a variant).
4. Click Run. The supervisor will evolve/evaluate controllers and communicate genomes to the robot controller.

## Controllers and variants
- `ga_supervisor/ga_supervisor.py`: GA supervisor with logging. Builds populations of length-16 genomes, handles evaluation, selection, crossover, and mutation.
- `gp_controller/gp_controller.py`: executes a genome on the robot by mapping 3 binary ground sensor readings (left, center, right) to one of 8 cases; for each case, two genome values set left and right wheel speeds.
- `- no_logging` variants: same behavior with file logging disabled.
- `- simple comms` variants: simplified communication, useful for debugging.
- `rule_base/gp_controller - rule_base.py`: example non-evolutionary baseline.

Here's a picture of the sensors' direction in the robot:
<div align="center">
<img width="350" height="250" alt="image" src="https://github.com/user-attachments/assets/2c75d793-c3a8-4abb-9467-c89eae09cbeb" />
</div>

## Configuration
Common parameters (population size, generations, timing, sensor threshold, genome size, logging paths, etc.) live in:
```
controllers/utils/config.py
```
Adjust these before running if you want different experiment settings.

## Tips and troubleshooting
- If Webots cannot import Python modules, verify the Python command setting and that `requirements.txt` was installed into that interpreter.
- If communication between supervisor and robot fails, try the `simple comms` variants to isolate issues.
- For faster runs, use the `no_logging` variants and reduce rendering quality or run with the fast mode in Webots.

## Citation
If you use this project in academic work, please cite this repository:
```
@software{line_follower_webots,
  title = {Line Follower in Webots - GA Optimized Controller},
  year = {2025},
  url = {https://github.com/malasiaa/line_follower_mujoco}
}
```
