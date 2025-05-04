import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_pedestrian_response_system():
    # Define fuzzy variables
    ped_distance = ctrl.Antecedent(np.arange(0, 101, 1), 'ped_distance')        # Distance to pedestrian
    ped_movement = ctrl.Antecedent(np.arange(0, 3, 1), 'ped_movement')          # 0: Stationary, 1: Walking, 2: Running
    vehicle_speed = ctrl.Antecedent(np.arange(0, 121, 1), 'vehicle_speed')      # Vehicle speed

    deceleration = ctrl.Consequent(np.arange(0, 11, 1), 'deceleration')         # 0: None, 10: Full
    warning_signal = ctrl.Consequent(np.arange(0, 101, 1), 'warning_signal')    # 0: Off, 100: High alert

    # Membership functions for inputs
    ped_distance['close'] = fuzz.trimf(ped_distance.universe, [0, 0, 40])
    ped_distance['medium'] = fuzz.trimf(ped_distance.universe, [30, 60, 90])
    ped_distance['far'] = fuzz.trimf(ped_distance.universe, [80, 100, 100])

    ped_movement['stationary'] = fuzz.trimf(ped_movement.universe, [0, 0, 0])
    ped_movement['walking'] = fuzz.trimf(ped_movement.universe, [1, 1, 1])
    ped_movement['running'] = fuzz.trimf(ped_movement.universe, [2, 2, 2])

    vehicle_speed['slow'] = fuzz.trimf(vehicle_speed.universe, [0, 0, 50])
    vehicle_speed['normal'] = fuzz.trimf(vehicle_speed.universe, [30, 60, 90])
    vehicle_speed['fast'] = fuzz.trimf(vehicle_speed.universe, [70, 120, 120])

    # Membership functions for outputs
    deceleration['none'] = fuzz.trimf(deceleration.universe, [0, 0, 2])
    deceleration['low'] = fuzz.trimf(deceleration.universe, [1, 2, 4])
    deceleration['moderate'] = fuzz.trimf(deceleration.universe, [3, 5, 7])
    deceleration['high'] = fuzz.trimf(deceleration.universe, [6, 10, 10])

    warning_signal['off'] = fuzz.trimf(warning_signal.universe, [0, 0, 10])
    warning_signal['low'] = fuzz.trimf(warning_signal.universe, [10, 30, 50])
    warning_signal['medium'] = fuzz.trimf(warning_signal.universe, [40, 60, 80])
    warning_signal['high'] = fuzz.trimf(warning_signal.universe, [70, 100, 100])

    # Rule base
    rules = [
        ctrl.Rule(ped_distance['close'] & ped_movement['walking'],
                  consequent=[deceleration['moderate'], warning_signal['high']]),

        ctrl.Rule(ped_distance['close'] & ped_movement['running'],
                  consequent=[deceleration['high'], warning_signal['high']]),

        ctrl.Rule(ped_distance['close'] & ped_movement['stationary'],
                  consequent=[deceleration['low'], warning_signal['low']]),

        ctrl.Rule(ped_distance['medium'] & ped_movement['walking'] & vehicle_speed['fast'],
                  consequent=[deceleration['moderate'], warning_signal['low']]),

        ctrl.Rule(ped_distance['medium'] & ped_movement['walking'] & vehicle_speed['slow'],
                  consequent=[deceleration['low'], warning_signal['low']]),

        ctrl.Rule(ped_distance['medium'] & ped_movement['running'] & vehicle_speed['fast'],
                  consequent=[deceleration['high'], warning_signal['high']]),

        ctrl.Rule(ped_distance['medium'] & ped_movement['stationary'],
                  consequent=[deceleration['none'], warning_signal['off']]),

        ctrl.Rule(ped_distance['far'] & ped_movement['walking'] & vehicle_speed['fast'],
                  consequent=[deceleration['moderate'], warning_signal['low']]),

        ctrl.Rule(ped_distance['far'] & ped_movement['running'] & vehicle_speed['fast'],
                  consequent=[deceleration['moderate'], warning_signal['medium']]),

        ctrl.Rule(ped_distance['far'] & ped_movement['stationary'],
                  consequent=[deceleration['none'], warning_signal['off']])
    ]

    # Create and return simulation system
    system = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(system)
