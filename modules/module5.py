import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_parking_assistance_system():
    # Define inputs
    distance = ctrl.Antecedent(np.arange(0, 101, 1), 'distance')
    angle = ctrl.Antecedent(np.arange(0, 181, 1), 'angle')

    # Define outputs
    steering = ctrl.Consequent(np.arange(-100, 101, 1), 'steering')
    speed = ctrl.Consequent(np.arange(0, 11, 1), 'speed')

    # Membership functions - Distance
    distance['close'] = fuzz.trimf(distance.universe, [0, 0, 30])
    distance['medium'] = fuzz.trimf(distance.universe, [20, 50, 80])
    distance['far'] = fuzz.trimf(distance.universe, [70, 100, 100])

    # Membership functions - Angle
    angle['acute'] = fuzz.trimf(angle.universe, [0, 0, 60])
    angle['right'] = fuzz.trimf(angle.universe, [60, 90, 120])
    angle['obtuse'] = fuzz.trimf(angle.universe, [120, 180, 180])

    # Membership functions - Steering
    steering['sharp_left'] = fuzz.trimf(steering.universe, [-100, -100, -60])
    steering['slight_left'] = fuzz.trimf(steering.universe, [-70, -40, -10])
    steering['straight'] = fuzz.trimf(steering.universe, [-20, 0, 20])
    steering['slight_right'] = fuzz.trimf(steering.universe, [10, 40, 70])
    steering['sharp_right'] = fuzz.trimf(steering.universe, [60, 100, 100])

    # Membership functions - Speed
    speed['stop'] = fuzz.trimf(speed.universe, [0, 0, 2])
    speed['slow'] = fuzz.trimf(speed.universe, [2, 6, 10])

    # Define rules
    rule1 = ctrl.Rule(distance['close'] & angle['acute'],
                      consequent=[steering['sharp_right'], speed['slow']])
    rule2 = ctrl.Rule(distance['close'] & angle['obtuse'],
                      consequent=[steering['sharp_left'], speed['slow']])
    rule3 = ctrl.Rule(distance['medium'] & angle['right'],
                      consequent=[steering['straight'], speed['slow']])
    rule4 = ctrl.Rule(distance['far'] & angle['acute'],
                      consequent=[steering['slight_right'], speed['slow']])
    rule5 = ctrl.Rule(distance['far'] & angle['obtuse'],
                      consequent=[steering['slight_left'], speed['slow']])
    rule6 = ctrl.Rule(angle['right'] & distance['close'],
                      consequent=[steering['straight'], speed['stop']])

    # Create control system
    parking_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
    simulation = ctrl.ControlSystemSimulation(parking_ctrl)

    return simulation
