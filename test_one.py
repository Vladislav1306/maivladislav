# content of test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5

def test_passing():
    assert (1, 2, 4) == (1, 2, 3)
