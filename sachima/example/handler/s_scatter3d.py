"""
s_scatter3d
"""


def run(data_in, params):
    df = data_in[0]
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    return df
