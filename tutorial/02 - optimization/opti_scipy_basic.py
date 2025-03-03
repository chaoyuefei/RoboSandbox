from robosandbox.optimization.opti_scipy import Opti


# Initialize the optimization environment
opti = Opti()

# Define variables with initial guesses and bounds
x = opti.variable(init_guess=5, name='x')
y = opti.variable(init_guess=0, name='y')

# Define an objective function: f = x^2 + y^2
f = x**2 + y**2
opti.minimize(f)

# Add constraints: x > 3 and y >= 2
opti.subject_to(x > 3)
opti.subject_to(y >= 2)

# Solve the optimization problem
sol = opti.solve()

# Display the results
if sol.success():
    optimized_x = sol(x)
    optimized_y = sol(y)
    print("Optimization was successful.")
    print(f"Optimal x: {optimized_x}")
    print(f"Optimal y: {optimized_y}")
    print(f"Objective Value: {sol.result.fun}")
else:
    print("Optimization failed:", sol.message())
