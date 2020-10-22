from apply_ltspice_filter import apply_ltspice_filter1
from student_temp import calibrate
import matplotlib.pyplot as pl
import numpy as np
import csv
import sys

class assignment_3_temp:
       
    def __init__(self, zero_deg_v, v_per_deg, temperature):
        self.zero_deg_v = zero_deg_v
        self.v_per_deg = v_per_deg
        self.temperature = temperature
        
    def generate_input_file(self, zero_deg_v, v_per_deg, temperature):
        
        input_data = {}
        input_data['time'] = np.arange(0,2,0.001)
        for i in range(len(input_data['time'])):
            input_data['time'][i] = round(input_data['time'][i],3)
        input_data['amplitude'] = [round(float(zero_deg_v)/1000 + float(temperature)*(float(v_per_deg)/1000),3)]*len(input_data['time'])
        self.save_file('TempSensorPWL.csv', input_data)
        return input_data
        
    def apply_ltspice_filter(self, time, signal_a, circuit_name):
        configuration = {
        }
        dummy, signal_a = apply_ltspice_filter1(
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
        
        input_data = self.generate_input_file(self.zero_deg_v, self.v_per_deg, self.temperature)
        output_data = {}
        output_data['time'] = input_data['time']
        output_data['amplitude']= self.apply_ltspice_filter(input_data["time"], input_data["amplitude"], "E344_A3_temp.asc")
        output_temperature = calibrate(output_data['time'], output_data['amplitude'])
        print('Temperature:', output_temperature, u"\u00b0C")

if __name__ == '__main__':
    
    zero_deg_v = sys.argv[1]
    v_per_deg = sys.argv[2]
    temperature = sys.argv[3]
    run = assignment_3_temp(zero_deg_v, v_per_deg, temperature)
    run.run()
