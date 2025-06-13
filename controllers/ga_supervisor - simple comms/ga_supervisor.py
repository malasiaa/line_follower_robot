from controller import Supervisor

TIME_STEP = 32

supervisor = Supervisor()
emitter = supervisor.getDevice("emitter")
emitter.setChannel(3)  # Match E-puck receiver

# Wait 1 second (or 30 steps) then send a message
step_count = 0
while supervisor.step(TIME_STEP) != -1:
    step_count += 1
    if step_count == 30:
        message = "Hello E-puck"
        print(f"Supervisor sending: {message}")
        emitter.send(message.encode('utf-8'))
