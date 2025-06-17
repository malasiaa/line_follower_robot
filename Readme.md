


_______________________________________________________________________________________________________________________________ 
# --> Starting by increasing the number of generations

## 1.
#### Best Fitness: 9703.7417
#### Best Genome:
-3.7602,4.8677,5.8634,0.6821,-5.2422,-0.0728,5.8005,-5.8060,1.7716,5.9449,3.3094,3.6316,-3.5267,0.7590,-0.4203,6.2800
###### robot params:
SENSOR_THRESHOLD = 1300, ##black goes around 1000, out of grass 1700 and higher
max_steps = 1500
fitness structure =
if c == 1: ## c center ir sensor
	fitness += 1.0 + speed  ## incentivizing speed (Avg of left and right motors)
elif l == 1 and r == 1: ## left and right ir sensors
	fitness += 0.1  ## Small reward for being close to the line
else:
	fitness -= 20  ## Penalize for being completely off
###### supervisor params:
POP_SIZE = 10
GENOME_SIZE = 16  ## 8 sensor states × 2 motor speeds
GENERATIONS = 20
MUTATION_RATE = 0.1

## 2.
#### Best Fitness: 10347.5901
#### Best Genome:
5.5439,5.7693,5.1683,-2.3317,-5.4720,-4.3279,-6.1456,4.4560,3.8238,6.2267,5.9557,6.2800,0.1432,5.4343,-6.2800,6.2800
###### robot params:
SENSOR_THRESHOLD = (same as previous)
max_steps = 1500
fitness structure =
(same as previous)
###### supervisor params:
POP_SIZE = 10
GENOME_SIZE = 16  ## 8 sensor states × 2 motor speeds
GENERATIONS = 40
MUTATION_RATE = 0.1

## 3.
#### Best Fitness: 10139.8486
#### Best Genome:
3.8551,-4.2471,-0.4473,2.6294,3.7070,0.8972,-3.7699,1.8743,-0.0495,-4.3500,-6.0819,-5.9588,1.3965,6.2800,6.2064,6.1878
###### robot params:
SENSOR_THRESHOLD = (same as previous)
max_steps = 1500
fitness structure =
(same as previous)
###### supervisor params:
POP_SIZE = 10
GENOME_SIZE = 16  ## 8 sensor states × 2 motor speeds
GENERATIONS = 80
MUTATION_RATE = 0.1

## 4.
#### Best Fitness: 10113.3911
#### Best Genome:
-5.5247,-6.2800,4.9428,1.8926,-2.3157,1.1489,-6.2800,6.1163,0.7343,-2.9908,4.9430,-2.9001,-1.6677,6.2800,-3.6620,6.2800
###### robot params:
SENSOR_THRESHOLD = (same as previous)
max_steps = 1500
fitness structure =
(same as previous)
###### supervisor params:
POP_SIZE = 10
GENOME_SIZE = 16  ## 8 sensor states × 2 motor speeds
GENERATIONS = 160
MUTATION_RATE = 0.1


# --> Conclusion: It might seem that an increase in the number of generations might lead to a better fitness
_______________________________________________________________________________________________________________________________ 

# --> Increasing population size 

## 5.
#### Best Fitness: 10355.8109
#### Best Genome:
1.9684,0.2218,2.9285,0.8471,-5.6371,-1.9636,-3.2098,1.0700,0.5407,4.6803,1.0283,-1.9612,0.1268,-6.0726,-6.2800,-6.2800
###### robot params:
SENSOR_THRESHOLD = (same as previous)
max_steps = 1500
fitness structure =
(same as previous)
###### supervisor params:
POP_SIZE = 30
GENOME_SIZE = 16  ## 8 sensor states × 2 motor speeds
GENERATIONS = 40
MUTATION_RATE = 0.1

# --> Conclusion: Increasing pop size leads to a marginal increase in fitness (from 10347 in atempt 2 to 10355 in atempt 5). It doesn't seem to produce any significant effect.
	
_______________________________________________________________________________________________________________________________ 

# --> Increasing number of learning steps

## 6.
#### Best Fitness: 23974.3039
#### Best Genome:
-0.0788,-3.3234,-3.7910,-1.1608,5.2272,-1.4751,-4.0439,1.0347,-1.6484,2.8386,5.1977,3.4333,0.2008,-5.7195,-6.2800,6.2800
###### robot params:
SENSOR_THRESHOLD = (same as previous)
max_steps = 3500
fitness structure =
(same as previous)
###### supervisor params:
POP_SIZE = 10
GENOME_SIZE = 16  ## 8 sensor states × 2 motor speeds
GENERATIONS = 40
MUTATION_RATE = 0.1


## 7.
#### Best Fitness: 33362.6994
#### Best Genome:
4.6032,5.3203,5.5053,0.3527,-3.8286,5.2055,-6.2800,-6.2345,-5.8447,1.2520,-0.7457,-6.2800,2.5946,4.3623,-1.6984,-6.2800
###### robot params:
SENSOR_THRESHOLD = (same as previous)
max_steps = 5000
fitness structure = (same as previous)

###### supervisor params:
POP_SIZE = 10
GENOME_SIZE = 16  ## 8 sensor states × 2 motor speeds
GENERATIONS = 40
MUTATION_RATE = 0.1

# --> Conclusion: Increasing the number learning steps, seems to have a SIGNIFICANT positive inpact in fitness.
_______________________________________________________________________________________________________________________________ 

# --> Increasing mutation rate to 20%

## 8.
#### Best Fitness: 32219.1186
#### Best Genome:
-1.4388,5.1289,1.0549,-4.2955,5.7401,-4.3173,-6.2800,-5.6834,0.5890,-3.8264,0.9011,-4.7695,5.4829,-2.5988,1.0178,-6.2800
###### robot params:
SENSOR_THRESHOLD = (same as previous)
max_steps = 5000
fitness structure =
(same as previous)
###### supervisor params:
POP_SIZE = 10
GENOME_SIZE = 16  ## 8 sensor states × 2 motor speeds
GENERATIONS = 40
MUTATION_RATE = 0.2

# --> Conclusion: Seems to produce nefareous effect in fitness.

_______________________________________________________________________________________________________________________________ 

# --> Based on learnt: Increasing number of steps and generations

## 9.
#### Best Fitness: 34463.7515
#### Best Genome:
4.6980,4.7135,0.7278,-4.5892,-4.3056,6.0608,6.2800,4.4991,0.2219,-4.1518,5.0405,-2.0183,0.1238,-5.5107,-6.2800,-6.2800
###### robot params:
SENSOR_THRESHOLD = (same as previous)
max_steps = 5000
fitness structure =
(same as previous)
###### supervisor params:
POP_SIZE = 10
GENOME_SIZE = 16  ## 8 sensor states × 2 motor speeds
GENERATIONS = 80
MUTATION_RATE = 0.2