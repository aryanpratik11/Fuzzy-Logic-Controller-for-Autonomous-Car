# module1.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_speed_control_system():
    # Define variables
    distance = ctrl.Antecedent(np.arange(0, 101, 1), 'distance')
    speed = ctrl.Antecedent(np.arange(0, 121, 1), 'speed')
    road = ctrl.Antecedent(np.arange(0, 3, 1), 'road')
    acceleration = ctrl.Consequent(np.arange(0, 11, 1), 'acceleration')
    brake = ctrl.Consequent(np.arange(0, 101, 1), 'brake')

    # Membership functions
    distance['close'] = fuzz.trimf(distance.universe, [0, 0, 40])
    distance['medium'] = fuzz.trimf(distance.universe, [20, 50, 80])
    distance['far'] = fuzz.trimf(distance.universe, [60, 100, 100])

    speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 50])
    speed['normal'] = fuzz.trimf(speed.universe, [30, 60, 90])
    speed['fast'] = fuzz.trimf(speed.universe, [70, 120, 120])

    road['slippery'] = fuzz.trimf(road.universe, [0, 0, 0])
    road['normal'] = fuzz.trimf(road.universe, [1, 1, 1])
    road['rough'] = fuzz.trimf(road.universe, [2, 2, 2])

    acceleration['decrease'] = fuzz.trimf(acceleration.universe, [0, 0, 4])
    acceleration['maintain'] = fuzz.trimf(acceleration.universe, [3, 5, 7])
    acceleration['increase'] = fuzz.trimf(acceleration.universe, [6, 10, 10])

    brake['low'] = fuzz.trimf(brake.universe, [0, 0, 40])
    brake['medium'] = fuzz.trimf(brake.universe, [30, 50, 70])
    brake['high'] = fuzz.trimf(brake.universe, [60, 100, 100])

    # Rules
    rule1 = ctrl.Rule(distance['close'] & speed['fast'], 
                      [acceleration['decrease'], brake['high']])
    rule2 = ctrl.Rule(road['slippery'], 
                      [acceleration['decrease'], brake['medium']])

    # Create control system
    system = ctrl.ControlSystem([rule1, rule2])
    simulation = ctrl.ControlSystemSimulation(system)

    return simulation