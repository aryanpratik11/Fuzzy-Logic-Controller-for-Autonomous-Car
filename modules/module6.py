import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_obstacle_avoidance_system():
    # Define input variables
    obstacle_distance = ctrl.Antecedent(np.arange(0, 101, 1), 'obstacle_distance')
    obstacle_position = ctrl.Antecedent(np.arange(0, 3, 1), 'obstacle_position')  # 0: Left, 1: Center, 2: Right

    # Define output variables
    steering = ctrl.Consequent(np.arange(-100, 101, 1), 'steering')
    deceleration = ctrl.Consequent(np.arange(0, 11, 1), 'deceleration')

    # Membership functions for obstacle distance
    obstacle_distance['close'] = fuzz.trimf(obstacle_distance.universe, [0, 0, 40])
    obstacle_distance['medium'] = fuzz.trimf(obstacle_distance.universe, [30, 50, 70])
    obstacle_distance['far'] = fuzz.trimf(obstacle_distance.universe, [60, 100, 100])

    # Membership functions for obstacle position
    obstacle_position['left'] = fuzz.trimf(obstacle_position.universe, [0, 0, 1])
    obstacle_position['center'] = fuzz.trimf(obstacle_position.universe, [0.5, 1, 1.5])
    obstacle_position['right'] = fuzz.trimf(obstacle_position.universe, [1, 2, 2])

    # Membership functions for steering
    steering['sharp_left'] = fuzz.trimf(steering.universe, [-100, -100, -60])
    steering['slight_left'] = fuzz.trimf(steering.universe, [-70, -40, -10])
    steering['straight'] = fuzz.trimf(steering.universe, [-20, 0, 20])
    steering['slight_right'] = fuzz.trimf(steering.universe, [10, 40, 70])
    steering['sharp_right'] = fuzz.trimf(steering.universe, [60, 100, 100])

    # Membership functions for deceleration
    deceleration['none'] = fuzz.trimf(deceleration.universe, [0, 0, 2])
    deceleration['moderate'] = fuzz.trimf(deceleration.universe, [2, 5, 8])
    deceleration['high'] = fuzz.trimf(deceleration.universe, [7, 10, 10])

    # Define fuzzy rules
    rule1 = ctrl.Rule(obstacle_distance['close'] & obstacle_position['center'],
                      consequent=[steering['sharp_left'], deceleration['moderate']])
    rule2 = ctrl.Rule(obstacle_distance['close'] & obstacle_position['left'],
                      consequent=[steering['sharp_right'], deceleration['high']])
    rule3 = ctrl.Rule(obstacle_distance['close'] & obstacle_position['right'],
                      consequent=[steering['sharp_left'], deceleration['high']])
    rule4 = ctrl.Rule(obstacle_distance['medium'] & obstacle_position['center'],
                      consequent=[steering['slight_left'], deceleration['moderate']])
    rule5 = ctrl.Rule(obstacle_distance['medium'] & obstacle_position['left'],
                      consequent=[steering['slight_right'], deceleration['moderate']])
    rule6 = ctrl.Rule(obstacle_distance['medium'] & obstacle_position['right'],
                      consequent=[steering['slight_left'], deceleration['moderate']])
    rule7 = ctrl.Rule(obstacle_distance['far'],
                      consequent=[steering['straight'], deceleration['none']])

    # Create control system and simulation
    obstacle_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
    obstacle_simulation = ctrl.ControlSystemSimulation(obstacle_ctrl)

    return obstacle_simulation
