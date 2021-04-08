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
Ki = 0.0 # No integral gives better results

# Stores integral value
i = 0

# Lists for for making graphs
ballPosn = []
time = []
beamAngle = []

# simulate 1000 steps
for t in range(100):
    # control theta with a PID controller
    env.render()
    p = env.bb.x - env.setpoint

    # Adding clamping to integral
    i = min(i + p/100, 0.005) if (i + p/1000) >= 0 else max(i + p/100, -0.005)

    d = env.bb.v
    theta = Kp*p + Ki*i + Kd*d
    obs, reward, done, info = env.step(theta)

    print(p, i)

    # Adding values to lists for plotting graphs
    ballPosn.append(env.bb.x)
    time.append(t)
    beamAngle.append(env.bb.theta)

    if done:
        print("Episode finished after {} timesteps".format(t+1))
        break

# Plotting the position v time and angle v time graphs
fig1, ax1 = plt.subplots( nrows=1, ncols=1 )
ax1.plot(time, ballPosn)
fig1.savefig('graphs/PosnVTime3.png')

fig2, ax2 = plt.subplots( nrows=1, ncols=1 )
ax2.plot(time, beamAngle)
fig2.savefig('graphs/AngleVTime3.png') 
env.close()