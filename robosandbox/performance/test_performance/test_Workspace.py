import robosandbox as rsb
import pytest
from robosandbox.performance.WorkSpace import WorkSpace

def test_add_samples():
    ws = WorkSpace()

    points = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    metric_values = [1, 2, 3]
    metric = 'yoshikawa'
    ws.add_samples(points, metric_values, metric)

    assert ws.df.shape[0] == 3, "The number of samples is not correct."
    assert ws.df['x'].iloc[0] == 1, "The x value is not correct."
    assert ws.df['y'].iloc[0] == 2, "The y value is not correct."
    assert ws.df['z'].iloc[0] == 3, "The z value is not correct."
    assert ws.df['yoshikawa'].iloc[0] == 1, "The yoshikawa value is not correct."

    print(ws.df)

    points = [(10, 11, 12), (13, 14, 15)]
    metric_values = [4, 5]
    metric = 'yoshikawa'
    ws.add_samples(points, metric_values, metric)

    assert ws.df.shape[0] == 5, "The number of samples is not correct."
    assert ws.df['x'].iloc[3] == 10, "The x value is not correct."
    assert ws.df['y'].iloc[3] == 11, "The y value is not correct."
    assert ws.df['z'].iloc[3] == 12, "The z value is not correct."
    assert ws.df['yoshikawa'].iloc[3] == 4, "The invcondition value is not correct."

    print(ws.df)



if __name__ == "__main__":
    test_add_samples()
