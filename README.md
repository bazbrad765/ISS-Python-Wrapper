# ISS Python Wrapper

A Python wrapper for accessing live telemetry data from the International Space Station (ISS) via NASA's Lightstreamer feed.

## Installation

```bash
pip install lightstreamer-client-lib
```

## Example Usage

# Initialize and connect
iss = ISS()

iss.connect()

time.sleep(2) - this is needed toi allow time to connect

# Get basic telemetry

print(f"GMT Time: {iss.gmt_time}")

print(f"Cabin Pressure: {iss.cabin_pressure}")

print(f"Cabin Temperature: {iss.cabin_temperature}")

print(f"Solar Beta Angle: {iss.solar_beta_angle}")

# Get attitude information

print(f"CMGs Online: {iss.cmgs_online_count}")

print(f"CMG 1 Status: {iss.cmg_1_online}")

print(f"Attitude Roll Error: {iss.attitude_roll_error}")


# Get position data

print(f"X Position: {iss.state_vector_x_pos} meters")

print(f"Y Position: {iss.state_vector_y_pos} meters")

print(f"Z Position: {iss.state_vector_z_pos} meters")


# Get environmental data

print(f"Lab O2 Pressure: {iss.lab_ppo2}")

print(f"Lab N2 Pressure: {iss.lab_ppn2}")

print(f"Lab CO2 Pressure: {iss.lab_ppco2}")


**Total Properties Available: 281**

## Notes

- All properties return `Optional` types - they may return `None` if data is not available
- Status properties return human-readable strings (e.g., "OPEN", "CLOSED") instead of numeric codes
- The wrapper automatically connects to NASA's live telemetry stream
- Data updates in real-time as the ISS transmits new telemetry

## Available Properties


### Control Moment Gyroscope (CMG) - Attitude Control
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.cmg_1_online` | `Optional[str]` | Control Moment Gyroscope 1 Online Status |
| `iss.cmg_2_online` | `Optional[str]` | Control Moment Gyroscope 2 Online Status |
| `iss.cmg_3_online` | `Optional[str]` | Control Moment Gyroscope 3 Online Status |
| `iss.cmg_4_online` | `Optional[str]` | Control Moment Gyroscope 4 Online Status |
| `iss.cmgs_online_count` | `Optional[int]` | Control Moment Gyroscopes Online Count |
| `iss.cmg_control_torque_roll` | `Optional[float]` | Control Moment Gyroscope Control Torque Roll |
| `iss.cmg_control_torque_pitch` | `Optional[float]` | Control Moment Gyroscope Control Torque Pitch |
| `iss.cmg_control_torque_yaw` | `Optional[float]` | Control Moment Gyroscope Control Torque Yaw |
| `iss.cmg_active_momentum` | `Optional[float]` | Control Moment Gyroscope Active Momentum |
| `iss.cmg_momentum_percentage` | `Optional[float]` | Control Moment Gyroscope Momentum Percentage |
| `iss.desaturation_request` | `Optional[str]` | CMG Desaturation Request Status |
| `iss.gnc_mode` | `Optional[str]` | Guidance Navigation and Control Mode |
| `iss.attitude_source` | `Optional[str]` | Attitude Determination Source |
| `iss.rate_source` | `Optional[str]` | Angular Rate Source |
| `iss.state_vector_source` | `Optional[str]` | State Vector Source |
| `iss.attitude_controller_type` | `Optional[str]` | Attitude Controller Type |
| `iss.attitude_control_reference_frame` | `Optional[str]` | Attitude Control Reference Frame |

### Attitude Quaternions
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.lvlh_quaternion_0` | `Optional[float]` | Local Vertical Local Horizontal Quaternion 0 |
| `iss.lvlh_quaternion_1` | `Optional[float]` | Local Vertical Local Horizontal Quaternion 1 |
| `iss.lvlh_quaternion_2` | `Optional[float]` | Local Vertical Local Horizontal Quaternion 2 |
| `iss.lvlh_quaternion_3` | `Optional[float]` | Local Vertical Local Horizontal Quaternion 3 |
| `iss.attitude_roll_error` | `Optional[float]` | Attitude Roll Error (degrees) |
| `iss.attitude_pitch_error` | `Optional[float]` | Attitude Pitch Error (degrees) |
| `iss.attitude_yaw_error` | `Optional[float]` | Attitude Yaw Error (degrees) |
| `iss.commanded_quaternion_0` | `Optional[float]` | Commanded Attitude Quaternion 0 |
| `iss.commanded_quaternion_1` | `Optional[float]` | Commanded Attitude Quaternion 1 |
| `iss.commanded_quaternion_2` | `Optional[float]` | Commanded Attitude Quaternion 2 |
| `iss.commanded_quaternion_3` | `Optional[float]` | Commanded Attitude Quaternion 3 |

### Position and Velocity
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.state_vector_x_pos` | `Optional[float]` | State Vector X Position (meters) |
| `iss.state_vector_y_pos` | `Optional[float]` | State Vector Y Position (meters) |
| `iss.state_vector_z_pos` | `Optional[float]` | State Vector Z Position (meters) |
| `iss.state_vector_x_vel` | `Optional[float]` | State Vector X Velocity (m/s) |
| `iss.state_vector_y_vel` | `Optional[float]` | State Vector Y Velocity (m/s) |
| `iss.state_vector_z_vel` | `Optional[float]` | State Vector Z Velocity (m/s) |

### Station Status
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.cmg_capacity` | `Optional[float]` | Control Moment Gyroscope Capacity |
| `iss.iss_total_mass` | `Optional[float]` | International Space Station Total Mass (kg) |
| `iss.solar_beta_angle` | `Optional[float]` | Solar Beta Angle (degrees) |
| `iss.loac_cmg_alarm` | `Optional[str]` | Loss of Attitude Control CMG Alarm |
| `iss.loac_iss_alarm` | `Optional[str]` | Loss of Attitude Control ISS Alarm |
| `iss.gps_1_status` | `Optional[str]` | Global Positioning System 1 Status |
| `iss.gps_2_status` | `Optional[str]` | Global Positioning System 2 Status |

### CMG Temperatures
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.cmg_1_spin_motor_temp` | `Optional[float]` | Control Moment Gyroscope 1 Spin Motor Temperature |
| `iss.cmg_2_spin_motor_temp` | `Optional[float]` | Control Moment Gyroscope 2 Spin Motor Temperature |
| `iss.cmg_3_spin_motor_temp` | `Optional[float]` | Control Moment Gyroscope 3 Spin Motor Temperature |
| `iss.cmg_4_spin_motor_temp` | `Optional[float]` | Control Moment Gyroscope 4 Spin Motor Temperature |
| `iss.cmg_1_hall_resolver_temp` | `Optional[float]` | Control Moment Gyroscope 1 Hall Resolver Temperature |
| `iss.cmg_2_hall_resolver_temp` | `Optional[float]` | Control Moment Gyroscope 2 Hall Resolver Temperature |
| `iss.cmg_3_hall_resolver_temp` | `Optional[float]` | Control Moment Gyroscope 3 Hall Resolver Temperature |
| `iss.cmg_4_hall_resolver_temp` | `Optional[float]` | Control Moment Gyroscope 4 Hall Resolver Temperature |

### Environmental Control and Life Support
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.lab_ppo2` | `Optional[float]` | Lab Partial Pressure Oxygen |
| `iss.lab_ppn2` | `Optional[float]` | Lab Partial Pressure Nitrogen |
| `iss.lab_ppco2` | `Optional[float]` | Lab Partial Pressure Carbon Dioxide |
| `iss.lab_coolant_lt` | `Optional[float]` | Lab Coolant Loop Temperature (Low) |
| `iss.lab_coolant_mt` | `Optional[float]` | Lab Coolant Loop Temperature (Medium) |
| `iss.cabin_temperature` | `Optional[float]` | Cabin Temperature |
| `iss.cabin_pressure` | `Optional[str]` | Cabin Atmospheric Pressure |
| `iss.lab_avionics_temp` | `Optional[float]` | Lab Avionics Temperature |
| `iss.lab_air_cooling_temp` | `Optional[float]` | Lab Air Cooling Temperature |
| `iss.vacuum_resource_valve` | `Optional[str]` | Vacuum Resource Valve Position |
| `iss.vacuum_exhaust_valve` | `Optional[str]` | Vacuum Exhaust Valve Position |
| `iss.lab_port_ac_state` | `Optional[str]` | Lab Port Air Conditioning State |
| `iss.lab_starboard_ac_state` | `Optional[str]` | Lab Starboard Air Conditioning State |

### Multiplexer/Demultiplexer Status
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.cc_mdm_1_status` | `Optional[str]` | Command and Control Multiplexer/Demultiplexer 1 Status |
| `iss.cc_mdm_2_status` | `Optional[str]` | Command and Control Multiplexer/Demultiplexer 2 Status |
| `iss.cc_mdm_3_status` | `Optional[str]` | Command and Control Multiplexer/Demultiplexer 3 Status |
| `iss.icz_mdm_1_status` | `Optional[str]` | Internal Control Zone Multiplexer/Demultiplexer 1 Status |
| `iss.icz_mdm_2_status` | `Optional[str]` | Internal Control Zone Multiplexer/Demultiplexer 2 Status |
| `iss.pl_mdm_1_status` | `Optional[str]` | Payload Multiplexer/Demultiplexer 1 Status |
| `iss.pl_mdm_2_status` | `Optional[str]` | Payload Multiplexer/Demultiplexer 2 Status |
| `iss.gnc_mdm_1_status` | `Optional[str]` | Guidance Navigation Control Multiplexer/Demultiplexer 1 Status |
| `iss.gnc_mdm_2_status` | `Optional[str]` | Guidance Navigation Control Multiplexer/Demultiplexer 2 Status |
| `iss.pmcu_1_mdm_status` | `Optional[str]` | Power Management Control Unit 1 Multiplexer/Demultiplexer Status |
| `iss.pmcu_2_mdm_status` | `Optional[str]` | Power Management Control Unit 2 Multiplexer/Demultiplexer Status |
| `iss.lab_mdm_1_status` | `Optional[str]` | Lab Multiplexer/Demultiplexer 1 Status |
| `iss.lab_mdm_2_status` | `Optional[str]` | Lab Multiplexer/Demultiplexer 2 Status |
| `iss.lab_mdm_3_status` | `Optional[str]` | Lab Multiplexer/Demultiplexer 3 Status |
| `iss.pmm_power_status` | `Optional[str]` | Permanent Multipurpose Module Power Status |

### Mission Control and Commands
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.attitude_maneuver_in_progress` | `Optional[bool]` | Attitude Maneuver In Progress Status |
| `iss.standard_command_counter` | `Optional[int]` | Standard Command Counter |
| `iss.data_load_command_counter` | `Optional[int]` | Data Load Command Counter |
| `iss.cc_mdm_time_coarse` | `Optional[int]` | Command and Control MDM Time Coarse |
| `iss.cc_mdm_time_fine` | `Optional[int]` | Command and Control MDM Time Fine |
| `iss.station_mode` | `Optional[str]` | Space Station Operating Mode |
| `iss.laptops_active` | `Optional[int]` | Number of Active Laptops |

### Communications
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.ku_video_ch1_activity` | `Optional[str]` | Ku-band Video Channel 1 Activity |
| `iss.ku_video_ch2_activity` | `Optional[str]` | Ku-band Video Channel 2 Activity |
| `iss.ku_video_ch3_activity` | `Optional[str]` | Ku-band Video Channel 3 Activity |
| `iss.ku_video_ch4_activity` | `Optional[str]` | Ku-band Video Channel 4 Activity |
| `iss.sband_active_string` | `Optional[str]` | S-band Active Communication String |
| `iss.iac_1_status` | `Optional[str]` | Internal Audio Controller 1 Status |
| `iss.iac_2_status` | `Optional[str]` | Internal Audio Controller 2 Status |
| `iss.video_downlink_1` | `Optional[str]` | Video Downlink Channel 1 |
| `iss.video_downlink_2` | `Optional[str]` | Video Downlink Channel 2 |
| `iss.video_downlink_3` | `Optional[str]` | Video Downlink Channel 3 |
| `iss.video_downlink_4` | `Optional[str]` | Video Downlink Channel 4 |
| `iss.uhf_1_power` | `Optional[str]` | Ultra High Frequency Radio 1 Power Status |
| `iss.uhf_2_power` | `Optional[str]` | Ultra High Frequency Radio 2 Power Status |
| `iss.uhf_frame_sync` | `Optional[str]` | Ultra High Frequency Frame Synchronization |

### CMG Performance
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.cmg_1_vibration` | `Optional[float]` | Control Moment Gyroscope 1 Vibration Level |
| `iss.cmg_2_vibration` | `Optional[float]` | Control Moment Gyroscope 2 Vibration Level |
| `iss.cmg_3_vibration` | `Optional[float]` | Control Moment Gyroscope 3 Vibration Level |
| `iss.cmg_4_vibration` | `Optional[float]` | Control Moment Gyroscope 4 Vibration Level |
| `iss.cmg_1_spin_motor_current` | `Optional[float]` | Control Moment Gyroscope 1 Spin Motor Current |
| `iss.cmg_2_spin_motor_current` | `Optional[float]` | Control Moment Gyroscope 2 Spin Motor Current |
| `iss.cmg_3_spin_motor_current` | `Optional[float]` | Control Moment Gyroscope 3 Spin Motor Current |
| `iss.cmg_4_spin_motor_current` | `Optional[float]` | Control Moment Gyroscope 4 Spin Motor Current |
| `iss.cmg_1_wheel_speed` | `Optional[float]` | Control Moment Gyroscope 1 Wheel Speed |
| `iss.cmg_2_wheel_speed` | `Optional[float]` | Control Moment Gyroscope 2 Wheel Speed |
| `iss.cmg_3_wheel_speed` | `Optional[float]` | Control Moment Gyroscope 3 Wheel Speed |
| `iss.cmg_4_wheel_speed` | `Optional[float]` | Control Moment Gyroscope 4 Wheel Speed |
| `iss.ku_transmit` | `Optional[str]` | Ku-band Transmit Status |
| `iss.ku_sgant_elevation` | `Optional[float]` | Ku-band Space-to-Ground Antenna Elevation |
| `iss.ku_sgant_cross_elevation` | `Optional[float]` | Ku-band Space-to-Ground Antenna Cross Elevation |

### Node Systems
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.airlock_mdm_status` | `Optional[str]` | Airlock Multiplexer/Demultiplexer Status |
| `iss.node1_mdm_1_status` | `Optional[str]` | Node 1 Multiplexer/Demultiplexer 1 Status |
| `iss.node1_mdm_2_status` | `Optional[str]` | Node 1 Multiplexer/Demultiplexer 2 Status |
| `iss.node2_mdm_2_status` | `Optional[str]` | Node 2 Multiplexer/Demultiplexer 2 Status |
| `iss.node2_mdm_1_status` | `Optional[str]` | Node 2 Multiplexer/Demultiplexer 1 Status |
| `iss.node3_hcz_mdm_2_status` | `Optional[str]` | Node 3 Health and Status Zone Multiplexer/Demultiplexer 2 Status |
| `iss.node3_mdm_2_status` | `Optional[str]` | Node 3 Multiplexer/Demultiplexer 2 Status |
| `iss.node3_hcz_mdm_1_status` | `Optional[str]` | Node 3 Health and Status Zone Multiplexer/Demultiplexer 1 Status |
| `iss.node3_mdm_1_status` | `Optional[str]` | Node 3 Multiplexer/Demultiplexer 1 Status |

### Truss Systems
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.p1_mdm_1_status` | `Optional[str]` | P1 Truss Multiplexer/Demultiplexer 1 Status |
| `iss.p1_str_mdm_status` | `Optional[str]` | P1 Starboard Truss Multiplexer/Demultiplexer Status |
| `iss.p1_mdm_2_status` | `Optional[str]` | P1 Truss Multiplexer/Demultiplexer 2 Status |
| `iss.p3_mdm_1_status` | `Optional[str]` | P3 Truss Multiplexer/Demultiplexer 1 Status |
| `iss.p3_mdm_2_status` | `Optional[str]` | P3 Truss Multiplexer/Demultiplexer 2 Status |
| `iss.s0_ecz_mdm_1_status` | `Optional[str]` | S0 External Control Zone Multiplexer/Demultiplexer 1 Status |
| `iss.s0_mdm_1_status` | `Optional[str]` | S0 Truss Multiplexer/Demultiplexer 1 Status |
| `iss.s0_ecz_mdm_2_status` | `Optional[str]` | S0 External Control Zone Multiplexer/Demultiplexer 2 Status |
| `iss.s0_mdm_2_status` | `Optional[str]` | S0 Truss Multiplexer/Demultiplexer 2 Status |
| `iss.s1_str_mdm_status` | `Optional[str]` | S1 Starboard Truss Multiplexer/Demultiplexer Status |
| `iss.s1_mdm_1_status` | `Optional[str]` | S1 Truss Multiplexer/Demultiplexer 1 Status |
| `iss.s1_mdm_2_status` | `Optional[str]` | S1 Truss Multiplexer/Demultiplexer 2 Status |
| `iss.s3_mdm_1_status` | `Optional[str]` | S3 Truss Multiplexer/Demultiplexer 1 Status |
| `iss.s3_mdm_2_status` | `Optional[str]` | S3 Truss Multiplexer/Demultiplexer 2 Status |

### Solar Array Systems
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.solar_array_2a_mdm_status` | `Optional[str]` | Solar Array 2A Multiplexer/Demultiplexer Status |
| `iss.solar_array_4a_mdm_status` | `Optional[str]` | Solar Array 4A Multiplexer/Demultiplexer Status |
| `iss.solar_array_4b_mdm_status` | `Optional[str]` | Solar Array 4B Multiplexer/Demultiplexer Status |
| `iss.solar_array_2b_mdm_status` | `Optional[str]` | Solar Array 2B Multiplexer/Demultiplexer Status |
| `iss.solar_array_1a_mdm_status` | `Optional[str]` | Solar Array 1A Multiplexer/Demultiplexer Status |
| `iss.solar_array_3a_mdm_status` | `Optional[str]` | Solar Array 3A Multiplexer/Demultiplexer Status |
| `iss.solar_array_3b_mdm_status` | `Optional[str]` | Solar Array 3B Multiplexer/Demultiplexer Status |
| `iss.solar_array_1b_mdm_status` | `Optional[str]` | Solar Array 1B Multiplexer/Demultiplexer Status |

### Antenna Systems
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.sband_rfg2_azimuth` | `Optional[float]` | S-band Radio Frequency Group 2 Azimuth |
| `iss.sband_rfg2_elevation` | `Optional[float]` | S-band Radio Frequency Group 2 Elevation |
| `iss.sband_rfg2_status` | `Optional[str]` | S-band Radio Frequency Group 2 Status |
| `iss.sband_rfg1_azimuth` | `Optional[float]` | S-band Radio Frequency Group 1 Azimuth |
| `iss.sband_rfg1_elevation` | `Optional[float]` | S-band Radio Frequency Group 1 Elevation |
| `iss.sband_rfg1_status` | `Optional[str]` | S-band Radio Frequency Group 1 Status |

### Thermal Control Systems
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.loop_b_pump_flowrate` | `Optional[float]` | Thermal Control Loop B Pump Flow Rate |
| `iss.loop_b_pm_pressure` | `Optional[float]` | Thermal Control Loop B Pump Module Pressure |
| `iss.loop_b_pm_temp` | `Optional[float]` | Thermal Control Loop B Pump Module Temperature |
| `iss.loop_a_pump_flowrate` | `Optional[float]` | Thermal Control Loop A Pump Flow Rate |
| `iss.loop_a_pm_pressure` | `Optional[float]` | Thermal Control Loop A Pump Module Pressure |
| `iss.loop_a_pm_temp` | `Optional[float]` | Thermal Control Loop A Pump Module Temperature |

### Solar Array Drive Systems
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.solar_2a_drive_voltage` | `Optional[float]` | Solar Array 2A Drive Voltage |
| `iss.solar_2a_drive_current` | `Optional[float]` | Solar Array 2A Drive Current |
| `iss.solar_4a_drive_voltage` | `Optional[float]` | Solar Array 4A Drive Voltage |
| `iss.solar_4a_drive_current` | `Optional[float]` | Solar Array 4A Drive Current |
| `iss.solar_2a_bga_position` | `Optional[float]` | Solar Array 2A Beta Gimbal Assembly Position |
| `iss.solar_4a_bga_position` | `Optional[float]` | Solar Array 4A Beta Gimbal Assembly Position |
| `iss.solar_4b_drive_voltage` | `Optional[float]` | Solar Array 4B Drive Voltage |
| `iss.solar_4b_drive_current` | `Optional[float]` | Solar Array 4B Drive Current |
| `iss.solar_2b_drive_voltage` | `Optional[float]` | Solar Array 2B Drive Voltage |
| `iss.solar_2b_drive_current` | `Optional[float]` | Solar Array 2B Drive Current |
| `iss.solar_4b_bga_position` | `Optional[float]` | Solar Array 4B Beta Gimbal Assembly Position |
| `iss.solar_2b_bga_position` | `Optional[float]` | Solar Array 2B Beta Gimbal Assembly Position |
| `iss.solar_1a_drive_voltage` | `Optional[float]` | Solar Array 1A Drive Voltage |
| `iss.solar_1a_drive_current` | `Optional[float]` | Solar Array 1A Drive Current |
| `iss.solar_3a_drive_voltage` | `Optional[float]` | Solar Array 3A Drive Voltage |
| `iss.solar_3a_drive_current` | `Optional[float]` | Solar Array 3A Drive Current |
| `iss.solar_1a_bga_position` | `Optional[float]` | Solar Array 1A Beta Gimbal Assembly Position |
| `iss.solar_3a_bga_position` | `Optional[float]` | Solar Array 3A Beta Gimbal Assembly Position |
| `iss.solar_3b_drive_voltage` | `Optional[float]` | Solar Array 3B Drive Voltage |
| `iss.solar_3b_drive_current` | `Optional[float]` | Solar Array 3B Drive Current |
| `iss.solar_1b_drive_voltage` | `Optional[float]` | Solar Array 1B Drive Voltage |
| `iss.solar_1b_drive_current` | `Optional[float]` | Solar Array 1B Drive Current |
| `iss.solar_3b_bga_position` | `Optional[float]` | Solar Array 3B Beta Gimbal Assembly Position |
| `iss.solar_1b_bga_position` | `Optional[float]` | Solar Array 1B Beta Gimbal Assembly Position |

### Joint Positions
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.starboard_trrj_position` | `Optional[float]` | Starboard Thermal Radiator Rotary Joint Position |
| `iss.port_trrj_position` | `Optional[float]` | Port Thermal Radiator Rotary Joint Position |
| `iss.starboard_sarj_position` | `Optional[float]` | Starboard Solar Alpha Rotary Joint Position |
| `iss.port_sarj_position` | `Optional[float]` | Port Solar Alpha Rotary Joint Position |
| `iss.port_sarj_commanded_position` | `Optional[float]` | Port Solar Alpha Rotary Joint Commanded Position |
| `iss.trrj_loop_b_mode` | `Optional[str]` | Thermal Radiator Rotary Joint Loop B Mode |
| `iss.trrj_loop_a_mode` | `Optional[str]` | Thermal Radiator Rotary Joint Loop A Mode |
| `iss.sarj_port_mode` | `Optional[str]` | Solar Alpha Rotary Joint Port Mode |
| `iss.sarj_starboard_mode` | `Optional[str]` | Solar Alpha Rotary Joint Starboard Mode |

### Node Environmental Systems
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.node2_coolant_mt` | `Optional[float]` | Node 2 Coolant Medium Temperature |
| `iss.node2_coolant_lt` | `Optional[float]` | Node 2 Coolant Low Temperature |
| `iss.node2_ac_state` | `Optional[str]` | Node 2 Air Conditioning State |
| `iss.node2_air_cooling_temp` | `Optional[float]` | Node 2 Air Cooling Temperature |
| `iss.node2_avionics_temp` | `Optional[float]` | Node 2 Avionics Temperature |
| `iss.node3_ppo2` | `Optional[float]` | Node 3 Partial Pressure Oxygen |
| `iss.node3_ppn2` | `Optional[float]` | Node 3 Partial Pressure Nitrogen |
| `iss.node3_ppco2` | `Optional[float]` | Node 3 Partial Pressure Carbon Dioxide |
| `iss.urine_processor_state` | `Optional[str]` | Urine Processor Assembly State |
| `iss.urine_tank_qty` | `Optional[float]` | Urine Tank Quantity |
| `iss.water_processor_state` | `Optional[str]` | Water Processor Assembly State |
| `iss.water_processor_step` | `Optional[str]` | Water Processor Assembly Processing Step |
| `iss.waste_water_tank_qty` | `Optional[float]` | Waste Water Tank Quantity |

| `iss.clean_water_tank_qty` | `Optional[float]` | Clean Water Tank Quantity |
| `iss.oxygen_generator_state` | `Optional[str]` | Oxygen Generator Assembly State |
| `iss.o2_production_rate` | `Optional[float]` | Oxygen Production Rate |
| `iss.node3_avionics_temp` | `Optional[float]` | Node 3 Avionics Temperature |
| `iss.node3_air_cooling_temp` | `Optional[float]` | Node 3 Air Cooling Temperature |
| `iss.node3_coolant_qty_1` | `Optional[float]` | Node 3 Coolant Quantity 1 |
| `iss.node3_ac_state` | `Optional[str]` | Node 3 Air Conditioning State |
| `iss.node3_coolant_qty_2` | `Optional[float]` | Node 3 Coolant Quantity 2 |

### Airlock Systems
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.crewlock_pressure` | `Optional[float]` | Crew Lock Atmospheric Pressure |
| `iss.lo_p_o2_valve_position` | `Optional[str]` | Low Pressure Oxygen Valve Position |
| `iss.hi_p_o2_valve_position` | `Optional[str]` | High Pressure Oxygen Valve Position |
| `iss.n2_supply_valve_position` | `Optional[str]` | Nitrogen Supply Valve Position |
| `iss.airlock_ac_state` | `Optional[str]` | Airlock Air Conditioning State |
| `iss.airlock_pressure` | `Optional[float]` | Airlock Atmospheric Pressure |
| `iss.airlock_hi_p_o2_pressure` | `Optional[float]` | Airlock High Pressure Oxygen Pressure |
| `iss.airlock_lo_p_o2_pressure` | `Optional[float]` | Airlock Low Pressure Oxygen Pressure |
| `iss.airlock_n2_pressure` | `Optional[float]` | Airlock Nitrogen Pressure |

### Airlock Power Systems (EMU and BCA)
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.emu_1_voltage` | `Optional[float]` | Extravehicular Mobility Unit 1 Voltage |
| `iss.emu_1_current` | `Optional[float]` | Extravehicular Mobility Unit 1 Current |
| `iss.emu_2_voltage` | `Optional[float]` | Extravehicular Mobility Unit 2 Voltage |
| `iss.emu_2_current` | `Optional[float]` | Extravehicular Mobility Unit 2 Current |
| `iss.iru_voltage` | `Optional[float]` | Interface Relay Unit Voltage |
| `iss.iru_current` | `Optional[float]` | Interface Relay Unit Current |
| `iss.eva_emu_1_voltage` | `Optional[float]` | EVA Extravehicular Mobility Unit 1 Voltage |
| `iss.eva_emu_1_current` | `Optional[float]` | EVA Extravehicular Mobility Unit 1 Current |
| `iss.eva_emu_2_voltage` | `Optional[float]` | EVA Extravehicular Mobility Unit 2 Voltage |
| `iss.eva_emu_2_current` | `Optional[float]` | EVA Extravehicular Mobility Unit 2 Current |
| `iss.bca_1_voltage` | `Optional[float]` | Battery Charger Assembly 1 Voltage |
| `iss.bca_1_current` | `Optional[float]` | Battery Charger Assembly 1 Current |
| `iss.bca_2_voltage` | `Optional[float]` | Battery Charger Assembly 2 Voltage |
| `iss.bca_2_current` | `Optional[float]` | Battery Charger Assembly 2 Current |
| `iss.bca_3_voltage` | `Optional[float]` | Battery Charger Assembly 3 Voltage |
| `iss.bca_3_current` | `Optional[float]` | Battery Charger Assembly 3 Current |
| `iss.bca_4_voltage` | `Optional[float]` | Battery Charger Assembly 4 Voltage |
| `iss.bca_4_current` | `Optional[float]` | Battery Charger Assembly 4 Current |
| `iss.bca_1_status` | `Optional[str]` | Battery Charger Assembly 1 Status |
| `iss.bca_2_status` | `Optional[str]` | Battery Charger Assembly 2 Status |
| `iss.bca_3_status` | `Optional[str]` | Battery Charger Assembly 3 Status |
| `iss.bca_4_status` | `Optional[str]` | Battery Charger Assembly 4 Status |

### Battery Charger Channel Status
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.bca_1_ch1_status` | `Optional[str]` | Battery Charger Assembly 1 Channel 1 Status |
| `iss.bca_1_ch2_status` | `Optional[str]` | Battery Charger Assembly 1 Channel 2 Status |
| `iss.bca_1_ch3_status` | `Optional[str]` | Battery Charger Assembly 1 Channel 3 Status |
| `iss.bca_1_ch4_status` | `Optional[str]` | Battery Charger Assembly 1 Channel 4 Status |
| `iss.bca_1_ch5_status` | `Optional[str]` | Battery Charger Assembly 1 Channel 5 Status |
| `iss.bca_1_ch6_status` | `Optional[str]` | Battery Charger Assembly 1 Channel 6 Status |
| `iss.depressurization_pump_voltage` | `Optional[float]` | Depressurization Pump Voltage |
| `iss.depressurization_pump_switch` | `Optional[str]` | Depressurization Pump Switch Position |

### Mobile Servicing System (MSS)
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.mss_mt_position` | `Optional[float]` | Mobile Servicing System Mobile Transporter Position |
| `iss.ssrms_base_location` | `Optional[str]` | Space Station Remote Manipulator System Base Location |
| `iss.ssrms_operating_base` | `Optional[str]` | Space Station Remote Manipulator System Operating Base |
| `iss.ssrms_sr_joint` | `Optional[float]` | SSRMS Shoulder Roll Joint Position |
| `iss.ssrms_sy_joint` | `Optional[float]` | SSRMS Shoulder Yaw Joint Position |
| `iss.ssrms_sp_joint` | `Optional[float]` | SSRMS Shoulder Pitch Joint Position |
| `iss.ssrms_ep_joint` | `Optional[float]` | SSRMS Elbow Pitch Joint Position |
| `iss.ssrms_wp_joint` | `Optional[float]` | SSRMS Wrist Pitch Joint Position |
| `iss.ssrms_wy_joint` | `Optional[float]` | SSRMS Wrist Yaw Joint Position |
| `iss.ssrms_wr_joint` | `Optional[float]` | SSRMS Wrist Roll Joint Position |
| `iss.ssrms_tip_lee_status` | `Optional[str]` | SSRMS Tip Latching End Effector Status |

### SPDM (Special Purpose Dexterous Manipulator)
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.spdm_base_location` | `Optional[str]` | Special Purpose Dexterous Manipulator Base Location |
| `iss.spdm_1_sr_joint` | `Optional[float]` | SPDM Arm 1 Shoulder Roll Joint Position |
| `iss.spdm_1_sy_joint` | `Optional[float]` | SPDM Arm 1 Shoulder Yaw Joint Position |
| `iss.spdm_1_sp_joint` | `Optional[float]` | SPDM Arm 1 Shoulder Pitch Joint Position |
| `iss.spdm_1_ep_joint` | `Optional[float]` | SPDM Arm 1 Elbow Pitch Joint Position |
| `iss.spdm_1_wp_joint` | `Optional[float]` | SPDM Arm 1 Wrist Pitch Joint Position |
| `iss.spdm_1_wy_joint` | `Optional[float]` | SPDM Arm 1 Wrist Yaw Joint Position |
| `iss.spdm_1_wr_joint` | `Optional[float]` | SPDM Arm 1 Wrist Roll Joint Position |
| `iss.spdm_1_otcm_status` | `Optional[str]` | SPDM Arm 1 Orbital Tool Change Mechanism Status |
| `iss.spdm_2_sr_joint` | `Optional[float]` | SPDM Arm 2 Shoulder Roll Joint Position |
| `iss.spdm_2_sy_joint` | `Optional[float]` | SPDM Arm 2 Shoulder Yaw Joint Position |
| `iss.spdm_2_sp_joint` | `Optional[float]` | SPDM Arm 2 Shoulder Pitch Joint Position |
| `iss.spdm_2_ep_joint` | `Optional[float]` | SPDM Arm 2 Elbow Pitch Joint Position |
| `iss.spdm_2_wp_joint` | `Optional[float]` | SPDM Arm 2 Wrist Pitch Joint Position |
| `iss.spdm_2_wy_joint` | `Optional[float]` | SPDM Arm 2 Wrist Yaw Joint Position |
| `iss.spdm_2_wr_joint` | `Optional[float]` | SPDM Arm 2 Wrist Roll Joint Position |
| `iss.spdm_2_otcm_status` | `Optional[str]` | SPDM Arm 2 Orbital Tool Change Mechanism Status |
| `iss.spdm_body_roll_joint` | `Optional[float]` | SPDM Body Roll Joint Position |
| `iss.spdm_body_status` | `Optional[str]` | SPDM Body Status |

### MBS (Mobile Base System)
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.mbs_mcas_status` | `Optional[str]` | Mobile Base System Mobile Cart Assembly Status |
| `iss.mbs_poa_status` | `Optional[str]` | Mobile Base System Payload Orbital Adapter Status |

### Russian Segment
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.russian_station_mode` | `Optional[str]` | Russian Segment Station Mode |
| `iss.kurs_equipment_1` | `Optional[str]` | Kurs Rendezvous Equipment 1 Status |
| `iss.kurs_equipment_2` | `Optional[str]` | Kurs Rendezvous Equipment 2 Status |
| `iss.kurs_p1_p2_failure` | `Optional[bool]` | Kurs P1/P2 Channel Failure Status |
| `iss.kurs_range` | `Optional[float]` | Kurs Target Range (meters) |
| `iss.kurs_range_rate` | `Optional[float]` | Kurs Target Range Rate (m/s) |
| `iss.kurs_test_mode` | `Optional[bool]` | Kurs Test Mode Status |
| `iss.kurs_capture_signal` | `Optional[bool]` | Kurs Capture Signal Status |
| `iss.kurs_target_acquisition` | `Optional[bool]` | Kurs Target Acquisition Status |
| `iss.kurs_functional_mode` | `Optional[bool]` | Kurs Functional Mode Status |
| `iss.kurs_standby_mode` | `Optional[bool]` | Kurs Standby Mode Status |
| `iss.sm_docking_flag` | `Optional[bool]` | Service Module Docking Flag |
| `iss.sm_forward_dock_engaged` | `Optional[bool]` | Service Module Forward Docking Port Engaged |
| `iss.sm_aft_dock_engaged` | `Optional[bool]` | Service Module Aft Docking Port Engaged |
| `iss.sm_nadir_dock_engaged` | `Optional[bool]` | Service Module Nadir Docking Port Engaged |
| `iss.fgb_nadir_dock_engaged` | `Optional[bool]` | Functional Cargo Block Nadir Docking Port Engaged |
| `iss.sm_nadir_udm_dock_engaged` | `Optional[bool]` | Service Module Nadir Universal Docking Module Port Engaged |
| `iss.mrm1_dock_engaged` | `Optional[bool]` | Mini Research Module 1 Docking Port Engaged |
| `iss.mrm2_dock_engaged` | `Optional[bool]` | Mini Research Module 2 Docking Port Engaged |
| `iss.sm_hooks_closed` | `Optional[bool]` | Service Module Docking Hooks Closed |
| `iss.russian_attitude_mode` | `Optional[str]` | Russian Segment Attitude Control Mode |
| `iss.russian_motion_control` | `Optional[str]` | Russian Segment Motion Control Mode |
| `iss.russian_free_drift_prep` | `Optional[bool]` | Russian Segment Free Drift Preparation |
| `iss.russian_thruster_terminated` | `Optional[bool]` | Russian Segment Thruster Terminated Status |
| `iss.russian_dynamic_mode` | `Optional[bool]` | Russian Segment Dynamic Mode Status |

### Time Systems
| Property | Return Type | Description |
|----------|-------------|-------------|
| `iss.year` | `Optional[int]` | Current Year |
| `iss.gmt_time` | `Optional[str]` | Greenwich Mean Time |
