import iss_wrapper
import time



iss = iss_wrapper.ISS()
iss.connect()
time.sleep(1) # this is required to allow time to connect


if iss.is_connected:
    try:
        while True:
            print(f"GMT Time: {iss.gmt_time}")

            print(f"Cabin Pressure: {iss.cabin_pressure}")

            print(f"Cabin Temperature: {iss.cabin_temperature}")

            print(f"Solar Beta Angle: {iss.solar_beta_angle}")

            print(f"CMGs Online: {iss.cmgs_online_count}")

            print(f"CMG 1 Status: {iss.cmg_1_online}")

            print(f"Attitude Roll Error: {iss.attitude_roll_error}")

            print(f"X Position: {iss.state_vector_x_pos} meters")

            print(f"Y Position: {iss.state_vector_y_pos} meters")

            print(f"Z Position: {iss.state_vector_z_pos} meters")

            print(f"Lab O2 Pressure: {iss.lab_ppo2}")

            print(f"Lab N2 Pressure: {iss.lab_ppn2}")

            print(f"Lab CO2 Pressure: {iss.lab_ppco2}")

            time.sleep(5)  # Update every 5 seconds
    except KeyboardInterrupt:
        print("Stopping...")
else:
    print("Failed to connect")