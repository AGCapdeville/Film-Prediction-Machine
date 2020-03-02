
'''

The following code example, we apply the gradient descent algorithm to find the minimum of the 
function f(x) = (x^4) - 3(x^3) + 2 with derivative f'(x) = 4(x^3) - 9(x^2).

Solving for 4(x^3) - 9(x^2) = 0 and evaluation of the second derivative at the solutions shows the 
function has a plateau point at 0 and a global minimum at x = 9 / 4.

'''

# line: y = mx + b

def update_weights(m, b, X, Y, learning_rate):
    m_deriv = 0
    b_deriv = 0
    N = len(X)
    for i in range(N):
        # Calculate partial derivatives
        # -2x(y - (mx + b))
        m_deriv += -2*X[i] * (Y[i] - (m*X[i] + b))

        # -2(y - (mx + b))
        b_deriv += -2*(Y[i] - (m*X[i] + b))

    # We subtract because the derivatives point in direction of steepest ascent
    m -= (m_deriv / float(N)) * learning_rate
    b -= (b_deriv / float(N)) * learning_rate

    return m, b

