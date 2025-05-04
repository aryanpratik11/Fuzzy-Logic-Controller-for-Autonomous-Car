import numpy as np

# Import all modules (assuming they're implemented as functions returning simulation objects)
from modules.module1 import create_speed_control_system
from modules.module2 import create_steering_control_system
from modules.module3 import create_pedestrian_response_system
from modules.module4 import create_adaptive_cruise_control_system
from modules.module5 import create_parking_assistance_system
from modules.module6 import create_obstacle_avoidance_system
from modules.module7 import create_traffic_signal_response_system
from modules.module8 import create_road_condition_adaptation_system

def run_speed_control():
    print("\n[1] Speed Control")
    distance = float(input("Distance to car ahead (0–100 m): "))
    speed = float(input("Current speed (0–150 km/h): "))
    road = float(input("Road condition (0: Slippery, 1: Normal, 2: Rough): "))
    sim1 = create_speed_control_system()
    sim1.input['distance'] = distance
    sim1.input['speed'] = speed
    sim1.input['road'] = road
    sim1.compute()
    print(f"> Acceleration: {sim1.output['acceleration']:.2f}, Brake: {sim1.output['brake']:.2f}")

def run_steering_control():
    print("\n[2] Steering Control")
    lane_dev_input = int(input("Lane deviation (0: Left, 1: Center, 2: Right): "))
    curvature_input = int(input("Road curvature (0: Straight, 1: Mild, 2: Sharp): "))
    obstacle_input = int(input("Obstacle position (0: Left, 1: Center, 2: Right): "))
    sim2 = create_steering_control_system()
    sim2.input['lane_dev'] = lane_dev_input
    sim2.input['curvature'] = curvature_input
    sim2.input['obstacle'] = obstacle_input
    sim2.compute()
    print(f"> Steering Angle: {sim2.output['steering']:.2f}")

def run_pedestrian_detection():
    print("\n[3] Pedestrian Detection")
    ped_distance = float(input("Pedestrian distance (0–100 m): "))
    ped_movement = float(input("Pedestrian movement (0: Stationary, 1: Walking, 2: Running): "))
    vehicle_speed = float(input("Vehicle speed (0–150 km/h): "))
    sim3 = create_pedestrian_response_system()
    sim3.input['ped_distance'] = ped_distance
    sim3.input['ped_movement'] = ped_movement
    sim3.input['vehicle_speed'] = vehicle_speed
    sim3.compute()
    print(f"> Deceleration: {sim3.output['deceleration']:.2f}, Warning: {sim3.output['warning_signal']:.2f}")

def run_adaptive_cruise_control():
    print("\n[4] Adaptive Cruise Control")
    distance = float(input("Distance to vehicle ahead (0–100 m): "))
    relative_speed = float(input("Relative speed (0: Slower, 1: Same, 2: Faster): "))
    sim4 = create_adaptive_cruise_control_system()
    sim4.input['distance'] = distance
    sim4.input['relative_speed'] = relative_speed
    sim4.compute()
    print(f"> Throttle: {sim4.output['throttle']:.2f}, Brake: {sim4.output['brake']:.2f}")

def run_parking_assistance():
    print("\n[5] Parking Assistance")
    distance = float(input("Distance to obstacle (0–100 cm): "))
    angle = float(input("Angle to parking space (0–180°): "))
    sim5 = create_parking_assistance_system()
    sim5.input['distance'] = distance
    sim5.input['angle'] = angle
    sim5.compute()
    print(f"> Steering: {sim5.output['steering']:.2f}, Speed: {sim5.output['speed']:.2f}")

def run_obstacle_avoidance():
    print("\n[6] Obstacle Avoidance")
    obstacle_distance = float(input("Obstacle distance (0–100 m): "))
    obstacle_position = float(input("Obstacle position (0: Left, 1: Center, 2: Right): "))
    sim6 = create_obstacle_avoidance_system()
    sim6.input['obstacle_distance'] = obstacle_distance
    sim6.input['obstacle_position'] = obstacle_position
    sim6.compute()
    print(f"> Steering: {sim6.output['steering']:.2f}, Deceleration: {sim6.output['deceleration']:.2f}")

def run_traffic_signal_response():
    print("\n[7] Traffic Signal Response")
    signal = float(input("Traffic signal (0: Red, 1: Yellow, 2: Green): "))
    distance = float(input("Distance to signal (0–100 m): "))
    sim7 = create_traffic_signal_response_system()
    sim7.input['signal'] = signal
    sim7.input['distance'] = distance
    sim7.compute()
    print(f"> Deceleration: {sim7.output['deceleration']:.2f}, Decision (0=Stop,1=Go): {sim7.output['decision']:.2f}")

def run_road_condition_adaptation():
    print("\n[8] Road Condition Adaptation")
    road = float(input("Road surface (0: Dry, 1: Wet, 2: Icy): "))
    visibility = float(input("Visibility (0: Clear, 1: Foggy, 2: Poor): "))
    sim8 = create_road_condition_adaptation_system()
    sim8.input['road'] = road
    sim8.input['visibility'] = visibility
    sim8.compute()
    print(f"> Speed Adjust: {sim8.output['speed']:.2f}, Brake Sensitivity: {sim8.output['brake']:.2f}")

def main():
    while True:
        print("\n===== Fuzzy Logic Controller for Autonomous Car =====")
        print("Select the module you want to test:")
        print("1. Speed Control")
        print("2. Steering Control")
        print("3. Pedestrian Detection")
        print("4. Adaptive Cruise Control")
        print("5. Parking Assistance")
        print("6. Obstacle Avoidance")
        print("7. Traffic Signal Response")
        print("8. Road Condition Adaptation")
        print("9. Exit")

        choice = int(input("Enter your choice (1-9): "))

        if choice == 1:
            run_speed_control()
        elif choice == 2:
            run_steering_control()
        elif choice == 3:
            run_pedestrian_detection()
        elif choice == 4:
            run_adaptive_cruise_control()
        elif choice == 5:
            run_parking_assistance()
        elif choice == 6:
            run_obstacle_avoidance()
        elif choice == 7:
            run_traffic_signal_response()
        elif choice == 8:
            run_road_condition_adaptation()
        elif choice == 9:
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()
