import numpy as np
import matplotlib.pyplot as pyplot

def calibrate(time, amplitude):
        
    ######################################
    # Enter calibration code here:          python assignment_3_temp.py 520 20 34
    ######################################
    
    voltage = np.average(amplitude)
    temperature = int(round(voltage * 2.381859292 + 33.52421399,0))
        
    ######################################
        
    return temperature
