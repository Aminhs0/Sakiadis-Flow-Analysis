import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_bvp

plt.rcParams['font.family'] = 'STIXGeneral'

# Sakiadis flow function
def sakiadis_flow(eta, f):
    f1, f2, f3 = f
    df1deta = f2
    df2deta = f3
    df3deta = -0.5 * f1 * f3
    return [df1deta, df2deta, df3deta]

# boundary conditions
def bc(ya, yb):
    return np.array([ya[0], ya[1] - 1, yb[1]])

# range of eta
eta = np.linspace(0, 10, 100)

# Initial guess
y_init = np.zeros((3, eta.size))

# Solve the differential equation
res = solve_bvp(sakiadis_flow, bc, eta, y_init)

# sections of x and length of the wal
x_sections = np.array([0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,1])

#  and kinematic viscosity
U_w = 1.0  # Wall velocity
nu = 1.5e-5  # Kinematic viscosity

# Calculate the displacement thickness at each section of x
delta_star = 1.62 * np.sqrt(nu * x_sections / U_w)

# Convert delta_star to millimeters
delta_star_mm = delta_star * 1000

# Plot the derivative of f (f') with respect to eta
plt.figure(figsize=(5, 5))
plt.plot(eta, res.sol(eta)[1], label="f'", color='#527A63')
plt.xlabel('$\eta$', fontsize=12)
plt.ylabel('$u/U_w$', fontsize=12)
plt.legend()
plt.show()

# Plot the displacement thickness
plt.figure(figsize=(5, 5))
plt.scatter(x_sections, delta_star_mm, color='#1D3557')
plt.xlabel('x(m)', fontsize=12)
plt.ylabel('$\delta^*$ (mm)', fontsize=12)
plt.show()

# Calculate the momentum thickness
theta = 0.887 * np.sqrt(nu * x_sections / U_w)

# Convert theta to millimeters
theta_mm = theta * 1000

# Plot the momentum thickness
plt.figure(figsize=(5, 5))
plt.scatter(x_sections, theta_mm, color='#1D3557')
plt.xlabel('x(m)', fontsize=12)
plt.ylabel('$\\theta$ (mm)', fontsize=12)
plt.show()

# Create a figure and axis
fig, ax = plt.subplots(figsize=(5, 5))

# Calculate f' at this section of x for all eta in eta_range
for x in x_sections:
    f_prime = res.sol(eta* x)[1]

    ax.plot(eta, f_prime, label=f'x={x}')

ax.set_xlabel('$\eta$', fontsize=12)
ax.set_ylabel('$u/U_w$', fontsize=12)
ax.legend()

plt.show()


fig, ax = plt.subplots(figsize=(6, 6))

# Calculate the transverse velocity at this section of x for all eta in eta_range
for x in x_sections:
    v_transverse = 0.5 * np.sqrt((nu * U_w) / x) * (eta * res.sol(eta * x)[1] - res.sol(eta * x)[0])

    ax.plot(eta, v_transverse, label=f'x={x}')

ax.set_xlabel('$\eta$', fontsize=12)
ax.set_ylabel('v(m/s)', fontsize=12)
ax.legend()

plt.show()


# Define the density of the fluid
rho = 1.225  # kg/m^3 for air at sea level and 15 degrees Celsius

# Define the sections of x with more sections
x_sections = np.linspace(0.01, 1, 500)

# Calculate the wall shear stress
tau_w = -0.4437 * rho * U_w**2 * np.sqrt(nu / (U_w * x_sections))
tau_w = tau_w / 1000
fig, ax = plt.subplots(figsize=(6, 6))

ax.plot(x_sections, tau_w)

ax.set_xlabel('x(m)', fontsize=12)
ax.set_ylabel('$\\tau_w$ (KPa)', fontsize=12)

plt.show()
