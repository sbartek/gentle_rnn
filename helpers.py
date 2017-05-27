import pandas as pd

def fibonacci_up_to(n):
    if n == 0:
        return [0]
    
    fibonaccis = [0, 1]
    k2 = 0
    k1 = 1
    for i in range(1, n):
        k0 = k1 + k2
        fibonaccis.append(k0)
        k2 = k1
        k1 = k0
    return fibonaccis

def df_fibonacci_up_to(n, shuffle=False):
    x = []
    y = []

    fib = fibonacci_up_to(2 + n + 1)
    for i in range(2, 2 + n):
        x.append([fib[i], fib[i+1]])
        y.append(fib[i+2])
    
    fib_data = pd.DataFrame(x)
    fib_data.columns = ['x1', 'x2']
    fib_data['y'] = y

    if shuffle:
        fib_data = fib_data.sample(frac=1).reset_index(drop=True)
    return fib_data
