import gym
import ballbeam_gym
import matplotlib.pyplot as plt

# pass env arguments as kwargs
kwargs = {'timestep': 0.05, 
          'beam_length': 1.0,
          'max_angle': 0.5,
          'init_velocity': 0.5,
          'max_timesteps': 100}

# create env
env = gym.make('BallBeamSetpoint-v0', **kwargs)

# constants for PID calculation
Kp = 3.0
Kd = 1.0
Ki = 0.0

i = 0

ballPosn = []
time = []
beamAngle = []

# simulate 1000 steps
for t in range(100):
    # control theta with a PID controller
    env.render()
    p = env.bb.x - env.setpoint
    i = min(i + p/100, 0.005) if (i + p/100) >= 0 else max(i + p/100, -0.005)
    d = env.bb.v
    theta = Kp*p + Ki*i + Kd*d
    obs, reward, done, info = env.step(theta)

    ballPosn.append(env.bb.x)
    time.append(t)
    beamAngle.append(env.bb.theta)

    if done:
        print("Episode finished after {} timesteps".format(t+1))
        break

fig1, ax1 = plt.subplots( nrows=1, ncols=1 )
ax1.plot(time, ballPosn)
fig1.savefig('1.png')

fig2, ax2 = plt.subplots( nrows=1, ncols=1 )
ax2.plot(time, beamAngle)
fig2.savefig('2.png') 
env.close()