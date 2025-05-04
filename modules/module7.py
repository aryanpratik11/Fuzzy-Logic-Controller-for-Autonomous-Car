import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_traffic_signal_response_system():
    # Define fuzzy variables
    signal = ctrl.Antecedent(np.arange(0, 3, 1), 'signal')            # 0: Red, 1: Yellow, 2: Green
    distance = ctrl.Antecedent(np.arange(0, 101, 1), 'distance')      # Distance to signal

    deceleration = ctrl.Consequent(np.arange(0, 11, 1), 'deceleration')  # Deceleration level
    decision = ctrl.Consequent(np.arange(0, 2, 1), 'decision')           # 0: Stop, 1: Go

    # Membership functions for inputs
    signal['red'] = fuzz.trimf(signal.universe, [0, 0, 0])
    signal['yellow'] = fuzz.trimf(signal.universe, [1, 1, 1])
    signal['green'] = fuzz.trimf(signal.universe, [2, 2, 2])

    distance['close'] = fuzz.trimf(distance.universe, [0, 0, 40])
    distance['medium'] = fuzz.trimf(distance.universe, [30, 50, 70])
    distance['far'] = fuzz.trimf(distance.universe, [60, 100, 100])

    # Membership functions for outputs
    deceleration['none'] = fuzz.trimf(deceleration.universe, [0, 0, 3])
    deceleration['moderate'] = fuzz.trimf(deceleration.universe, [2, 5, 7])
    deceleration['high'] = fuzz.trimf(deceleration.universe, [6, 10, 10])

    decision['stop'] = fuzz.trimf(decision.universe, [0, 0, 0])
    decision['go'] = fuzz.trimf(decision.universe, [1, 1, 1])

    # Rule base
    rules = [
        # RED signal rules
        ctrl.Rule(signal['red'] & distance['close'],
                  consequent=[deceleration['high'], decision['stop']]),
        ctrl.Rule(signal['red'] & distance['medium'],
                  consequent=[deceleration['moderate'], decision['stop']]),
        ctrl.Rule(signal['red'] & distance['far'],
                  consequent=[deceleration['moderate'], decision['stop']]),

        # YELLOW signal rules
        ctrl.Rule(signal['yellow'] & distance['close'],
                  consequent=[deceleration['high'], decision['stop']]),
        ctrl.Rule(signal['yellow'] & distance['medium'],
                  consequent=[deceleration['moderate'], decision['stop']]),
        ctrl.Rule(signal['yellow'] & distance['far'],
                  consequent=[deceleration['none'], decision['go']]),

        # GREEN signal rules
        ctrl.Rule(signal['green'] & distance['close'],
                  consequent=[deceleration['none'], decision['go']]),
        ctrl.Rule(signal['green'] & distance['medium'],
                  consequent=[deceleration['none'], decision['go']]),
        ctrl.Rule(signal['green'] & distance['far'],
                  consequent=[deceleration['none'], decision['go']])
    ]

    # Create and return simulation system
    system = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(system)
