import iss_wrapper
import time


iss = iss_wrapper.ISS()
iss.connect()
time.sleep(1)

print(iss.urine_processor_state)
print(iss.clean_water_tank_qty)
print(iss.cabin_temperature)