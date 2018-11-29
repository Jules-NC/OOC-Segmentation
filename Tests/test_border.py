import pytest
from Code.Border import *
from Code.Image import *


IMAGE.len_x = 4
IMAGE.len_y = 2

def test_border_1():
    b_1 = Border(0, 0, 1, 1)
    assert b_1.x1 == 0
    assert b_1.y1 == 0
    assert b_1.x2 == 1
    assert b_1.y2 == 1


def test_index():
    b_1 = Border(0, 0, 2, 1)
    leafs = b_1.generate_leafs()
    assert len(leafs) is 6
    assert leafs[0].name == 0
    assert leafs[1].name == 1
    assert leafs[2].name == 2
    assert leafs[3].name == 4
    assert leafs[4].name == 5
    assert leafs[5].name == 6
    
    global IMAGE
    IMAGE.len_x = 3
    IMAGE.len_y = 3
    b_1 = Border(1, 1, 1, 1)
    leafs = b_1.generate_leafs()

    assert len(leafs) is 1
    assert leafs[0].name == 4

    #   Tests boundary does not match the image
    IMAGE.len_x = 2
    IMAGE.len_y = 3942
    with pytest.raises(AssertionError):
        b_1 = Border(-1, 0, 0, 0)
    
    with pytest.raises(AssertionError):
        b_1 = Border(0, 0, 2, 0)

    with pytest.raises(AssertionError):
        b_1 = Border(0, 0, 1, 3942)
        
    with pytest.raises(AssertionError):
        b_1 = Border(10, 0, 1, 0)
        
    with pytest.raises(AssertionError):
        b_1 = Border(0, 900, 1, 2)


def test_int_coords_ibloc_to_iimage():
    global IMAGE   
    IMAGE.len_x = 10
    IMAGE.len_y = 10
    b_1 = Border(2, 7, 5, 9)
    assert b_1.int_coords_ibloc_to_iimage(0) is 72
    assert b_1.int_coords_ibloc_to_iimage(3) is 75 
    assert b_1.int_coords_ibloc_to_iimage(8) is 92

