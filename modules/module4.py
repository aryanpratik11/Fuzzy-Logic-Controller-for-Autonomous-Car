import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_adaptive_cruise_control_system():
    # Define inputs
    distance = ctrl.Antecedent(np.arange(0, 101, 1), 'distance')
    relative_speed = ctrl.Antecedent(np.arange(-50, 51, 1), 'relative_speed')

    # Define outputs
    throttle = ctrl.Consequent(np.arange(0, 11, 1), 'throttle')
    brake = ctrl.Consequent(np.arange(0, 101, 1), 'brake')

    # Distance membership functions
    distance['close'] = fuzz.trimf(distance.universe, [0, 0, 40])
    distance['medium'] = fuzz.trimf(distance.universe, [30, 50, 70])
    distance['far'] = fuzz.trimf(distance.universe, [60, 100, 100])

    # Relative speed membership functions
    relative_speed['slower'] = fuzz.trimf(relative_speed.universe, [-50, -50, 0])
    relative_speed['same'] = fuzz.trimf(relative_speed.universe, [-10, 0, 10])
    relative_speed['faster'] = fuzz.trimf(relative_speed.universe, [0, 50, 50])

    # Throttle membership functions
    throttle['decrease'] = fuzz.trimf(throttle.universe, [0, 0, 3])
    throttle['maintain'] = fuzz.trimf(throttle.universe, [3, 5, 7])
    throttle['increase'] = fuzz.trimf(throttle.universe, [7, 10, 10])

    # Brake membership functions
    brake['low'] = fuzz.trimf(brake.universe, [0, 0, 30])
    brake['medium'] = fuzz.trimf(brake.universe, [20, 50, 80])
    brake['high'] = fuzz.trimf(brake.universe, [70, 100, 100])

    # Define rules
    rule1 = ctrl.Rule(distance['close'] & relative_speed['slower'],
                      consequent=[throttle['decrease'], brake['medium']])
    rule2 = ctrl.Rule(distance['close'] & relative_speed['same'],
                      consequent=[throttle['decrease'], brake['high']])
    rule3 = ctrl.Rule(distance['medium'] & relative_speed['slower'],
                      consequent=[throttle['maintain'], brake['low']])
    rule4 = ctrl.Rule(distance['medium'] & relative_speed['same'],
                      consequent=[throttle['maintain'], brake['low']])
    rule5 = ctrl.Rule(distance['far'] & relative_speed['same'],
                      consequent=[throttle['increase'], brake['low']])
    rule6 = ctrl.Rule(distance['far'] & relative_speed['faster'],
                      consequent=[throttle['increase'], brake['low']])
    rule7 = ctrl.Rule(distance['far'] & relative_speed['slower'],
                      consequent=[throttle['maintain'], brake['low']])

    # Create system and simulation
    acc_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
    acc_simulation = ctrl.ControlSystemSimulation(acc_system)

    return acc_simulation
