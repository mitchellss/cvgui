from utils.utils import *
from constants.constants import *

def test_blazepose_to_pixel_x():
    assert bp2p_x(0.5) == 0.5*PIXEL_SCALE+PIXEL_X_OFFSET
    
def test_blazepose_to_pixel_y():
    assert bp2p_y(0.5) == 0.5*PIXEL_SCALE+PIXEL_Y_OFFSET
    
def test_pixel_to_blazepose_x():
    assert p2bp_x(0.5) == (0.5-PIXEL_X_OFFSET)/PIXEL_SCALE
    
def test_pixel_to_blazepose_y():
    assert p2bp_y(0.5) == (0.5-PIXEL_Y_OFFSET)/PIXEL_SCALE