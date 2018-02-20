import pandas as pd
import numpy as np

data = np.random.randn(3,3)
a = pd.DataFrame(data, index = ['A', 'B', 'C'], columns = ['a', 'b', 'c'])
b = pd.DataFrame(data, index = ['A', 'B', 'C'], columns = ['d', 'c', 'b'])
temp = pd.Series(None, index = [40, 41, 42, 1, 2, 3])
print("iloc: \n {} \n loc: \n {}".format(temp.iloc[ : 3], temp.loc[1 : 3]))