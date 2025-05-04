import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_parking_assistance_system():
    # Define fuzzy variables
    distance = ctrl.Antecedent(np.arange(0, 101, 1), 'distance')           # Distance to parking object
    angle = ctrl.Antecedent(np.arange(0, 181, 1), 'angle')                 # Entry angle into parking spot

    steering = ctrl.Consequent(np.arange(-100, 101, 1), 'steering')        # Steering angle
    speed = ctrl.Consequent(np.arange(0, 11, 1), 'speed')                  # Speed control

    # Membership functions for inputs
    distance['close'] = fuzz.trimf(distance.universe, [0, 0, 30])
    distance['medium'] = fuzz.trimf(distance.universe, [20, 50, 80])
    distance['far'] = fuzz.trimf(distance.universe, [70, 100, 100])

    angle['acute'] = fuzz.trimf(angle.universe, [0, 0, 60])
    angle['right'] = fuzz.trimf(angle.universe, [60, 90, 120])
    angle['obtuse'] = fuzz.trimf(angle.universe, [120, 180, 180])

    # Membership functions for outputs
    steering['sharp_left'] = fuzz.trimf(steering.universe, [-100, -100, -60])
    steering['slight_left'] = fuzz.trimf(steering.universe, [-70, -40, -10])
    steering['straight'] = fuzz.trimf(steering.universe, [-20, 0, 20])
    steering['slight_right'] = fuzz.trimf(steering.universe, [10, 40, 70])
    steering['sharp_right'] = fuzz.trimf(steering.universe, [60, 100, 100])

    speed['stop'] = fuzz.trimf(speed.universe, [0, 0, 2])
    speed['slow'] = fuzz.trimf(speed.universe, [2, 6, 10])

    # Rule base
    rules = [
        ctrl.Rule(distance['close'] & angle['acute'],
                  consequent=[steering['sharp_right'], speed['slow']]),

        ctrl.Rule(distance['close'] & angle['obtuse'],
                  consequent=[steering['sharp_left'], speed['slow']]),

        ctrl.Rule(distance['medium'] & angle['right'],
                  consequent=[steering['straight'], speed['slow']]),

        ctrl.Rule(distance['far'] & angle['acute'],
                  consequent=[steering['slight_right'], speed['slow']]),

        ctrl.Rule(distance['far'] & angle['obtuse'],
                  consequent=[steering['slight_left'], speed['slow']]),

        ctrl.Rule(distance['close'] & angle['right'],
                  consequent=[steering['straight'], speed['stop']])
    ]

    # Create and return simulation system
    system = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(system)
