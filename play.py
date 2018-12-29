import numpy as np
import pandas as pd

data1 = pd.DataFrame({
    'AAA': [1, 2, 3, 4],
    '0': 1.,
    '字段A': pd.Timestamp('20181228'),
    '字段B': '这是一段测试文字测试字段的长度是否能自动调整',
    '字段C': pd.Series(1, index=list(range(4)), dtype='float32'),
    '字段D': np.array([3] * 4, dtype='int32'),
    '字段E': pd.Categorical(["test", "train", "test", "train"]),
    '字段F': '这是一段测试文字测试字段的长度是否能自动调整'
})

data2 = pd.DataFrame({
    'AAA': [4, 3, 2, 1],
    '0': 1.,
    '字段A': pd.Timestamp('20181228'),
    '字段B': '这是一段测试文字测试字段的长度是否能自动调整',
    '字段C': pd.Series(1, index=list(range(4)), dtype='float32'),
    '字段D': np.array([3] * 4, dtype='int32'),
    '字段E': pd.Categorical(["test", "train", "test", "train"]),
    '字段F': '这是一段测试文字测试字段的长度是否能自动调整'
})
print(data1[['AAA']].sort_values('AAA').reset_index(drop=True))
print(data2[['AAA']].sort_values('AAA').reset_index(drop=True))
print(data1[['AAA']].sort_values('AAA').reset_index(drop=True).equals(data2[['AAA']].sort_values('AAA').reset_index(drop=True)))
print()