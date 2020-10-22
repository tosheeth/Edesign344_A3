import numpy as np

def calibrate(time, amplitude):
        
    ######################################
    # Enter calibration code here:              python assignment_3_heart.py 1.5 61.05 120 
    ######################################
    times_up = []
    times_down = []

    for i in range(2,len(amplitude)):
        amplitude[i] = 1 if amplitude[i] > 2.5 else 0
        
        times_down.append(time[i] - sum(times_down)) if amplitude[i] < amplitude[i-1] and time[i] > 0.1 else None
        times_up.append(time[i] - sum(times_up)) if amplitude[i] > amplitude[i-1] and time[i] > 0.1 else None

    times_up = times_up[1:]

    times_up.extend(times_down[2:])
    
    avg_time = np.average(times_up) 
    bpm = int(round(avg_time**-1 * 60,0))
    ######################################
        
    return bpm
