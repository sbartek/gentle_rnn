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

from IPython.display import clear_output, Image, display, HTML
import tensorflow as tf
import numpy as np

def strip_consts(graph_def, max_const_size=32):
    """Strip large constant values from graph_def."""
    strip_def = tf.GraphDef()
    for n0 in graph_def.node:
        n = strip_def.node.add() 
        n.MergeFrom(n0)
        if n.op == 'Const':
            tensor = n.attr['value'].tensor
            size = len(tensor.tensor_content)
            if size > max_const_size:
                tensor.tensor_content = "<stripped %d bytes>"%size
    return strip_def

def show_graph(graph_def, max_const_size=32):
    """Visualize TensorFlow graph."""
    if hasattr(graph_def, 'as_graph_def'):
        graph_def = graph_def.as_graph_def()
    strip_def = strip_consts(graph_def, max_const_size=max_const_size)
    code = """
        <script>
          function load() {{
            document.getElementById("{id}").pbtxt = {data};
          }}
        </script>
        <link rel="import" href="https://tensorboard.appspot.com/tf-graph-basic.build.html" onload=load()>
        <div style="height:600px">
          <tf-graph-basic id="{id}"></tf-graph-basic>
        </div>
    """.format(data=repr(str(strip_def)), id='graph'+str(np.random.rand()))

    iframe = """
        <iframe seamless style="width:1200px;height:620px;border:0" srcdoc="{}"></iframe>
    """.format(code.replace('"', '&quot;'))
    display(HTML(iframe))