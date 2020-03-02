
'''

The following code example, we apply the gradient descent algorithm to find the minimum of the 
function f(x) = (x^4) - 3(x^3) + 2 with derivative f'(x) = 4(x^3) - 9(x^2).

Solving for 4(x^3) - 9(x^2) = 0 and evaluation of the second derivative at the solutions shows the 
function has a plateau point at 0 and a global minimum at x = 9 / 4.

'''



next_x = 6  # We start the search at x=6
gamma = 0.01  # Step size multiplier
precision = 0.00001  # Desired precision of result
max_iters = 10000  # Maximum number of iterations

# Derivative function
def df(x):
    return 4 * x ** 3 - 9 * x ** 2


for _i in range(max_iters):
    current_x = next_x
    next_x = current_x - gamma * df(current_x)

    step = next_x - current_x
    if abs(step) <= precision:
        break

print("Minimum at ", next_x)

# The output for the above will be something like
# "Minimum at 2.2499646074278457"