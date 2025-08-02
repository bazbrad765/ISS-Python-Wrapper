from typing import Optional, Dict
from lightstreamer.client import LightstreamerClient, Subscription, ItemUpdate
from lightstreamer.client import SubscriptionListener
import time

class ISSListener(SubscriptionListener):
    def __init__(self,data_store):
        self.data = data_store


    def onItemUpdate(self, update):
        item = update.getItemName()
        value = update.getValue("Value")
        #value = round(float(value),2) add a float checker and add this rounder to all floats
        self.data[item] = value

class ISS:
    """a wrapper to get the live nodes from the ISS lightstreamer"""

    def __init__(self):
        self._data = {}
        self._client = None
        self._connected = False
        self._iss_telemetry_nodes = {

    # Control Moment Gyroscope (CMG) - Attitude Control
    'cmg_1_online': 'USLAB000001',
    'cmg_2_online': 'USLAB000002',
    'cmg_3_online': 'USLAB000003',
    'cmg_4_online': 'USLAB000004',
    'cmgs_online_count': 'USLAB000005',
    'cmg_control_torque_roll': 'USLAB000006',
    'cmg_control_torque_pitch': 'USLAB000007',
    'cmg_control_torque_yaw': 'USLAB000008',
    'cmg_active_momentum': 'USLAB000009',
    'cmg_momentum_percentage': 'USLAB000010',
    'desaturation_request': 'USLAB000011',
    'gnc_mode': 'USLAB000012',
    'attitude_source': 'USLAB000013',
    'rate_source': 'USLAB000014',
    'state_vector_source': 'USLAB000015',
    'attitude_controller_type': 'USLAB000016',
    'attitude_control_reference_frame': 'USLAB000017',
    
    # Attitude Quaternions
    'lvlh_quaternion_0': 'USLAB000018',
    'lvlh_quaternion_1': 'USLAB000019',
    'lvlh_quaternion_2': 'USLAB000020',
    'lvlh_quaternion_3': 'USLAB000021',
    'attitude_roll_error': 'USLAB000022',
    'attitude_pitch_error': 'USLAB000023',
    'attitude_yaw_error': 'USLAB000024',
    'commanded_quaternion_0': 'USLAB000025',
    'commanded_quaternion_1': 'USLAB000026',
    'commanded_quaternion_2': 'USLAB000027',
    'commanded_quaternion_3': 'USLAB000028',
    
    # Position and Velocity State Vectors
    'state_vector_x_pos': 'USLAB000032',
    'state_vector_y_pos': 'USLAB000033',
    'state_vector_z_pos': 'USLAB000034',
    'state_vector_x_vel': 'USLAB000035',
    'state_vector_y_vel': 'USLAB000036',
    'state_vector_z_vel': 'USLAB000037',
    
    # Station and System Status
    'cmg_capacity': 'USLAB000038',
    'iss_total_mass': 'USLAB000039',
    'solar_beta_angle': 'USLAB000040',
    'loac_cmg_alarm': 'USLAB000041',
    'loac_iss_alarm': 'USLAB000042',
    'gps_1_status': 'USLAB000043',
    'gps_2_status': 'USLAB000044',
    
    # CMG Temperatures
    'cmg_1_spin_motor_temp': 'USLAB000045',
    'cmg_2_spin_motor_temp': 'USLAB000046',
    'cmg_3_spin_motor_temp': 'USLAB000047',
    'cmg_4_spin_motor_temp': 'USLAB000048',
    'cmg_1_hall_resolver_temp': 'USLAB000049',
    'cmg_2_hall_resolver_temp': 'USLAB000050',
    'cmg_3_hall_resolver_temp': 'USLAB000051',
    'cmg_4_hall_resolver_temp': 'USLAB000052',
    
    # Environmental Control and Life Support
    'lab_ppo2': 'USLAB000053',
    'lab_ppn2': 'USLAB000054',
    'lab_ppco2': 'USLAB000055',
    'lab_coolant_lt': 'USLAB000056',
    'lab_coolant_mt': 'USLAB000057',
    'cabin_pressure': 'USLAB000058',
    'cabin_temperature': 'USLAB000059',
    'lab_avionics_temp': 'USLAB000060',
    'lab_air_cooling_temp': 'USLAB000061',
    'vacuum_resource_valve': 'USLAB000062',
    'vacuum_exhaust_valve': 'USLAB000063',
    'lab_port_ac_state': 'USLAB000064',
    'lab_starboard_ac_state': 'USLAB000065',
    
    # Multiplexer/Demultiplexer Status
    'cc_mdm_1_status': 'USLAB000066',
    'cc_mdm_2_status': 'USLAB000067',
    'cc_mdm_3_status': 'USLAB000068',
    'icz_mdm_1_status': 'USLAB000069',
    'icz_mdm_2_status': 'USLAB000070',
    'pl_mdm_1_status': 'USLAB000071',
    'pl_mdm_2_status': 'USLAB000072',
    'gnc_mdm_1_status': 'USLAB000073',
    'gnc_mdm_2_status': 'USLAB000074',
    'pmcu_1_mdm_status': 'USLAB000075',
    'pmcu_2_mdm_status': 'USLAB000076',
    'lab_mdm_1_status': 'USLAB000077',
    'lab_mdm_2_status': 'USLAB000078',
    'lab_mdm_3_status': 'USLAB000079',
    'pmm_power_status': 'USLAB000080',
    
    # Mission Control and Commands
    'attitude_maneuver_in_progress': 'USLAB000081',
    'standard_command_counter': 'USLAB000082',
    'data_load_command_counter': 'USLAB000083',
    'cc_mdm_time_coarse': 'USLAB000084',
    'cc_mdm_time_fine': 'USLAB000085',
    'station_mode': 'USLAB000086',
    'laptops_active': 'USLAB000087',
    
    # Communications
    'ku_video_ch1_activity': 'USLAB000088',
    'ku_video_ch2_activity': 'USLAB000089',
    'ku_video_ch3_activity': 'USLAB000090',
    'ku_video_ch4_activity': 'USLAB000091',
    'sband_active_string': 'USLAB000092',
    'iac_1_status': 'USLAB000093',
    'iac_2_status': 'USLAB000094',
    'video_downlink_1': 'USLAB000095',
    'video_downlink_2': 'USLAB000096',
    'video_downlink_3': 'USLAB000097',
    'video_downlink_4': 'USLAB000098',
    'uhf_1_power': 'USLAB000099',
    'uhf_2_power': 'USLAB000100',
    'uhf_frame_sync': 'USLAB000101',
    
    # CMG Vibration and Performance (Z1000 series)
    'cmg_1_vibration': 'Z1000001',
    'cmg_2_vibration': 'Z1000002',
    'cmg_3_vibration': 'Z1000003',
    'cmg_4_vibration': 'Z1000004',
    'cmg_1_spin_motor_current': 'Z1000005',
    'cmg_2_spin_motor_current': 'Z1000006',
    'cmg_3_spin_motor_current': 'Z1000007',
    'cmg_4_spin_motor_current': 'Z1000008',
    'cmg_1_wheel_speed': 'Z1000009',
    'cmg_2_wheel_speed': 'Z1000010',
    'cmg_3_wheel_speed': 'Z1000011',
    'cmg_4_wheel_speed': 'Z1000012',
    'ku_transmit': 'Z1000013',
    'ku_sgant_elevation': 'Z1000014',
    'ku_sgant_cross_elevation': 'Z1000015',
    
    # Node Systems
    'airlock_mdm_status': 'AIRLOCK000058',
    'node1_mdm_1_status': 'NODE1000001',
    'node1_mdm_2_status': 'NODE1000002',
    'node2_mdm_2_status': 'NODE2000004',
    'node2_mdm_1_status': 'NODE2000005',
    'node3_hcz_mdm_2_status': 'NODE3000014',
    'node3_mdm_2_status': 'NODE3000015',
    'node3_hcz_mdm_1_status': 'NODE3000016',
    'node3_mdm_1_status': 'NODE3000020',
    
    # Truss Systems and Solar Arrays
    'p1_mdm_1_status': 'P1000006',
    'p1_str_mdm_status': 'P1000008',
    'p1_mdm_2_status': 'P1000009',
    'p3_mdm_1_status': 'P3000001',
    'p3_mdm_2_status': 'P3000002',
    's0_ecz_mdm_1_status': 'S0000010',
    's0_mdm_1_status': 'S0000011',
    's0_ecz_mdm_2_status': 'S0000012',
    's0_mdm_2_status': 'S0000013',
    's1_str_mdm_status': 'S1000006',
    's1_mdm_1_status': 'S1000007',
    's1_mdm_2_status': 'S1000008',
    's3_mdm_1_status': 'S3000001',
    's3_mdm_2_status': 'S3000002',
    
    # Solar Array Power Systems
    'solar_array_2a_mdm_status': 'P4000003',
    'solar_array_4a_mdm_status': 'P4000006',
    'solar_array_4b_mdm_status': 'P6000003',
    'solar_array_2b_mdm_status': 'P6000006',
    'solar_array_1a_mdm_status': 'S4000003',
    'solar_array_3a_mdm_status': 'S4000006',
    'solar_array_3b_mdm_status': 'S6000003',
    'solar_array_1b_mdm_status': 'S6000006',
    
    # Antenna Systems
    'sband_rfg2_azimuth': 'P1000004',
    'sband_rfg2_elevation': 'P1000005',
    'sband_rfg2_status': 'P1000007',
    'sband_rfg1_azimuth': 'S1000004',
    'sband_rfg1_elevation': 'S1000005',
    'sband_rfg1_status': 'S1000009',
    
    # Thermal Control Systems
    'loop_b_pump_flowrate': 'P1000001',
    'loop_b_pm_pressure': 'P1000002',
    'loop_b_pm_temp': 'P1000003',
    'loop_a_pump_flowrate': 'S1000001',
    'loop_a_pm_pressure': 'S1000002',
    'loop_a_pm_temp': 'S1000003',
    
    # Solar Array Drive Systems
    'solar_2a_drive_voltage': 'P4000001',
    'solar_2a_drive_current': 'P4000002',
    'solar_4a_drive_voltage': 'P4000004',
    'solar_4a_drive_current': 'P4000005',
    'solar_2a_bga_position': 'P4000007',
    'solar_4a_bga_position': 'P4000008',
    'solar_4b_drive_voltage': 'P6000001',
    'solar_4b_drive_current': 'P6000002',
    'solar_2b_drive_voltage': 'P6000004',
    'solar_2b_drive_current': 'P6000005',
    'solar_4b_bga_position': 'P6000007',
    'solar_2b_bga_position': 'P6000008',
    'solar_1a_drive_voltage': 'S4000001',
    'solar_1a_drive_current': 'S4000002',
    'solar_3a_drive_voltage': 'S4000004',
    'solar_3a_drive_current': 'S4000005',
    'solar_1a_bga_position': 'S4000007',
    'solar_3a_bga_position': 'S4000008',
    'solar_3b_drive_voltage': 'S6000001',
    'solar_3b_drive_current': 'S6000002',
    'solar_1b_drive_voltage': 'S6000004',
    'solar_1b_drive_current': 'S6000005',
    'solar_3b_bga_position': 'S6000007',
    'solar_1b_bga_position': 'S6000008',
    
    # Joint Positions
    'starboard_trrj_position': 'S0000001',
    'port_trrj_position': 'S0000002',
    'starboard_sarj_position': 'S0000003',
    'port_sarj_position': 'S0000004',
    'port_sarj_commanded_position': 'S0000005',
    'trrj_loop_b_mode': 'S0000006',
    'trrj_loop_a_mode': 'S0000007',
    'sarj_port_mode': 'S0000008',
    'sarj_starboard_mode': 'S0000009',
    
    # Node Environmental Systems
    'node2_coolant_mt': 'NODE2000001',
    'node2_coolant_lt': 'NODE2000002',
    'node2_ac_state': 'NODE2000003',
    'node2_air_cooling_temp': 'NODE2000006',
    'node2_avionics_temp': 'NODE2000007',
    'node3_ppo2': 'NODE3000001',
    'node3_ppn2': 'NODE3000002',
    'node3_ppco2': 'NODE3000003',
    'urine_processor_state': 'NODE3000004',
    'urine_tank_qty': 'NODE3000005',
    'water_processor_state': 'NODE3000006',
    'water_processor_step': 'NODE3000007',
    'waste_water_tank_qty': 'NODE3000008',
    'clean_water_tank_qty': 'NODE3000009',
    'oxygen_generator_state': 'NODE3000010',
    'o2_production_rate': 'NODE3000011',
    'node3_avionics_temp': 'NODE3000012',
    'node3_air_cooling_temp': 'NODE3000013',
    'node3_coolant_qty_1': 'NODE3000017',
    'node3_ac_state': 'NODE3000018',
    'node3_coolant_qty_2': 'NODE3000019',
    
    # Airlock Systems
    'crewlock_pressure': 'AIRLOCK000049',
    'hi_p_o2_valve_position': 'AIRLOCK000050',
    'lo_p_o2_valve_position': 'AIRLOCK000051',
    'n2_supply_valve_position': 'AIRLOCK000052',
    'airlock_ac_state': 'AIRLOCK000053',
    'airlock_pressure': 'AIRLOCK000054',
    'airlock_hi_p_o2_pressure': 'AIRLOCK000055',
    'airlock_lo_p_o2_pressure': 'AIRLOCK000056',
    'airlock_n2_pressure': 'AIRLOCK000057',
    
    # Airlock Power Systems (EMU and BCA)
    'emu_1_voltage': 'AIRLOCK000001',
    'emu_1_current': 'AIRLOCK000002',
    'emu_2_voltage': 'AIRLOCK000003',
    'emu_2_current': 'AIRLOCK000004',
    'iru_voltage': 'AIRLOCK000005',
    'iru_current': 'AIRLOCK000006',
    'eva_emu_1_voltage': 'AIRLOCK000007',
    'eva_emu_1_current': 'AIRLOCK000008',
    'eva_emu_2_voltage': 'AIRLOCK000009',
    'eva_emu_2_current': 'AIRLOCK000010',
    'bca_1_voltage': 'AIRLOCK000011',
    'bca_1_current': 'AIRLOCK000012',
    'bca_2_voltage': 'AIRLOCK000013',
    'bca_2_current': 'AIRLOCK000014',
    'bca_3_voltage': 'AIRLOCK000015',
    'bca_3_current': 'AIRLOCK000016',
    'bca_4_voltage': 'AIRLOCK000017',
    'bca_4_current': 'AIRLOCK000018',
    'bca_1_status': 'AIRLOCK000019',
    'bca_2_status': 'AIRLOCK000020',
    'bca_3_status': 'AIRLOCK000021',
    'bca_4_status': 'AIRLOCK000022',
    
    # Battery Charger Channel Status (abbreviated - there are many more)
    'bca_1_ch1_status': 'AIRLOCK000023',
    'bca_1_ch2_status': 'AIRLOCK000024',
    'bca_1_ch3_status': 'AIRLOCK000025',
    'bca_1_ch4_status': 'AIRLOCK000026',
    'bca_1_ch5_status': 'AIRLOCK000027',
    'bca_1_ch6_status': 'AIRLOCK000028',
    'depressurization_pump_voltage': 'AIRLOCK000047',
    'depressurization_pump_switch': 'AIRLOCK000048',
    
    # Mobile Servicing System (MSS)
    'mss_mt_position': 'CSAMT000001',
    'ssrms_base_location': 'CSASSRMS002',
    'ssrms_operating_base': 'CSASSRMS003',
    'ssrms_sr_joint': 'CSASSRMS004',
    'ssrms_sy_joint': 'CSASSRMS005',
    'ssrms_sp_joint': 'CSASSRMS006',
    'ssrms_ep_joint': 'CSASSRMS007',
    'ssrms_wp_joint': 'CSASSRMS008',
    'ssrms_wy_joint': 'CSASSRMS009',
    'ssrms_wr_joint': 'CSASSRMS010',
    'ssrms_tip_lee_status': 'CSASSRMS011',
    
    # SPDM (Special Purpose Dexterous Manipulator)
    'spdm_base_location': 'CSASPDM0002',
    'spdm_1_sr_joint': 'CSASPDM0003',
    'spdm_1_sy_joint': 'CSASPDM0004',
    'spdm_1_sp_joint': 'CSASPDM0005',
    'spdm_1_ep_joint': 'CSASPDM0006',
    'spdm_1_wp_joint': 'CSASPDM0007',
    'spdm_1_wy_joint': 'CSASPDM0008',
    'spdm_1_wr_joint': 'CSASPDM0009',
    'spdm_1_otcm_status': 'CSASPDM0010',
    'spdm_2_sr_joint': 'CSASPDM0011',
    'spdm_2_sy_joint': 'CSASPDM0012',
    'spdm_2_sp_joint': 'CSASPDM0013',
    'spdm_2_ep_joint': 'CSASPDM0014',
    'spdm_2_wp_joint': 'CSASPDM0015',
    'spdm_2_wy_joint': 'CSASPDM0016',
    'spdm_2_wr_joint': 'CSASPDM0017',
    'spdm_2_otcm_status': 'CSASPDM0019',
    'spdm_body_roll_joint': 'CSASPDM0020',
    'spdm_body_status': 'CSASPDM0022',
    
    # MBS (Mobile Base System)
    'mbs_mcas_status': 'CSAMBS00002',
    'mbs_poa_status': 'CSAMBA00004',
    
    # Russian Segment
    'russian_station_mode': 'RUSSEG000001',
    'kurs_equipment_1': 'RUSSEG000002',
    'kurs_equipment_2': 'RUSSEG000003',
    'kurs_p1_p2_failure': 'RUSSEG000004',
    'kurs_range': 'RUSSEG000005',
    'kurs_range_rate': 'RUSSEG000006',
    'kurs_test_mode': 'RUSSEG000007',
    'kurs_capture_signal': 'RUSSEG000008',
    'kurs_target_acquisition': 'RUSSEG000009',
    'kurs_functional_mode': 'RUSSEG000010',
    'kurs_standby_mode': 'RUSSEG000011',
    'sm_docking_flag': 'RUSSEG000012',
    'sm_forward_dock_engaged': 'RUSSEG000013',
    'sm_aft_dock_engaged': 'RUSSEG000014',
    'sm_nadir_dock_engaged': 'RUSSEG000015',
    'fgb_nadir_dock_engaged': 'RUSSEG000016',
    'sm_nadir_udm_dock_engaged': 'RUSSEG000017',
    'mrm1_dock_engaged': 'RUSSEG000018',
    'mrm2_dock_engaged': 'RUSSEG000019',
    'sm_hooks_closed': 'RUSSEG000020', 
    'russian_attitude_mode': 'RUSSEG000021',
    'russian_motion_control': 'RUSSEG000022',
    'russian_free_drift_prep': 'RUSSEG000023',
    'russian_thruster_terminated': 'RUSSEG000024',
    'russian_dynamic_mode': 'RUSSEG000025',
    
    # Time Systems
    'gmt_time': 'TIME_000001',
    'year': 'TIME_000002'
}

    def _decode_status(self, value, mapping):
        """decode the index to the map"""
        if value is None:
            return None
        try:
            return mapping.get(int(value))
        except (ValueError, TypeError):
            return str(value)
     
    def connect(self):
        self._client = LightstreamerClient("https://push.lightstreamer.com", "ISSLIVE")
        time.sleep(1)

        #sub = Subscription("MERGE",["item1","item2","item3"],["stock_name","last_price"])

        sub = Subscription(
            mode="MERGE",
            items=list(self._iss_telemetry_nodes.values()),
            fields=['Value'])


        sub.addListener(ISSListener(self._data))
        self._client.subscribe(sub)
        self._client.connect()
        self._connected = True


    def _get_value(self, name: str) -> Optional[str]:
        if name in self._iss_telemetry_nodes:
            return self._data.get(self._iss_telemetry_nodes[name])
        else:
            print("Node name not found")
            return None


    def get_node(self,name:str):
        return self._get_value(name)
        
    @property
    def waste_water_tank(self) -> Optional[float]:
        """Waste Water Tank Quantity"""
        return self._get_value("waste_water_tank_qty")
    
    @property
    def gmt_time(self) -> Optional[str]:
        """Greenwich Mean Time"""
        return self._get_value("gmt_time")
    
    @property
    def cabin_pressure(self) -> Optional[str]:
        """Cabin Atmospheric Pressure"""
        return self._get_value("cabin_pressure")
    
    @property
    def hi_p_o2_valve_position(self) -> Optional[str]:
        """High Pressure Oxygen Valve Position"""
        value = self._get_value("hi_p_o2_valve_position")
        mapping = {0: "CLOSED", 1: "OPEN", 2: "IN-TRANSIT", 3: "FAILED"}
        return self._decode_status(value, mapping)
    

    @property
    def cmg_1_online(self) -> Optional[str]:
        """Control Moment Gyroscope 1 Online Status"""
        value = self._get_value("cmg_1_online")
        mapping = {0: "NOT IN USE", 1: "IN USE"}
        return self._decode_status(value, mapping)
    
    @property
    def cmg_2_online(self) -> Optional[str]:
        """Control Moment Gyroscope 2 Online Status"""
        value = self._get_value("cmg_2_online")
        mapping = {0: "NOT IN USE", 1: "IN USE"}
        return self._decode_status(value, mapping)
    
    @property
    def cmg_3_online(self) -> Optional[str]:
        """Control Moment Gyroscope 3 Online Status"""
        value = self._get_value("cmg_3_online")
        mapping = {0: "NOT IN USE", 1: "IN USE"}
        return self._decode_status(value, mapping)
    
    @property
    def cmg_4_online(self) -> Optional[str]:
        """Control Moment Gyroscope 4 Online Status"""
        value = self._get_value("cmg_4_online")
        mapping = {0: "NOT IN USE", 1: "IN USE"}
        return self._decode_status(value, mapping)
    
    @property
    def cmgs_online_count(self) -> Optional[int]:
        """Control Moment Gyroscopes Online Count"""
        return self._get_value("cmgs_online_count")
    
    @property
    def cmg_control_torque_roll(self) -> Optional[float]:
        """Control Moment Gyroscope Control Torque Roll"""
        return self._get_value("cmg_control_torque_roll")
    
    @property
    def cmg_control_torque_pitch(self) -> Optional[float]:
        """Control Moment Gyroscope Control Torque Pitch"""
        return self._get_value("cmg_control_torque_pitch")
    
    @property
    def cmg_control_torque_yaw(self) -> Optional[float]:
        """Control Moment Gyroscope Control Torque Yaw"""
        return self._get_value("cmg_control_torque_yaw")
    
    @property
    def cmg_active_momentum(self) -> Optional[float]:
        """Control Moment Gyroscope Active Momentum"""
        return self._get_value("cmg_active_momentum")
    
    @property
    def cmg_momentum_percentage(self) -> Optional[float]:
        """Control Moment Gyroscope Momentum Percentage"""
        return self._get_value("cmg_momentum_percentage")
    
    @property
    def desaturation_request(self) -> Optional[str]:
        """CMG Desaturation Request Status"""
        value = self._get_value("desaturation_request")
        mapping = {0: "ENABLED", 1: "INHIBITED"}
        return self._decode_status(value, mapping)
    
    @property
    def gnc_mode(self) -> Optional[str]:
        """Guidance Navigation and Control Mode"""
        return self._get_value("gnc_mode")
    
    @property
    def attitude_source(self) -> Optional[str]:
        """Attitude Determination Source"""
        value = self._get_value("attitude_source")
        mapping = {0: "NONE"}
        return self._decode_status(value, mapping)
    
    @property
    def rate_source(self) -> Optional[str]:
        """Angular Rate Source"""
        value = self._get_value("rate_source")
        mapping = {0: "NONE", 1: "RGA1", 2: "RGA2", 3: "RUSSIAN"}
        return self._decode_status(value, mapping)
    
    @property
    def state_vector_source(self) -> Optional[str]:
        """State Vector Source"""
        value = self._get_value("state_vector_source")
        mapping = {
            0: "NO_SOURCE", 1: "Unused", 2: "Unused", 3: "RUSSIAN", 
            4: "GPS1_DETERMINISTIC", 5: "GPS2_DETERMINISTIC", 6: "GROUND"
        }
        return self._decode_status(value, mapping)
    
    @property
    def attitude_controller_type(self) -> Optional[str]:
        """Attitude Controller Type"""
        value = self._get_value("attitude_controller_type")
        mapping = {0: "ATTITUDE HOLD", 1: "TEA"}
        return self._decode_status(value, mapping)
    
    @property
    def attitude_control_reference_frame(self) -> Optional[str]:
        """Attitude Control Reference Frame"""
        value = self._get_value("attitude_control_reference_frame")
        mapping = {0: "LVLH", 1: "Inertial", 2: "XPOP"}
        return self._decode_status(value, mapping)
    

    @property
    def lvlh_quaternion_0(self) -> Optional[float]:
        """Local Vertical Local Horizontal Quaternion 0"""
        return self._get_value("lvlh_quaternion_0")
    
    @property
    def lvlh_quaternion_1(self) -> Optional[float]:
        """Local Vertical Local Horizontal Quaternion 1"""
        return self._get_value("lvlh_quaternion_1")
    
    @property
    def lvlh_quaternion_2(self) -> Optional[float]:
        """Local Vertical Local Horizontal Quaternion 2"""
        return self._get_value("lvlh_quaternion_2")
    
    @property
    def lvlh_quaternion_3(self) -> Optional[float]:
        """Local Vertical Local Horizontal Quaternion 3"""
        return self._get_value("lvlh_quaternion_3")
    
    @property
    def attitude_roll_error(self) -> Optional[float]:
        """Attitude Roll Error (degrees)"""
        return self._get_value("attitude_roll_error")
    
    @property
    def attitude_pitch_error(self) -> Optional[float]:
        """Attitude Pitch Error (degrees)"""
        return self._get_value("attitude_pitch_error")
    
    @property
    def attitude_yaw_error(self) -> Optional[float]:
        """Attitude Yaw Error (degrees)"""
        return self._get_value("attitude_yaw_error")
    
    @property
    def commanded_quaternion_0(self) -> Optional[float]:
        """Commanded Attitude Quaternion 0"""
        return self._get_value("commanded_quaternion_0")
    
    @property
    def commanded_quaternion_1(self) -> Optional[float]:
        """Commanded Attitude Quaternion 1"""
        return self._get_value("commanded_quaternion_1")
    
    @property
    def commanded_quaternion_2(self) -> Optional[float]:
        """Commanded Attitude Quaternion 2"""
        return self._get_value("commanded_quaternion_2")
    
    @property
    def commanded_quaternion_3(self) -> Optional[float]:
        """Commanded Attitude Quaternion 3"""
        return self._get_value("commanded_quaternion_3")
    

    @property
    def state_vector_x_pos(self) -> Optional[float]:
        """State Vector X Position (meters)"""
        return self._get_value("state_vector_x_pos")
    
    @property
    def state_vector_y_pos(self) -> Optional[float]:
        """State Vector Y Position (meters)"""
        return self._get_value("state_vector_y_pos")
    
    @property
    def state_vector_z_pos(self) -> Optional[float]:
        """State Vector Z Position (meters)"""
        return self._get_value("state_vector_z_pos")
    
    @property
    def state_vector_x_vel(self) -> Optional[float]:
        """State Vector X Velocity (m/s)"""
        return self._get_value("state_vector_x_vel")
    
    @property
    def state_vector_y_vel(self) -> Optional[float]:
        """State Vector Y Velocity (m/s)"""
        return self._get_value("state_vector_y_vel")
    
    @property
    def state_vector_z_vel(self) -> Optional[float]:
        """State Vector Z Velocity (m/s)"""
        return self._get_value("state_vector_z_vel")
    

    @property
    def cmg_capacity(self) -> Optional[float]:
        """Control Moment Gyroscope Capacity"""
        return self._get_value("cmg_capacity")
    
    @property
    def iss_total_mass(self) -> Optional[float]:
        """International Space Station Total Mass (kg)"""
        return self._get_value("iss_total_mass")
    
    @property
    def solar_beta_angle(self) -> Optional[float]:
        """Solar Beta Angle (degrees)"""
        return self._get_value("solar_beta_angle")
    
    @property
    def loac_cmg_alarm(self) -> Optional[str]:
        """Loss of Attitude Control CMG Alarm"""
        value = self._get_value("loac_cmg_alarm")
        mapping = {0: "FALSE", 1: "TRUE"}
        return self._decode_status(value, mapping)
    
    @property
    def loac_iss_alarm(self) -> Optional[str]:
        """Loss of Attitude Control ISS Alarm"""
        value = self._get_value("loac_iss_alarm")
        mapping = {0: "FALSE", 1: "TRUE"}
        return self._decode_status(value, mapping)
    
    @property
    def gps_1_status(self) -> Optional[str]:
        """Global Positioning System 1 Status"""
        value = self._get_value("gps_1_status")
        mapping = {
            0: "DOING POSITION FIXES", 1: "SV TIMING", 2: "APPROXIMATE TIMING", 
            3: "GPS TIME", 4: "NEED INITIALIZATION", 5: "GDOP NEEDED", 
            6: "BAD TIMING", 7: "NO USABLE SV", 8: "ONLY 1 USABLE SVs", 
            9: "ONLY 2 USABLE SVs", 10: "ONLY 3 USABLE SVs", 11: "BAD INTEGRITY", 
            12: "NO VEL AVAIL", 13: "UNUSABLE FIX"
        }
        return self._decode_status(value, mapping)
    
    @property
    def gps_2_status(self) -> Optional[str]:
        """Global Positioning System 2 Status"""
        value = self._get_value("gps_2_status")
        mapping = {
            0: "DOING POSITION FIXES", 1: "SV TIMING", 2: "APPROXIMATE TIMING", 
            3: "GPS TIME", 4: "NEED INITIALIZATION", 5: "GDOP NEEDED", 
            6: "BAD TIMING", 7: "NO USABLE SV", 8: "ONLY 1 USABLE SVs", 
            9: "ONLY 2 USABLE SVs", 10: "ONLY 3 USABLE SVs", 11: "BAD INTEGRITY", 
            12: "NO VEL AVAIL", 13: "UNUSABLE FIX"
        }
        return self._decode_status(value, mapping)
    

    @property
    def cmg_1_spin_motor_temp(self) -> Optional[float]:
        """Control Moment Gyroscope 1 Spin Motor Temperature"""
        return self._get_value("cmg_1_spin_motor_temp")
    
    @property
    def cmg_2_spin_motor_temp(self) -> Optional[float]:
        """Control Moment Gyroscope 2 Spin Motor Temperature"""
        return self._get_value("cmg_2_spin_motor_temp")
    
    @property
    def cmg_3_spin_motor_temp(self) -> Optional[float]:
        """Control Moment Gyroscope 3 Spin Motor Temperature"""
        return self._get_value("cmg_3_spin_motor_temp")
    
    @property
    def cmg_4_spin_motor_temp(self) -> Optional[float]:
        """Control Moment Gyroscope 4 Spin Motor Temperature"""
        return self._get_value("cmg_4_spin_motor_temp")
    
    @property
    def cmg_1_hall_resolver_temp(self) -> Optional[float]:
        """Control Moment Gyroscope 1 Hall Resolver Temperature"""
        return self._get_value("cmg_1_hall_resolver_temp")
    
    @property
    def cmg_2_hall_resolver_temp(self) -> Optional[float]:
        """Control Moment Gyroscope 2 Hall Resolver Temperature"""
        return self._get_value("cmg_2_hall_resolver_temp")
    
    @property
    def cmg_3_hall_resolver_temp(self) -> Optional[float]:
        """Control Moment Gyroscope 3 Hall Resolver Temperature"""
        return self._get_value("cmg_3_hall_resolver_temp")
    
    @property
    def cmg_4_hall_resolver_temp(self) -> Optional[float]:
        """Control Moment Gyroscope 4 Hall Resolver Temperature"""
        return self._get_value("cmg_4_hall_resolver_temp")
    

    @property
    def lab_ppo2(self) -> Optional[float]:
        """Lab Partial Pressure Oxygen"""
        return self._get_value("lab_ppo2")
    
    @property
    def lab_ppn2(self) -> Optional[float]:
        """Lab Partial Pressure Nitrogen"""
        return self._get_value("lab_ppn2")
    
    @property
    def lab_ppco2(self) -> Optional[float]:
        """Lab Partial Pressure Carbon Dioxide"""
        return self._get_value("lab_ppco2")
    
    @property
    def lab_coolant_lt(self) -> Optional[float]:
        """Lab Coolant Loop Temperature (Low)"""
        return self._get_value("lab_coolant_lt")
    
    @property
    def lab_coolant_mt(self) -> Optional[float]:
        """Lab Coolant Loop Temperature (Medium)"""
        return self._get_value("lab_coolant_mt")
    
    @property
    def cabin_temperature(self) -> Optional[float]:
        """Cabin Temperature"""
        return self._get_value("cabin_temperature")
    
    @property
    def lab_avionics_temp(self) -> Optional[float]:
        """Lab Avionics Temperature"""
        return self._get_value("lab_avionics_temp")
    
    @property
    def lab_air_cooling_temp(self) -> Optional[float]:
        """Lab Air Cooling Temperature"""
        return self._get_value("lab_air_cooling_temp")
    
    @property
    def vacuum_resource_valve(self) -> Optional[str]:
        """Vacuum Resource Valve Position"""
        value = self._get_value("vacuum_resource_valve")
        mapping = {0: "FAIL", 1: "OPEN", 2: "CLSD", 3: "TRNS"}
        return self._decode_status(value, mapping)
    
    @property
    def vacuum_exhaust_valve(self) -> Optional[str]:
        """Vacuum Exhaust Valve Position"""
        value = self._get_value("vacuum_exhaust_valve")
        mapping = {0: "FAIL", 1: "OPEN", 2: "CLSD", 3: "TRNS"}
        return self._decode_status(value, mapping)
    
    @property
    def lab_port_ac_state(self) -> Optional[str]:
        """Lab Port Air Conditioning State"""
        value = self._get_value("lab_port_ac_state")
        mapping = {0: "RESET", 1: "DRAIN", 2: "DRYOUT", 3: "EIB OFF", 4: "OFF", 5: "ON", 6: "STARTUP", 7: "TEST"}
        return self._decode_status(value, mapping)
    
    @property
    def lab_starboard_ac_state(self) -> Optional[str]:
        """Lab Starboard Air Conditioning State"""
        value = self._get_value("lab_starboard_ac_state")
        mapping = {0: "RESET", 1: "DRAIN", 2: "DRYOUT", 3: "EIB OFF", 4: "OFF", 5: "ON", 6: "STARTUP", 7: "TEST"}
        return self._decode_status(value, mapping)
    

    @property
    def cc_mdm_1_status(self) -> Optional[str]:
        """Command and Control Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("cc_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def cc_mdm_2_status(self) -> Optional[str]:
        """Command and Control Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("cc_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def cc_mdm_3_status(self) -> Optional[str]:
        """Command and Control Multiplexer/Demultiplexer 3 Status"""
        value = self._get_value("cc_mdm_3_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def icz_mdm_1_status(self) -> Optional[str]:
        """Internal Control Zone Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("icz_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def icz_mdm_2_status(self) -> Optional[str]:
        """Internal Control Zone Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("icz_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def pl_mdm_1_status(self) -> Optional[str]:
        """Payload Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("pl_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def pl_mdm_2_status(self) -> Optional[str]:
        """Payload Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("pl_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def gnc_mdm_1_status(self) -> Optional[str]:
        """Guidance Navigation Control Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("gnc_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def gnc_mdm_2_status(self) -> Optional[str]:
        """Guidance Navigation Control Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("gnc_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def pmcu_1_mdm_status(self) -> Optional[str]:
        """Power Management Control Unit 1 Multiplexer/Demultiplexer Status"""
        value = self._get_value("pmcu_1_mdm_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def pmcu_2_mdm_status(self) -> Optional[str]:
        """Power Management Control Unit 2 Multiplexer/Demultiplexer Status"""
        value = self._get_value("pmcu_2_mdm_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def lab_mdm_1_status(self) -> Optional[str]:
        """Lab Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("lab_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def lab_mdm_2_status(self) -> Optional[str]:
        """Lab Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("lab_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def lab_mdm_3_status(self) -> Optional[str]:
        """Lab Multiplexer/Demultiplexer 3 Status"""
        value = self._get_value("lab_mdm_3_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def pmm_power_status(self) -> Optional[str]:
        """Permanent Multipurpose Module Power Status"""
        value = self._get_value("pmm_power_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    

    @property
    def attitude_maneuver_in_progress(self) -> Optional[bool]:
        """Attitude Maneuver In Progress Status"""
        return self._get_value("attitude_maneuver_in_progress")
    
    @property
    def standard_command_counter(self) -> Optional[int]:
        """Standard Command Counter"""
        return self._get_value("standard_command_counter")
    
    @property
    def data_load_command_counter(self) -> Optional[int]:
        """Data Load Command Counter"""
        return self._get_value("data_load_command_counter")
    
    @property
    def cc_mdm_time_coarse(self) -> Optional[int]:
        """Command and Control MDM Time Coarse"""
        return self._get_value("cc_mdm_time_coarse")
    
    @property
    def cc_mdm_time_fine(self) -> Optional[int]:
        """Command and Control MDM Time Fine"""
        return self._get_value("cc_mdm_time_fine")
    
    @property
    def station_mode(self) -> Optional[str]:
        """Space Station Operating Mode"""
        return self._get_value("station_mode")
    
    @property
    def laptops_active(self) -> Optional[int]:
        """Number of Active Laptops"""
        return self._get_value("laptops_active")
    

    @property
    def ku_video_ch1_activity(self) -> Optional[str]:
        """Ku-band Video Channel 1 Activity"""
        value = self._get_value("ku_video_ch1_activity")
        mapping = {0: "INACTIVE", 1: "ACTIVE"}
        return self._decode_status(value, mapping)
    
    @property
    def ku_video_ch2_activity(self) -> Optional[str]:
        """Ku-band Video Channel 2 Activity"""
        value = self._get_value("ku_video_ch2_activity")
        mapping = {0: "INACTIVE", 1: "ACTIVE"}
        return self._decode_status(value, mapping)
    
    @property
    def ku_video_ch3_activity(self) -> Optional[str]:
        """Ku-band Video Channel 3 Activity"""
        value = self._get_value("ku_video_ch3_activity")
        mapping = {0: "INACTIVE", 1: "ACTIVE"}
        return self._decode_status(value, mapping)
    
    @property
    def ku_video_ch4_activity(self) -> Optional[str]:
        """Ku-band Video Channel 4 Activity"""
        value = self._get_value("ku_video_ch4_activity")
        mapping = {0: "INACTIVE", 1: "ACTIVE"}
        return self._decode_status(value, mapping)
    
    @property
    def sband_active_string(self) -> Optional[str]:
        """S-band Active Communication String"""
        value = self._get_value("sband_active_string")
        mapping = {1: "String 1", 2: "String 2"}
        return self._decode_status(value, mapping)
    
    @property
    def iac_1_status(self) -> Optional[str]:
        """Internal Audio Controller 1 Status"""
        value = self._get_value("iac_1_status")
        mapping = {0: "Backup", 1: "Active"}
        return self._decode_status(value, mapping)
    
    @property
    def iac_2_status(self) -> Optional[str]:
        """Internal Audio Controller 2 Status"""
        value = self._get_value("iac_2_status")
        mapping = {0: "Backup", 1: "Active"}
        return self._decode_status(value, mapping)
    
    @property
    def video_downlink_1(self) -> Optional[str]:
        """Video Downlink Channel 1"""
        value = self._get_value("video_downlink_1")
        video_mapping = {
            0: "-", 1: "S3AFT", 2: "S1UPOB", 3: "SCU1 Mux", 4: "S1LOOB", 5: "JPM a", 
            6: "JPM b", 7: "S1UPIB", 8: "S1LOIB", 9: "COL 1", 10: "COL 2", 11: "P1UPIB", 
            12: "SCU2 Mux", 13: "NOD3S", 14: "P1LOIB", 15: "SCU1 Test", 16: "WETA112", 
            17: "ORB1", 18: "ORB2", 19: "P1LOOB", 20: "SCU2 Test", 21: "P3AFT", 
            22: "Payload Rack", 23: "VTR1", 24: "VTR2", 25: "NOD2LO", 26: "WETA115", 
            28: "LAB S", 31: "POA PL3", 32: "POA", 33: "SPDMS1", 34: "SPDMS2", 
            35: "MBS CLPA", 36: "SPDMLEE", 37: "MAST", 40: "BLEE", 43: "BELB", 
            48: "TELB", 50: "MSS PL3", 51: "TLEE", 52: "Lab AVU1", 53: "Lab AVU2", 
            54: "Cup AVU1", 55: "Cup AVU2", 56: "OTCM1", 57: "BODY1", 58: "OTCM2", 
            59: "BODY2", 60: "SSRMS PL1", 61: "SSRMS PL2", 62: "SSRMS PL3", 
            63: "MSS PL1", 64: "MSS PL2", 65: "LAB1D3", 66: "LAB1P2", 67: "LAB1P4", 
            68: "LABCAM", 69: "LAB1O5", 70: "LAB1O4", 71: "LAB1O3", 72: "LAB1O2", 
            73: "LAB1O1", 74: "LAB1S1", 75: "LAB1S2", 76: "LAB1S3", 77: "A/L CAM", 
            78: "LAB1S4", 79: "N1 CAM", 80: "N3 CAM"
        }
        return self._decode_status(value, video_mapping)
    
    @property
    def video_downlink_2(self) -> Optional[str]:
        """Video Downlink Channel 2"""
        value = self._get_value("video_downlink_2")
        video_mapping = {
            0: "-", 1: "S3AFT", 2: "S1UPOB", 3: "SCU1 Mux", 4: "S1LOOB", 5: "JPM a", 
            6: "JPM b", 7: "S1UPIB", 8: "S1LOIB", 9: "COL 1", 10: "COL 2", 11: "P1UPIB", 
            12: "SCU2 Mux", 13: "NOD3S", 14: "P1LOIB", 15: "SCU1 Test", 16: "WETA112", 
            17: "ORB1", 18: "ORB2", 19: "P1LOOB", 20: "SCU2 Test", 21: "P3AFT", 
            22: "Payload Rack", 23: "VTR1", 24: "VTR2", 25: "NOD2LO", 26: "WETA115", 
            28: "LAB S", 31: "POA PL3", 32: "POA", 33: "SPDMS1", 34: "SPDMS2", 
            35: "MBS CLPA", 36: "SPDMLEE", 37: "MAST", 40: "BLEE", 43: "BELB", 
            48: "TELB", 50: "MSS PL3", 51: "TLEE", 52: "Lab AVU1", 53: "Lab AVU2", 
            54: "Cup AVU1", 55: "Cup AVU2", 56: "OTCM1", 57: "BODY1", 58: "OTCM2", 
            59: "BODY2", 60: "SSRMS PL1", 61: "SSRMS PL2", 62: "SSRMS PL3", 
            63: "MSS PL1", 64: "MSS PL2", 65: "LAB1D3", 66: "LAB1P2", 67: "LAB1P4", 
            68: "LABCAM", 69: "LAB1O5", 70: "LAB1O4", 71: "LAB1O3", 72: "LAB1O2", 
            73: "LAB1O1", 74: "LAB1S1", 75: "LAB1S2", 76: "LAB1S3", 77: "A/L CAM", 
            78: "LAB1S4", 79: "N1 CAM", 80: "N3 CAM"
        }
        return self._decode_status(value, video_mapping)
    
    @property
    def video_downlink_3(self) -> Optional[str]:
        """Video Downlink Channel 3"""
        value = self._get_value("video_downlink_3")
        video_mapping = {
            0: "-", 1: "S3AFT", 2: "S1UPOB", 3: "SCU1 Mux", 4: "S1LOOB", 5: "JPM a", 
            6: "JPM b", 7: "S1UPIB", 8: "S1LOIB", 9: "COL 1", 10: "COL 2", 11: "P1UPIB", 
            12: "SCU2 Mux", 13: "NOD3S", 14: "P1LOIB", 15: "SCU1 Test", 16: "WETA112", 
            17: "ORB1", 18: "ORB2", 19: "P1LOOB", 20: "SCU2 Test", 21: "P3AFT", 
            22: "Payload Rack", 23: "VTR1", 24: "VTR2", 25: "NOD2LO", 26: "WETA115", 
            28: "LAB S", 31: "POA PL3", 32: "POA", 33: "SPDMS1", 34: "SPDMS2", 
            35: "MBS CLPA", 36: "SPDMLEE", 37: "MAST", 40: "BLEE", 43: "BELB", 
            48: "TELB", 50: "MSS PL3", 51: "TLEE", 52: "Lab AVU1", 53: "Lab AVU2", 
            54: "Cup AVU1", 55: "Cup AVU2", 56: "OTCM1", 57: "BODY1", 58: "OTCM2", 
            59: "BODY2", 60: "SSRMS PL1", 61: "SSRMS PL2", 62: "SSRMS PL3", 
            63: "MSS PL1", 64: "MSS PL2", 65: "LAB1D3", 66: "LAB1P2", 67: "LAB1P4", 
            68: "LABCAM", 69: "LAB1O5", 70: "LAB1O4", 71: "LAB1O3", 72: "LAB1O2", 
            73: "LAB1O1", 74: "LAB1S1", 75: "LAB1S2", 76: "LAB1S3", 77: "A/L CAM", 
            78: "LAB1S4", 79: "N1 CAM", 80: "N3 CAM"
        }
        return self._decode_status(value, video_mapping)
    
    @property
    def video_downlink_4(self) -> Optional[str]:
        """Video Downlink Channel 4"""
        value = self._get_value("video_downlink_4")
        video_mapping = {
            0: "-", 1: "S3AFT", 2: "S1UPOB", 3: "SCU1 Mux", 4: "S1LOOB", 5: "JPM a", 
            6: "JPM b", 7: "S1UPIB", 8: "S1LOIB", 9: "COL 1", 10: "COL 2", 11: "P1UPIB", 
            12: "SCU2 Mux", 13: "NOD3S", 14: "P1LOIB", 15: "SCU1 Test", 16: "WETA112", 
            17: "ORB1", 18: "ORB2", 19: "P1LOOB", 20: "SCU2 Test", 21: "P3AFT", 
            22: "Payload Rack", 23: "VTR1", 24: "VTR2", 25: "NOD2LO", 26: "WETA115", 
            28: "LAB S", 31: "POA PL3", 32: "POA", 33: "SPDMS1", 34: "SPDMS2", 
            35: "MBS CLPA", 36: "SPDMLEE", 37: "MAST", 40: "BLEE", 43: "BELB", 
            48: "TELB", 50: "MSS PL3", 51: "TLEE", 52: "Lab AVU1", 53: "Lab AVU2", 
            54: "Cup AVU1", 55: "Cup AVU2", 56: "OTCM1", 57: "BODY1", 58: "OTCM2", 
            59: "BODY2", 60: "SSRMS PL1", 61: "SSRMS PL2", 62: "SSRMS PL3", 
            63: "MSS PL1", 64: "MSS PL2", 65: "LAB1D3", 66: "LAB1P2", 67: "LAB1P4", 
            68: "LABCAM", 69: "LAB1O5", 70: "LAB1O4", 71: "LAB1O3", 72: "LAB1O2", 
            73: "LAB1O1", 74: "LAB1S1", 75: "LAB1S2", 76: "LAB1S3", 77: "A/L CAM", 
            78: "LAB1S4", 79: "N1 CAM", 80: "N3 CAM"
        }
        return self._decode_status(value, video_mapping)
    
    @property
    def uhf_1_power(self) -> Optional[str]:
        """Ultra High Frequency Radio 1 Power Status"""
        value = self._get_value("uhf_1_power")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def uhf_2_power(self) -> Optional[str]:
        """Ultra High Frequency Radio 2 Power Status"""
        value = self._get_value("uhf_2_power")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def uhf_frame_sync(self) -> Optional[str]:
        """Ultra High Frequency Frame Synchronization"""
        value = self._get_value("uhf_frame_sync")
        mapping = {0: "Frame Sync unlocked", 1: "Frame Sync locked"}
        return self._decode_status(value, mapping)
    

    @property
    def cmg_1_vibration(self) -> Optional[float]:
        """Control Moment Gyroscope 1 Vibration Level"""
        return self._get_value("cmg_1_vibration")
    
    @property
    def cmg_2_vibration(self) -> Optional[float]:
        """Control Moment Gyroscope 2 Vibration Level"""
        return self._get_value("cmg_2_vibration")
    
    @property
    def cmg_3_vibration(self) -> Optional[float]:
        """Control Moment Gyroscope 3 Vibration Level"""
        return self._get_value("cmg_3_vibration")
    
    @property
    def cmg_4_vibration(self) -> Optional[float]:
        """Control Moment Gyroscope 4 Vibration Level"""
        return self._get_value("cmg_4_vibration")
    
    @property
    def cmg_1_spin_motor_current(self) -> Optional[float]:
        """Control Moment Gyroscope 1 Spin Motor Current"""
        return self._get_value("cmg_1_spin_motor_current")
    
    @property
    def cmg_2_spin_motor_current(self) -> Optional[float]:
        """Control Moment Gyroscope 2 Spin Motor Current"""
        return self._get_value("cmg_2_spin_motor_current")
    
    @property
    def cmg_3_spin_motor_current(self) -> Optional[float]:
        """Control Moment Gyroscope 3 Spin Motor Current"""
        return self._get_value("cmg_3_spin_motor_current")
    
    @property
    def cmg_4_spin_motor_current(self) -> Optional[float]:
        """Control Moment Gyroscope 4 Spin Motor Current"""
        return self._get_value("cmg_4_spin_motor_current")
    
    @property
    def cmg_1_wheel_speed(self) -> Optional[float]:
        """Control Moment Gyroscope 1 Wheel Speed"""
        return self._get_value("cmg_1_wheel_speed")
    
    @property
    def cmg_2_wheel_speed(self) -> Optional[float]:
        """Control Moment Gyroscope 2 Wheel Speed"""
        return self._get_value("cmg_2_wheel_speed")
    
    @property
    def cmg_3_wheel_speed(self) -> Optional[float]:
        """Control Moment Gyroscope 3 Wheel Speed"""
        return self._get_value("cmg_3_wheel_speed")
    
    @property
    def cmg_4_wheel_speed(self) -> Optional[float]:
        """Control Moment Gyroscope 4 Wheel Speed"""
        return self._get_value("cmg_4_wheel_speed")
    
    @property
    def ku_transmit(self) -> Optional[str]:
        """Ku-band Transmit Status"""
        value = self._get_value("ku_transmit")
        mapping = {0: "RESET", 1: "NORMAL"}
        return self._decode_status(value, mapping)
    
    @property
    def ku_sgant_elevation(self) -> Optional[float]:
        """Ku-band Space-to-Ground Antenna Elevation"""
        return self._get_value("ku_sgant_elevation")
    
    @property
    def ku_sgant_cross_elevation(self) -> Optional[float]:
        """Ku-band Space-to-Ground Antenna Cross Elevation"""
        return self._get_value("ku_sgant_cross_elevation")
    

    @property
    def airlock_mdm_status(self) -> Optional[str]:
        """Airlock Multiplexer/Demultiplexer Status"""
        value = self._get_value("airlock_mdm_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def node1_mdm_1_status(self) -> Optional[str]:
        """Node 1 Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("node1_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def node1_mdm_2_status(self) -> Optional[str]:
        """Node 1 Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("node1_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def node2_mdm_2_status(self) -> Optional[str]:
        """Node 2 Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("node2_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def node2_mdm_1_status(self) -> Optional[str]:
        """Node 2 Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("node2_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def node3_hcz_mdm_2_status(self) -> Optional[str]:
        """Node 3 Health and Status Zone Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("node3_hcz_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def node3_mdm_2_status(self) -> Optional[str]:
        """Node 3 Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("node3_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def node3_hcz_mdm_1_status(self) -> Optional[str]:
        """Node 3 Health and Status Zone Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("node3_hcz_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def node3_mdm_1_status(self) -> Optional[str]:
        """Node 3 Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("node3_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    

    @property
    def p1_mdm_1_status(self) -> Optional[str]:
        """P1 Truss Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("p1_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def p1_str_mdm_status(self) -> Optional[str]:
        """P1 Starboard Truss Multiplexer/Demultiplexer Status"""
        value = self._get_value("p1_str_mdm_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def p1_mdm_2_status(self) -> Optional[str]:
        """P1 Truss Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("p1_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def p3_mdm_1_status(self) -> Optional[str]:
        """P3 Truss Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("p3_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def p3_mdm_2_status(self) -> Optional[str]:
        """P3 Truss Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("p3_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def s0_ecz_mdm_1_status(self) -> Optional[str]:
        """S0 External Control Zone Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("s0_ecz_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def s0_mdm_1_status(self) -> Optional[str]:
        """S0 Truss Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("s0_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def s0_ecz_mdm_2_status(self) -> Optional[str]:
        """S0 External Control Zone Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("s0_ecz_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def s0_mdm_2_status(self) -> Optional[str]:
        """S0 Truss Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("s0_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def s1_str_mdm_status(self) -> Optional[str]:
        """S1 Starboard Truss Multiplexer/Demultiplexer Status"""
        value = self._get_value("s1_str_mdm_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def s1_mdm_1_status(self) -> Optional[str]:
        """S1 Truss Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("s1_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def s1_mdm_2_status(self) -> Optional[str]:
        """S1 Truss Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("s1_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def s3_mdm_1_status(self) -> Optional[str]:
        """S3 Truss Multiplexer/Demultiplexer 1 Status"""
        value = self._get_value("s3_mdm_1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def s3_mdm_2_status(self) -> Optional[str]:
        """S3 Truss Multiplexer/Demultiplexer 2 Status"""
        value = self._get_value("s3_mdm_2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    

    @property
    def solar_array_2a_mdm_status(self) -> Optional[str]:
        """Solar Array 2A Multiplexer/Demultiplexer Status"""
        value = self._get_value("solar_array_2a_mdm_status")
        mapping = {0: "Not Enabled", 1: "Enabled"}
        return self._decode_status(value, mapping)
    
    @property
    def solar_array_4a_mdm_status(self) -> Optional[str]:
        """Solar Array 4A Multiplexer/Demultiplexer Status"""
        value = self._get_value("solar_array_4a_mdm_status")
        mapping = {0: "Not Enabled", 1: "Enabled"}
        return self._decode_status(value, mapping)
    
    @property
    def solar_array_4b_mdm_status(self) -> Optional[str]:
        """Solar Array 4B Multiplexer/Demultiplexer Status"""
        value = self._get_value("solar_array_4b_mdm_status")
        mapping = {0: "Not Enabled", 1: "Enabled"}
        return self._decode_status(value, mapping)
    
    @property
    def solar_array_2b_mdm_status(self) -> Optional[str]:
        """Solar Array 2B Multiplexer/Demultiplexer Status"""
        value = self._get_value("solar_array_2b_mdm_status")
        mapping = {0: "Not Enabled", 1: "Enabled"}
        return self._decode_status(value, mapping)
    
    @property
    def solar_array_1a_mdm_status(self) -> Optional[str]:
        """Solar Array 1A Multiplexer/Demultiplexer Status"""
        value = self._get_value("solar_array_1a_mdm_status")
        mapping = {0: "Not Enabled", 1: "Enabled"}
        return self._decode_status(value, mapping)
    
    @property
    def solar_array_3a_mdm_status(self) -> Optional[str]:
        """Solar Array 3A Multiplexer/Demultiplexer Status"""
        value = self._get_value("solar_array_3a_mdm_status")
        mapping = {0: "Not Enabled", 1: "Enabled"}
        return self._decode_status(value, mapping)
    
    @property
    def solar_array_3b_mdm_status(self) -> Optional[str]:
        """Solar Array 3B Multiplexer/Demultiplexer Status"""
        value = self._get_value("solar_array_3b_mdm_status")
        mapping = {0: "Not Enabled", 1: "Enabled"}
        return self._decode_status(value, mapping)
    
    @property
    def solar_array_1b_mdm_status(self) -> Optional[str]:
        """Solar Array 1B Multiplexer/Demultiplexer Status"""
        value = self._get_value("solar_array_1b_mdm_status")
        mapping = {0: "Not Enabled", 1: "Enabled"}
        return self._decode_status(value, mapping)
    

    @property
    def sband_rfg2_azimuth(self) -> Optional[float]:
        """S-band Radio Frequency Group 2 Azimuth"""
        return self._get_value("sband_rfg2_azimuth")
    
    @property
    def sband_rfg2_elevation(self) -> Optional[float]:
        """S-band Radio Frequency Group 2 Elevation"""
        return self._get_value("sband_rfg2_elevation")
    
    @property
    def sband_rfg2_status(self) -> Optional[str]:
        """S-band Radio Frequency Group 2 Status"""
        value = self._get_value("sband_rfg2_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    
    @property
    def sband_rfg1_azimuth(self) -> Optional[float]:
        """S-band Radio Frequency Group 1 Azimuth"""
        return self._get_value("sband_rfg1_azimuth")
    
    @property
    def sband_rfg1_elevation(self) -> Optional[float]:
        """S-band Radio Frequency Group 1 Elevation"""
        return self._get_value("sband_rfg1_elevation")
    
    @property
    def sband_rfg1_status(self) -> Optional[str]:
        """S-band Radio Frequency Group 1 Status"""
        value = self._get_value("sband_rfg1_status")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 3: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    

    @property
    def loop_b_pump_flowrate(self) -> Optional[float]:
        """Thermal Control Loop B Pump Flow Rate"""
        return self._get_value("loop_b_pump_flowrate")
    
    @property
    def loop_b_pm_pressure(self) -> Optional[float]:
        """Thermal Control Loop B Pump Module Pressure"""
        return self._get_value("loop_b_pm_pressure")
    
    @property
    def loop_b_pm_temp(self) -> Optional[float]:
        """Thermal Control Loop B Pump Module Temperature"""
        return self._get_value("loop_b_pm_temp")
    
    @property
    def loop_a_pump_flowrate(self) -> Optional[float]:
        """Thermal Control Loop A Pump Flow Rate"""
        return self._get_value("loop_a_pump_flowrate")
    
    @property
    def loop_a_pm_pressure(self) -> Optional[float]:
        """Thermal Control Loop A Pump Module Pressure"""
        return self._get_value("loop_a_pm_pressure")
    
    @property
    def loop_a_pm_temp(self) -> Optional[float]:
        """Thermal Control Loop A Pump Module Temperature"""
        return self._get_value("loop_a_pm_temp")
    
    @property
    def solar_2a_drive_voltage(self) -> Optional[float]:
        """Solar Array 2A Drive Voltage"""
        return self._get_value("solar_2a_drive_voltage")
    
    @property
    def solar_2a_drive_current(self) -> Optional[float]:
        """Solar Array 2A Drive Current"""
        return self._get_value("solar_2a_drive_current")
    
    @property
    def solar_4a_drive_voltage(self) -> Optional[float]:
        """Solar Array 4A Drive Voltage"""
        return self._get_value("solar_4a_drive_voltage")
    
    @property
    def solar_4a_drive_current(self) -> Optional[float]:
        """Solar Array 4A Drive Current"""
        return self._get_value("solar_4a_drive_current")
    
    @property
    def solar_2a_bga_position(self) -> Optional[float]:
        """Solar Array 2A Beta Gimbal Assembly Position"""
        return self._get_value("solar_2a_bga_position")
    
    @property
    def solar_4a_bga_position(self) -> Optional[float]:
        """Solar Array 4A Beta Gimbal Assembly Position"""
        return self._get_value("solar_4a_bga_position")
    
    @property
    def solar_4b_drive_voltage(self) -> Optional[float]:
        """Solar Array 4B Drive Voltage"""
        return self._get_value("solar_4b_drive_voltage")
    
    @property
    def solar_4b_drive_current(self) -> Optional[float]:
        """Solar Array 4B Drive Current"""
        return self._get_value("solar_4b_drive_current")
    
    @property
    def solar_2b_drive_voltage(self) -> Optional[float]:
        """Solar Array 2B Drive Voltage"""
        return self._get_value("solar_2b_drive_voltage")
    
    @property
    def solar_2b_drive_current(self) -> Optional[float]:
        """Solar Array 2B Drive Current"""
        return self._get_value("solar_2b_drive_current")
    
    @property
    def solar_4b_bga_position(self) -> Optional[float]:
        """Solar Array 4B Beta Gimbal Assembly Position"""
        return self._get_value("solar_4b_bga_position")
    
    @property
    def solar_2b_bga_position(self) -> Optional[float]:
        """Solar Array 2B Beta Gimbal Assembly Position"""
        return self._get_value("solar_2b_bga_position")
    
    @property
    def solar_1a_drive_voltage(self) -> Optional[float]:
        """Solar Array 1A Drive Voltage"""
        return self._get_value("solar_1a_drive_voltage")
    
    @property
    def solar_1a_drive_current(self) -> Optional[float]:
        """Solar Array 1A Drive Current"""
        return self._get_value("solar_1a_drive_current")
    
    @property
    def solar_3a_drive_voltage(self) -> Optional[float]:
        """Solar Array 3A Drive Voltage"""
        return self._get_value("solar_3a_drive_voltage")
    
    @property
    def solar_3a_drive_current(self) -> Optional[float]:
        """Solar Array 3A Drive Current"""
        return self._get_value("solar_3a_drive_current")
    
    @property
    def solar_1a_bga_position(self) -> Optional[float]:
        """Solar Array 1A Beta Gimbal Assembly Position"""
        return self._get_value("solar_1a_bga_position")
    
    @property
    def solar_3a_bga_position(self) -> Optional[float]:
        """Solar Array 3A Beta Gimbal Assembly Position"""
        return self._get_value("solar_3a_bga_position")
    
    @property
    def solar_3b_drive_voltage(self) -> Optional[float]:
        """Solar Array 3B Drive Voltage"""
        return self._get_value("solar_3b_drive_voltage")
    
    @property
    def solar_3b_drive_current(self) -> Optional[float]:
        """Solar Array 3B Drive Current"""
        return self._get_value("solar_3b_drive_current")
    
    @property
    def solar_1b_drive_voltage(self) -> Optional[float]:
        """Solar Array 1B Drive Voltage"""
        return self._get_value("solar_1b_drive_voltage")
    
    @property
    def solar_1b_drive_current(self) -> Optional[float]:
        """Solar Array 1B Drive Current"""
        return self._get_value("solar_1b_drive_current")
    
    @property
    def solar_3b_bga_position(self) -> Optional[float]:
        """Solar Array 3B Beta Gimbal Assembly Position"""
        return self._get_value("solar_3b_bga_position")
    
    @property
    def solar_1b_bga_position(self) -> Optional[float]:
        """Solar Array 1B Beta Gimbal Assembly Position"""
        return self._get_value("solar_1b_bga_position")
    

    @property
    def starboard_trrj_position(self) -> Optional[float]:
        """Starboard Thermal Radiator Rotary Joint Position"""
        return self._get_value("starboard_trrj_position")
    
    @property
    def port_trrj_position(self) -> Optional[float]:
        """Port Thermal Radiator Rotary Joint Position"""
        return self._get_value("port_trrj_position")
    
    @property
    def starboard_sarj_position(self) -> Optional[float]:
        """Starboard Solar Alpha Rotary Joint Position"""
        return self._get_value("starboard_sarj_position")
    
    @property
    def port_sarj_position(self) -> Optional[float]:
        """Port Solar Alpha Rotary Joint Position"""
        return self._get_value("port_sarj_position")
    
    @property
    def port_sarj_commanded_position(self) -> Optional[float]:
        """Port Solar Alpha Rotary Joint Commanded Position"""
        return self._get_value("port_sarj_commanded_position")
    
    @property
    def trrj_loop_b_mode(self) -> Optional[str]:
        """Thermal Radiator Rotary Joint Loop B Mode"""
        return self._get_value("trrj_loop_b_mode")
    
    @property
    def trrj_loop_a_mode(self) -> Optional[str]:
        """Thermal Radiator Rotary Joint Loop A Mode"""
        return self._get_value("trrj_loop_a_mode")
    
    @property
    def sarj_port_mode(self) -> Optional[str]:
        """Solar Alpha Rotary Joint Port Mode"""
        return self._get_value("sarj_port_mode")
    
    @property
    def sarj_starboard_mode(self) -> Optional[str]:
        """Solar Alpha Rotary Joint Starboard Mode"""
        return self._get_value("sarj_starboard_mode")
    

    @property
    def node2_coolant_mt(self) -> Optional[float]:
        """Node 2 Coolant Medium Temperature"""
        return self._get_value("node2_coolant_mt")
    
    @property
    def node2_coolant_lt(self) -> Optional[float]:
        """Node 2 Coolant Low Temperature"""
        return self._get_value("node2_coolant_lt")
    
    @property
    def node2_ac_state(self) -> Optional[str]:
        """Node 2 Air Conditioning State"""
        value = self._get_value("node2_ac_state")
        mapping = {0: "RESET", 1: "DRAIN", 2: "DRYOUT", 3: "EIB OFF", 4: "OFF", 5: "ON", 6: "STARTUP", 7: "TEST"}
        return self._decode_status(value, mapping)
    
    @property
    def node2_air_cooling_temp(self) -> Optional[float]:
        """Node 2 Air Cooling Temperature"""
        return self._get_value("node2_air_cooling_temp")
    
    @property
    def node2_avionics_temp(self) -> Optional[float]:
        """Node 2 Avionics Temperature"""
        return self._get_value("node2_avionics_temp")
    
    @property
    def node3_ppo2(self) -> Optional[float]:
        """Node 3 Partial Pressure Oxygen"""
        return self._get_value("node3_ppo2")
    
    @property
    def node3_ppn2(self) -> Optional[float]:
        """Node 3 Partial Pressure Nitrogen"""
        return self._get_value("node3_ppn2")
    
    @property
    def node3_ppco2(self) -> Optional[float]:
        """Node 3 Partial Pressure Carbon Dioxide"""
        return self._get_value("node3_ppco2")
    
    @property
    def urine_processor_state(self) -> Optional[str]:
        """Urine Processor Assembly State"""
        value = self._get_value("urine_processor_state")
        mapping = {2: "STOP", 4: "SHUTDOWN", 8: "MAINTENANCE", 16: "NORMAL", 32: "STANDBY", 64: "IDLE", 128: "SYSTEM INITIALIZED"}
        return self._decode_status(value, mapping)
    
    @property
    def urine_tank_qty(self) -> Optional[float]:
        """Urine Tank Quantity"""
        return self._get_value("urine_tank_qty")
    
    @property
    def water_processor_state(self) -> Optional[str]:
        """Water Processor Assembly State"""
        value = self._get_value("water_processor_state")
        mapping = {1: "STOP", 2: "SHUTDOWN", 3: "STANDBY", 4: "PROCESS", 5: "HOT SERVICE", 6: "FLUSH", 7: "WARM SHUTDOWN"}
        return self._decode_status(value, mapping)
    
    @property
    def water_processor_step(self) -> Optional[str]:
        """Water Processor Assembly Processing Step"""
        value = self._get_value("water_processor_step")
        mapping = {0: "NONE", 1: "VENT", 2: "HEATUP", 3: "PURGE", 4: "FLOW", 5: "TEST", 6: "TEST_SV_1", 7: "TEST_SV_2", 8: "SERVICE"}
        return self._decode_status(value, mapping)
    
    @property
    def waste_water_tank_qty(self) -> Optional[float]:
        """Waste Water Tank Quantity"""
        return self._get_value("waste_water_tank_qty")
    
    @property
    def clean_water_tank_qty(self) -> Optional[float]:
        """Clean Water Tank Quantity"""
        return self._get_value("clean_water_tank_qty")
    
    @property
    def oxygen_generator_state(self) -> Optional[str]:
        """Oxygen Generator Assembly State"""
        value = self._get_value("oxygen_generator_state")
        mapping = {1: "PROCESS", 2: "STANDBY", 3: "SHUTDOWN", 4: "STOP", 5: "VENT_DOME", 6: "INERT_DOME", 7: "FAST_SHUTDOWN", 8: "N2_PURGE_SHUTDOWN"}
        return self._decode_status(value, mapping)
    
    @property
    def o2_production_rate(self) -> Optional[float]:
        """Oxygen Production Rate"""
        return self._get_value("o2_production_rate")
    
    @property
    def node3_avionics_temp(self) -> Optional[float]:
        """Node 3 Avionics Temperature"""
        return self._get_value("node3_avionics_temp")
    
    @property
    def node3_air_cooling_temp(self) -> Optional[float]:
        """Node 3 Air Cooling Temperature"""
        return self._get_value("node3_air_cooling_temp")
    
    @property
    def node3_coolant_qty_1(self) -> Optional[float]:
        """Node 3 Coolant Quantity 1"""
        return self._get_value("node3_coolant_qty_1")
    
    @property
    def node3_ac_state(self) -> Optional[str]:
        """Node 3 Air Conditioning State"""
        value = self._get_value("node3_ac_state")
        mapping = {0: "RESET", 1: "DRAIN", 2: "DRYOUT", 3: "EIB OFF", 4: "OFF", 5: "ON", 6: "STARTUP", 7: "TEST"}
        return self._decode_status(value, mapping)
    
    @property
    def node3_coolant_qty_2(self) -> Optional[float]:
        """Node 3 Coolant Quantity 2"""
        return self._get_value("node3_coolant_qty_2")
    

    @property
    def crewlock_pressure(self) -> Optional[float]:
        """Crew Lock Atmospheric Pressure"""
        return self._get_value("crewlock_pressure")
    
    @property
    def lo_p_o2_valve_position(self) -> Optional[str]:
        """Low Pressure Oxygen Valve Position"""
        value = self._get_value("lo_p_o2_valve_position")
        mapping = {0: "CLOSED", 1: "OPEN", 2: "IN-TRANSIT", 3: "FAILED"}
        return self._decode_status(value, mapping)
    
    @property
    def n2_supply_valve_position(self) -> Optional[str]:
        """Nitrogen Supply Valve Position"""
        value = self._get_value("n2_supply_valve_position")
        mapping = {0: "CLOSED", 1: "OPEN", 2: "IN-TRANSIT", 3: "FAILED"}
        return self._decode_status(value, mapping)
    
    @property
    def airlock_ac_state(self) -> Optional[str]:
        """Airlock Air Conditioning State"""
        value = self._get_value("airlock_ac_state")
        mapping = {0: "RESET", 1: "DRAIN", 2: "DRYOUT", 3: "EIB OFF", 4: "OFF", 5: "ON", 6: "STARTUP", 7: "TEST"}
        return self._decode_status(value, mapping)
    
    @property
    def airlock_pressure(self) -> Optional[float]:
        """Airlock Atmospheric Pressure"""
        return self._get_value("airlock_pressure")
    
    @property
    def airlock_hi_p_o2_pressure(self) -> Optional[float]:
        """Airlock High Pressure Oxygen Pressure"""
        return self._get_value("airlock_hi_p_o2_pressure")
    
    @property
    def airlock_lo_p_o2_pressure(self) -> Optional[float]:
        """Airlock Low Pressure Oxygen Pressure"""
        return self._get_value("airlock_lo_p_o2_pressure")
    
    @property
    def airlock_n2_pressure(self) -> Optional[float]:
        """Airlock Nitrogen Pressure"""
        return self._get_value("airlock_n2_pressure")
    

    @property
    def emu_1_voltage(self) -> Optional[float]:
        """Extravehicular Mobility Unit 1 Voltage"""
        return self._get_value("emu_1_voltage")
    
    @property
    def emu_1_current(self) -> Optional[float]:
        """Extravehicular Mobility Unit 1 Current"""
        return self._get_value("emu_1_current")
    
    @property
    def emu_2_voltage(self) -> Optional[float]:
        """Extravehicular Mobility Unit 2 Voltage"""
        return self._get_value("emu_2_voltage")
    
    @property
    def emu_2_current(self) -> Optional[float]:
        """Extravehicular Mobility Unit 2 Current"""
        return self._get_value("emu_2_current")
    
    @property
    def iru_voltage(self) -> Optional[float]:
        """Interface Relay Unit Voltage"""
        return self._get_value("iru_voltage")
    
    @property
    def iru_current(self) -> Optional[float]:
        """Interface Relay Unit Current"""
        return self._get_value("iru_current")
    
    @property
    def eva_emu_1_voltage(self) -> Optional[float]:
        """EVA Extravehicular Mobility Unit 1 Voltage"""
        return self._get_value("eva_emu_1_voltage")
    
    @property
    def eva_emu_1_current(self) -> Optional[float]:
        """EVA Extravehicular Mobility Unit 1 Current"""
        return self._get_value("eva_emu_1_current")
    
    @property
    def eva_emu_2_voltage(self) -> Optional[float]:
        """EVA Extravehicular Mobility Unit 2 Voltage"""
        return self._get_value("eva_emu_2_voltage")
    
    @property
    def eva_emu_2_current(self) -> Optional[float]:
        """EVA Extravehicular Mobility Unit 2 Current"""
        return self._get_value("eva_emu_2_current")
    
    @property
    def bca_1_voltage(self) -> Optional[float]:
        """Battery Charger Assembly 1 Voltage"""
        return self._get_value("bca_1_voltage")
    
    @property
    def bca_1_current(self) -> Optional[float]:
        """Battery Charger Assembly 1 Current"""
        return self._get_value("bca_1_current")
    
    @property
    def bca_2_voltage(self) -> Optional[float]:
        """Battery Charger Assembly 2 Voltage"""
        return self._get_value("bca_2_voltage")
    
    @property
    def bca_2_current(self) -> Optional[float]:
        """Battery Charger Assembly 2 Current"""
        return self._get_value("bca_2_current")
    
    @property
    def bca_3_voltage(self) -> Optional[float]:
        """Battery Charger Assembly 3 Voltage"""
        return self._get_value("bca_3_voltage")
    
    @property
    def bca_3_current(self) -> Optional[float]:
        """Battery Charger Assembly 3 Current"""
        return self._get_value("bca_3_current")
    
    @property
    def bca_4_voltage(self) -> Optional[float]:
        """Battery Charger Assembly 4 Voltage"""
        return self._get_value("bca_4_voltage")
    
    @property
    def bca_4_current(self) -> Optional[float]:
        """Battery Charger Assembly 4 Current"""
        return self._get_value("bca_4_current")
    
    @property
    def bca_1_status(self) -> Optional[str]:
        """Battery Charger Assembly 1 Status"""
        value = self._get_value("bca_1_status")
        mapping = {0: "Normal", 1: "No Data", 2: "Missing Data", 3: "Extra Data"}
        return self._decode_status(value, mapping)
    
    @property
    def bca_2_status(self) -> Optional[str]:
        """Battery Charger Assembly 2 Status"""
        value = self._get_value("bca_2_status")
        mapping = {0: "Normal", 1: "No Data", 2: "Missing Data", 3: "Extra Data"}
        return self._decode_status(value, mapping)
    
    @property
    def bca_3_status(self) -> Optional[str]:
        """Battery Charger Assembly 3 Status"""
        value = self._get_value("bca_3_status")
        mapping = {0: "Normal", 1: "No Data", 2: "Missing Data", 3: "Extra Data"}
        return self._decode_status(value, mapping)
    
    @property
    def bca_4_status(self) -> Optional[str]:
        """Battery Charger Assembly 4 Status"""
        value = self._get_value("bca_4_status")
        mapping = {0: "Normal", 1: "No Data", 2: "Missing Data", 3: "Extra Data"}
        return self._decode_status(value, mapping)
    

    @property
    def bca_1_ch1_status(self) -> Optional[str]:
        """Battery Charger Assembly 1 Channel 1 Status"""
        value = self._get_value("bca_1_ch1_status")
        bca_mapping = {
            0: "No History - a charge has not been initiated yet", 1: "Presently charging", 
            2: "Task completed normally", 3: "Task terminated due to stop switch being toggled", 
            4: "Task terminated due to an open circuit error", 5: "Task terminated due to Wrong Batt or Hi-imp", 
            6: "Task terminated due to an over-temperature error", 7: "Amp-hour capacity test result OK", 
            8: "Amp-hour capacity test error", 9: "Task terminated due to low charge slope error", 
            10: "Task terminated due to power error", 11: "Task terminated due to reverse-polarity error", 
            12: "Task terminated due to a short-circuit error", 13: "Task terminated due to a time-out error", 
            14: "Task terminated due to an external-temperature error", 15: "Discharge", 
            16: "Wait on Discharge", 17: "Wait on Charge"
        }
        return self._decode_status(value, bca_mapping)
    
    @property
    def bca_1_ch2_status(self) -> Optional[str]:
        """Battery Charger Assembly 1 Channel 2 Status"""
        value = self._get_value("bca_1_ch2_status")
        bca_mapping = {
            0: "No History - a charge has not been initiated yet", 1: "Presently charging", 
            2: "Task completed normally", 3: "Task terminated due to stop switch being toggled", 
            4: "Task terminated due to an open circuit error", 5: "Task terminated due to Wrong Batt or Hi-imp", 
            6: "Task terminated due to an over-temperature error", 7: "Amp-hour capacity test result OK", 
            8: "Amp-hour capacity test error", 9: "Task terminated due to low charge slope error", 
            10: "Task terminated due to power error", 11: "Task terminated due to reverse-polarity error", 
            12: "Task terminated due to a short-circuit error", 13: "Task terminated due to a time-out error", 
            14: "Task terminated due to an external-temperature error", 15: "Discharge", 
            16: "Wait on Discharge", 17: "Wait on Charge"
        }
        return self._decode_status(value, bca_mapping)
    
    @property
    def bca_1_ch3_status(self) -> Optional[str]:
        """Battery Charger Assembly 1 Channel 3 Status"""
        value = self._get_value("bca_1_ch3_status")
        bca_mapping = {
            0: "No History - a charge has not been initiated yet", 1: "Presently charging", 
            2: "Task completed normally", 3: "Task terminated due to stop switch being toggled", 
            4: "Task terminated due to an open circuit error", 5: "Task terminated due to Wrong Batt or Hi-imp", 
            6: "Task terminated due to an over-temperature error", 7: "Amp-hour capacity test result OK", 
            8: "Amp-hour capacity test error", 9: "Task terminated due to low charge slope error", 
            10: "Task terminated due to power error", 11: "Task terminated due to reverse-polarity error", 
            12: "Task terminated due to a short-circuit error", 13: "Task terminated due to a time-out error", 
            14: "Task terminated due to an external-temperature error", 15: "Discharge", 
            16: "Wait on Discharge", 17: "Wait on Charge"
        }
        return self._decode_status(value, bca_mapping)
    
    @property
    def bca_1_ch4_status(self) -> Optional[str]:
        """Battery Charger Assembly 1 Channel 4 Status"""
        value = self._get_value("bca_1_ch4_status")
        bca_mapping = {
            0: "No History - a charge has not been initiated yet", 1: "Presently charging", 
            2: "Task completed normally", 3: "Task terminated due to stop switch being toggled", 
            4: "Task terminated due to an open circuit error", 5: "Task terminated due to Wrong Batt or Hi-imp", 
            6: "Task terminated due to an over-temperature error", 7: "Amp-hour capacity test result OK", 
            8: "Amp-hour capacity test error", 9: "Task terminated due to low charge slope error", 
            10: "Task terminated due to power error", 11: "Task terminated due to reverse-polarity error", 
            12: "Task terminated due to a short-circuit error", 13: "Task terminated due to a time-out error", 
            14: "Task terminated due to an external-temperature error", 15: "Discharge", 
            16: "Wait on Discharge", 17: "Wait on Charge"
        }
        return self._decode_status(value, bca_mapping)
    
    @property
    def bca_1_ch5_status(self) -> Optional[str]:
        """Battery Charger Assembly 1 Channel 5 Status"""
        value = self._get_value("bca_1_ch5_status")
        bca_mapping = {
            0: "No History - a charge has not been initiated yet", 1: "Presently charging", 
            2: "Task completed normally", 3: "Task terminated due to stop switch being toggled", 
            4: "Task terminated due to an open circuit error", 5: "Task terminated due to Wrong Batt or Hi-imp", 
            6: "Task terminated due to an over-temperature error", 7: "Amp-hour capacity test result OK", 
            8: "Amp-hour capacity test error", 9: "Task terminated due to low charge slope error", 
            10: "Task terminated due to power error", 11: "Task terminated due to reverse-polarity error", 
            12: "Task terminated due to a short-circuit error", 13: "Task terminated due to a time-out error", 
            14: "Task terminated due to an external-temperature error", 15: "Discharge", 
            16: "Wait on Discharge", 17: "Wait on Charge"
        }
        return self._decode_status(value, bca_mapping)
    
    @property
    def bca_1_ch6_status(self) -> Optional[str]:
        """Battery Charger Assembly 1 Channel 6 Status"""
        value = self._get_value("bca_1_ch6_status")
        bca_mapping = {
            0: "No History - a charge has not been initiated yet", 1: "Presently charging", 
            2: "Task completed normally", 3: "Task terminated due to stop switch being toggled", 
            4: "Task terminated due to an open circuit error", 5: "Task terminated due to Wrong Batt or Hi-imp", 
            6: "Task terminated due to an over-temperature error", 7: "Amp-hour capacity test result OK", 
            8: "Amp-hour capacity test error", 9: "Task terminated due to low charge slope error", 
            10: "Task terminated due to power error", 11: "Task terminated due to reverse-polarity error", 
            12: "Task terminated due to a short-circuit error", 13: "Task terminated due to a time-out error", 
            14: "Task terminated due to an external-temperature error", 15: "Discharge", 
            16: "Wait on Discharge", 17: "Wait on Charge"
        }
        return self._decode_status(value, bca_mapping)
    
    @property
    def depressurization_pump_voltage(self) -> Optional[float]:
        """Depressurization Pump Voltage"""
        return self._get_value("depressurization_pump_voltage")
    
    @property
    def depressurization_pump_switch(self) -> Optional[str]:
        """Depressurization Pump Switch Position"""
        value = self._get_value("depressurization_pump_switch")
        mapping = {0: "Off-Ok", 1: "Not-Off Ok", 2: "Not-Off Failed"}
        return self._decode_status(value, mapping)
    

    @property
    def mss_mt_position(self) -> Optional[float]:
        """Mobile Servicing System Mobile Transporter Position"""
        return self._get_value("mss_mt_position")
    
    @property
    def ssrms_base_location(self) -> Optional[str]:
        """Space Station Remote Manipulator System Base Location"""
        value = self._get_value("ssrms_base_location")
        mapping = {
            1: "Lab", 2: "Node3", 4: "Node2", 7: "MBS PDGF 1", 8: "MBS PDGF 2", 
            11: "MBS PDGF 3", 13: "MBS PDGF 4", 14: "FGB", 16: "POA", 
            19: "SSRMS Tip LEE", 63: "Undefined"
        }
        return self._decode_status(value, mapping)
    
    @property
    def ssrms_operating_base(self) -> Optional[str]:
        """Space Station Remote Manipulator System Operating Base"""
        value = self._get_value("ssrms_operating_base")
        mapping = {0: "Lee A", 5: "Lee B"}
        return self._decode_status(value, mapping)
    
    @property
    def ssrms_sr_joint(self) -> Optional[float]:
        """SSRMS Shoulder Roll Joint Position"""
        return self._get_value("ssrms_sr_joint")
    
    @property
    def ssrms_sy_joint(self) -> Optional[float]:
        """SSRMS Shoulder Yaw Joint Position"""
        return self._get_value("ssrms_sy_joint")
    
    @property
    def ssrms_sp_joint(self) -> Optional[float]:
        """SSRMS Shoulder Pitch Joint Position"""
        return self._get_value("ssrms_sp_joint")
    
    @property
    def ssrms_ep_joint(self) -> Optional[float]:
        """SSRMS Elbow Pitch Joint Position"""
        return self._get_value("ssrms_ep_joint")
    
    @property
    def ssrms_wp_joint(self) -> Optional[float]:
        """SSRMS Wrist Pitch Joint Position"""
        return self._get_value("ssrms_wp_joint")
    
    @property
    def ssrms_wy_joint(self) -> Optional[float]:
        """SSRMS Wrist Yaw Joint Position"""
        return self._get_value("ssrms_wy_joint")
    
    @property
    def ssrms_wr_joint(self) -> Optional[float]:
        """SSRMS Wrist Roll Joint Position"""
        return self._get_value("ssrms_wr_joint")
    
    @property
    def ssrms_tip_lee_status(self) -> Optional[str]:
        """SSRMS Tip Latching End Effector Status"""
        value = self._get_value("ssrms_tip_lee_status")
        mapping = {0: "Released", 1: "Captive", 2: "Captured"}
        return self._decode_status(value, mapping)
    

    @property
    def spdm_base_location(self) -> Optional[str]:
        """Special Purpose Dexterous Manipulator Base Location"""
        value = self._get_value("spdm_base_location")
        mapping = {
            1: "Lab", 2: "Node3", 4: "Node2", 7: "MBS PDGF 1", 8: "MBS PDGF 2", 
            11: "MBS PDGF 3", 13: "MBS PDGF 4", 14: "FGB", 16: "POA", 
            19: "SSRMS Tip LEE", 63: "Undefined"
        }
        return self._decode_status(value, mapping)
    
    @property
    def spdm_1_sr_joint(self) -> Optional[float]:
        """SPDM Arm 1 Shoulder Roll Joint Position"""
        return self._get_value("spdm_1_sr_joint")
    
    @property
    def spdm_1_sy_joint(self) -> Optional[float]:
        """SPDM Arm 1 Shoulder Yaw Joint Position"""
        return self._get_value("spdm_1_sy_joint")
    
    @property
    def spdm_1_sp_joint(self) -> Optional[float]:
        """SPDM Arm 1 Shoulder Pitch Joint Position"""
        return self._get_value("spdm_1_sp_joint")
    
    @property
    def spdm_1_ep_joint(self) -> Optional[float]:
        """SPDM Arm 1 Elbow Pitch Joint Position"""
        return self._get_value("spdm_1_ep_joint")
    
    @property
    def spdm_1_wp_joint(self) -> Optional[float]:
        """SPDM Arm 1 Wrist Pitch Joint Position"""
        return self._get_value("spdm_1_wp_joint")
    
    @property
    def spdm_1_wy_joint(self) -> Optional[float]:
        """SPDM Arm 1 Wrist Yaw Joint Position"""
        return self._get_value("spdm_1_wy_joint")
    
    @property
    def spdm_1_wr_joint(self) -> Optional[float]:
        """SPDM Arm 1 Wrist Roll Joint Position"""
        return self._get_value("spdm_1_wr_joint")
    
    @property
    def spdm_1_otcm_status(self) -> Optional[str]:
        """SPDM Arm 1 Orbital Tool Change Mechanism Status"""
        value = self._get_value("spdm_1_otcm_status")
        mapping = {0: "Released", 1: "Captive", 2: "Captured"}
        return self._decode_status(value, mapping)
    
    @property
    def spdm_2_sr_joint(self) -> Optional[float]:
        """SPDM Arm 2 Shoulder Roll Joint Position"""
        return self._get_value("spdm_2_sr_joint")
    
    @property
    def spdm_2_sy_joint(self) -> Optional[float]:
        """SPDM Arm 2 Shoulder Yaw Joint Position"""
        return self._get_value("spdm_2_sy_joint")
    
    @property
    def spdm_2_sp_joint(self) -> Optional[float]:
        """SPDM Arm 2 Shoulder Pitch Joint Position"""
        return self._get_value("spdm_2_sp_joint")
    
    @property
    def spdm_2_ep_joint(self) -> Optional[float]:
        """SPDM Arm 2 Elbow Pitch Joint Position"""
        return self._get_value("spdm_2_ep_joint")
    
    @property
    def spdm_2_wp_joint(self) -> Optional[float]:
        """SPDM Arm 2 Wrist Pitch Joint Position"""
        return self._get_value("spdm_2_wp_joint")
    
    @property
    def spdm_2_wy_joint(self) -> Optional[float]:
        """SPDM Arm 2 Wrist Yaw Joint Position"""
        return self._get_value("spdm_2_wy_joint")
    
    @property
    def spdm_2_wr_joint(self) -> Optional[float]:
        """SPDM Arm 2 Wrist Roll Joint Position"""
        return self._get_value("spdm_2_wr_joint")
    
    @property
    def spdm_2_otcm_status(self) -> Optional[str]:
        """SPDM Arm 2 Orbital Tool Change Mechanism Status"""
        value = self._get_value("spdm_2_otcm_status")
        mapping = {0: "Released", 1: "Captive", 2: "Captured"}
        return self._decode_status(value, mapping)
    
    @property
    def spdm_body_roll_joint(self) -> Optional[float]:
        """SPDM Body Roll Joint Position"""
        return self._get_value("spdm_body_roll_joint")
    
    @property
    def spdm_body_status(self) -> Optional[str]:
        """SPDM Body Status"""
        value = self._get_value("spdm_body_status")
        mapping = {0: "Released", 1: "Captive", 2: "Captured"}
        return self._decode_status(value, mapping)
    

    @property
    def mbs_mcas_status(self) -> Optional[str]:
        """Mobile Base System Mobile Cart Assembly Status"""
        value = self._get_value("mbs_mcas_status")
        mapping = {0: "Released", 1: "Captured"}
        return self._decode_status(value, mapping)
    
    @property
    def mbs_poa_status(self) -> Optional[str]:
        """Mobile Base System Payload Orbital Adapter Status"""
        value = self._get_value("mbs_poa_status")
        mapping = {0: "Released", 1: "Captive", 2: "Captured"}
        return self._decode_status(value, mapping)
    

    @property
    def russian_station_mode(self) -> Optional[str]:
        """Russian Segment Station Mode"""
        return self._get_value("russian_station_mode")
    
    @property
    def kurs_equipment_1(self) -> Optional[str]:
        """Kurs Rendezvous Equipment 1 Status"""
        return self._get_value("kurs_equipment_1")
    
    @property
    def kurs_equipment_2(self) -> Optional[str]:
        """Kurs Rendezvous Equipment 2 Status"""
        return self._get_value("kurs_equipment_2")
    
    @property
    def kurs_p1_p2_failure(self) -> Optional[bool]:
        """Kurs P1/P2 Channel Failure Status"""
        return self._get_value("kurs_p1_p2_failure")
    
    @property
    def kurs_range(self) -> Optional[float]:
        """Kurs Target Range (meters)"""
        return self._get_value("kurs_range")
    
    @property
    def kurs_range_rate(self) -> Optional[float]:
        """Kurs Target Range Rate (m/s)"""
        return self._get_value("kurs_range_rate")
    
    @property
    def kurs_test_mode(self) -> Optional[bool]:
        """Kurs Test Mode Status"""
        return self._get_value("kurs_test_mode")
    
    @property
    def kurs_capture_signal(self) -> Optional[bool]:
        """Kurs Capture Signal Status"""
        return self._get_value("kurs_capture_signal")
    
    @property
    def kurs_target_acquisition(self) -> Optional[bool]:
        """Kurs Target Acquisition Status"""
        return self._get_value("kurs_target_acquisition")
    
    @property
    def kurs_functional_mode(self) -> Optional[bool]:
        """Kurs Functional Mode Status"""
        return self._get_value("kurs_functional_mode")
    
    @property
    def kurs_standby_mode(self) -> Optional[bool]:
        """Kurs Standby Mode Status"""
        return self._get_value("kurs_standby_mode")
    
    @property
    def sm_docking_flag(self) -> Optional[bool]:
        """Service Module Docking Flag"""
        return self._get_value("sm_docking_flag")
    
    @property
    def sm_forward_dock_engaged(self) -> Optional[bool]:
        """Service Module Forward Docking Port Engaged"""
        return self._get_value("sm_forward_dock_engaged")
    
    @property
    def sm_aft_dock_engaged(self) -> Optional[bool]:
        """Service Module Aft Docking Port Engaged"""
        return self._get_value("sm_aft_dock_engaged")
    
    @property
    def sm_nadir_dock_engaged(self) -> Optional[bool]:
        """Service Module Nadir Docking Port Engaged"""
        return self._get_value("sm_nadir_dock_engaged")
    
    @property
    def fgb_nadir_dock_engaged(self) -> Optional[bool]:
        """Functional Cargo Block Nadir Docking Port Engaged"""
        return self._get_value("fgb_nadir_dock_engaged")
    
    @property
    def sm_nadir_udm_dock_engaged(self) -> Optional[bool]:
        """Service Module Nadir Universal Docking Module Port Engaged"""
        return self._get_value("sm_nadir_udm_dock_engaged")
    
    @property
    def mrm1_dock_engaged(self) -> Optional[bool]:
        """Mini Research Module 1 Docking Port Engaged"""
        return self._get_value("mrm1_dock_engaged")
    
    @property
    def mrm2_dock_engaged(self) -> Optional[bool]:
        """Mini Research Module 2 Docking Port Engaged"""
        return self._get_value("mrm2_dock_engaged")
    
    @property
    def sm_hooks_closed(self) -> Optional[bool]:
        """Service Module Docking Hooks Closed"""
        return self._get_value("sm_hooks_closed")
    
    @property
    def russian_attitude_mode(self) -> Optional[str]:
        """Russian Segment Attitude Control Mode"""
        return self._get_value("russian_attitude_mode")
    
    @property
    def russian_motion_control(self) -> Optional[str]:
        """Russian Segment Motion Control Mode"""
        return self._get_value("russian_motion_control")
    
    @property
    def russian_free_drift_prep(self) -> Optional[bool]:
        """Russian Segment Free Drift Preparation"""
        return self._get_value("russian_free_drift_prep")
    
    @property
    def russian_thruster_terminated(self) -> Optional[bool]:
        """Russian Segment Thruster Terminated Status"""
        return self._get_value("russian_thruster_terminated")
    
    @property
    def russian_dynamic_mode(self) -> Optional[bool]:
        """Russian Segment Dynamic Mode Status"""
        return self._get_value("russian_dynamic_mode")
    

    @property
    def year(self) -> Optional[int]:
        """Current Year"""
        return self._get_value("year")
    

