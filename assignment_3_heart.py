from apply_ltspice_filter import apply_ltspice_filter2
from student_heart import calibrate
import matplotlib.pyplot as pl
import numpy as np
import csv
import sys
import math
import random

class assignment_3_heart:
       
    def __init__(self, v_dc, v_amplitude, bpm):
        self.v_dc = v_dc
        self.v_amplitude = float(v_amplitude)/5.55
        self.bpm = bpm
        
    def generate_input_file(self, v_dc, v_amplitude, bpm):
        input_data = {}
        nominal = 1
        amplitude = (float(v_amplitude)*nominal)/1000 
        dcmid = float(v_dc)
        input_data['time'] = []
        input_data['amplitude'] = []
        #for number in range (20*250):
        #    timestep = number*4/1000
        for timestep in np.arange(0,6,0.001):
            fundamentalHeart = float(bpm)/60
            heart = amplitude * ( 4 * math.sin(2 * math.pi * fundamentalHeart * timestep) + 2 * math.sin(2 * math.pi * (fundamentalHeart*2) *timestep) + 1 * math.sin(2 * math.pi * (fundamentalHeart*3) * timestep)) 
            noise = amplitude * (2* math.sin(0.25*timestep* 2 * math.pi) + 2 * math.sin(20*timestep*2*math.pi) + 0.4 *math.sin(50*timestep*2*math.pi) + 0.8*math.sin(350*timestep*2*math.pi))
            noise = noise + amplitude * 4 * (random.random()-0.5)     
            input_data['time'].append(timestep)
            input_data['amplitude'].append(heart+noise+dcmid)   
        self.save_file('HeartSensorPWL.csv', input_data)
        return input_data

    def apply_ltspice_filter(self, time, signal_a, circuit_name):
        configuration = {
        }
        dummy, signal_a = apply_ltspice_filter2(
                circuit_name,
                time, signal_a,
                params=configuration
                )
        return list(signal_a)

    def save_file(self, file_string, dict_data):
        zd = zip(*dict_data.values())
        with open(file_string, 'w') as file:
            writer = csv.writer(file, delimiter=',', lineterminator = '\n')
            #writer.writerow(dict_data.keys())
            writer.writerows(zd)
        
    def run(self):
        
        input_data = self.generate_input_file(self.v_dc, self.v_amplitude, self.bpm)
        output_data = {}
        output_data['time'] = input_data['time']
        output_data['amplitude'] = self.apply_ltspice_filter(input_data["time"], input_data["amplitude"], "E344_A3_heart.asc")
        #print(output_data['amplitude'])
        output_heartbeat = calibrate(output_data['time'], output_data['amplitude'])
        print('Heartbeat:', output_heartbeat, "bpm")

if __name__ == '__main__':
    
    v_dc = sys.argv[1]
    v_amplitude = sys.argv[2]
    bpm = sys.argv[3]
    run = assignment_3_heart(v_dc, v_amplitude, bpm)
    run.run()
