import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_steering_control_system():
    # Define variables
    lane_dev = ctrl.Antecedent(np.arange(-1, 2, 1), 'lane_dev')      # -1: Left, 0: Center, 1: Right
    curvature = ctrl.Antecedent(np.arange(0, 101, 1), 'curvature')   # 0: Straight, 100: Sharp Curve
    obstacle = ctrl.Antecedent(np.arange(-1, 2, 1), 'obstacle')      # -1: Left, 0: Center, 1: Right
    steering = ctrl.Consequent(np.arange(-100, 101, 1), 'steering')  # -100: Sharp Left, 100: Sharp Right

    # Membership functions
    lane_dev['left'] = fuzz.trimf(lane_dev.universe, [-1, -1, 0])
    lane_dev['center'] = fuzz.trimf(lane_dev.universe, [-1, 0, 1])
    lane_dev['right'] = fuzz.trimf(lane_dev.universe, [0, 1, 1])

    curvature['straight'] = fuzz.trimf(curvature.universe, [0, 0, 30])
    curvature['mild'] = fuzz.trimf(curvature.universe, [20, 50, 80])
    curvature['sharp'] = fuzz.trimf(curvature.universe, [60, 100, 100])

    obstacle['left'] = fuzz.trimf(obstacle.universe, [-1, -1, 0])
    obstacle['center'] = fuzz.trimf(obstacle.universe, [-1, 0, 1])
    obstacle['right'] = fuzz.trimf(obstacle.universe, [0, 1, 1])

    steering['sharp_left'] = fuzz.trimf(steering.universe, [-100, -100, -50])
    steering['slight_left'] = fuzz.trimf(steering.universe, [-80, -40, 0])
    steering['straight'] = fuzz.trimf(steering.universe, [-10, 0, 10])
    steering['slight_right'] = fuzz.trimf(steering.universe, [0, 40, 80])
    steering['sharp_right'] = fuzz.trimf(steering.universe, [50, 100, 100])

    # Rules
    rules = [
        ctrl.Rule(lane_dev['left'] & curvature['straight'], steering['slight_right']),
        ctrl.Rule(lane_dev['right'] & curvature['straight'], steering['slight_left']),
        ctrl.Rule(lane_dev['left'] & curvature['mild'], steering['slight_right']),
        ctrl.Rule(lane_dev['right'] & curvature['mild'], steering['slight_left']),
        ctrl.Rule(lane_dev['left'] & curvature['sharp'], steering['sharp_right']),
        ctrl.Rule(lane_dev['right'] & curvature['sharp'], steering['sharp_left']),
        ctrl.Rule(lane_dev['center'], steering['straight']),

        ctrl.Rule(obstacle['left'], steering['sharp_right']),
        ctrl.Rule(obstacle['right'], steering['sharp_left']),
        ctrl.Rule(obstacle['center'], steering['slight_right']),

        ctrl.Rule(curvature['sharp'] & obstacle['right'], steering['sharp_left']),
        ctrl.Rule(curvature['sharp'] & obstacle['left'], steering['sharp_right']),
        ctrl.Rule(curvature['mild'] & obstacle['right'], steering['slight_left']),
        ctrl.Rule(curvature['mild'] & obstacle['left'], steering['slight_right']),
        ctrl.Rule(curvature['straight'] & obstacle['center'], steering['slight_right']),
    ]

    # Create control system
    system = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(system)

    return simulation
