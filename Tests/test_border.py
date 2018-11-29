from Code.Border import *


def test_border_1():
    b_1 = Border(0, 0, 1, 1)
    assert b_1.x1 == 0
    assert b_1.y1 == 0
    assert b_1.x2 == 1
    assert b_1.y2 == 1
