import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_road_condition_adaptation_system():
    # Define inputs
    road = ctrl.Antecedent(np.arange(0, 3, 1), 'road')           # 0: Dry, 1: Wet, 2: Icy
    visibility = ctrl.Antecedent(np.arange(0, 3, 1), 'visibility')  # 0: Clear, 1: Foggy, 2: Poor

    # Define outputs
    speed = ctrl.Consequent(np.arange(0, 3, 1), 'speed')  # 0: Slow Down, 1: Maintain, 2: Speed Up
    brake = ctrl.Consequent(np.arange(0, 3, 1), 'brake')  # 0: Low, 1: Medium, 2: High

    # Membership functions - road
    road['dry'] = fuzz.trimf(road.universe, [0, 0, 0])
    road['wet'] = fuzz.trimf(road.universe, [1, 1, 1])
    road['icy'] = fuzz.trimf(road.universe, [2, 2, 2])

    # Membership functions - visibility
    visibility['clear'] = fuzz.trimf(visibility.universe, [0, 0, 0])
    visibility['foggy'] = fuzz.trimf(visibility.universe, [1, 1, 1])
    visibility['poor'] = fuzz.trimf(visibility.universe, [2, 2, 2])

    # Membership functions - speed
    speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 0])
    speed['maintain'] = fuzz.trimf(speed.universe, [1, 1, 1])
    speed['fast'] = fuzz.trimf(speed.universe, [2, 2, 2])

    # Membership functions - brake
    brake['low'] = fuzz.trimf(brake.universe, [0, 0, 0])
    brake['medium'] = fuzz.trimf(brake.universe, [1, 1, 1])
    brake['high'] = fuzz.trimf(brake.universe, [2, 2, 2])

    # Rule base
    rules = [
        # DRY road
        ctrl.Rule(road['dry'] & visibility['clear'],
                  consequent=[speed['maintain'], brake['low']]),
        ctrl.Rule(road['dry'] & visibility['foggy'],
                  consequent=[speed['slow'], brake['medium']]),
        ctrl.Rule(road['dry'] & visibility['poor'],
                  consequent=[speed['slow'], brake['high']]),

        # WET road
        ctrl.Rule(road['wet'] & visibility['clear'],
                  consequent=[speed['maintain'], brake['medium']]),
        ctrl.Rule(road['wet'] & visibility['foggy'],
                  consequent=[speed['slow'], brake['medium']]),
        ctrl.Rule(road['wet'] & visibility['poor'],
                  consequent=[speed['slow'], brake['high']]),

        # ICY road
        ctrl.Rule(road['icy'] & visibility['clear'],
                  consequent=[speed['slow'], brake['high']]),
        ctrl.Rule(road['icy'] & visibility['foggy'],
                  consequent=[speed['slow'], brake['high']]),
        ctrl.Rule(road['icy'] & visibility['poor'],
                  consequent=[speed['slow'], brake['high']])
    ]

    # Create control system and simulation
    system = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(system)
