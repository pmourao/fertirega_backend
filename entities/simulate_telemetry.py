#!/usr/bin/env python3
"""
ThingsBoard Smart Irrigation Telemetry Simulator
Continuously sends telemetry data to simulate a real irrigation system
"""

import requests
import json
import time
import random
from datetime import datetime

# Configuration
TB_URL = "http://localhost:8080"  # Change to your ThingsBoard URL
USERNAME = "tenant@thingsboard.org"  # Change to your username
PASSWORD = "tenant"  # Change to your password
INTERVAL_SECONDS = 10  # Send telemetry every 10 seconds

class TelemetrySimulator:
    def __init__(self, url, username, password):
        self.url = url
        self.token = None
        self.login(username, password)
        self.device_tokens = {}
        self.asset_ids = {}
        self.moisture_trends = {}  # Track moisture trends for realistic data

    def login(self, username, password):
        """Login to ThingsBoard and get JWT token"""
        response = requests.post(
            f"{self.url}/api/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json()["token"]
            print("✓ Successfully logged in to ThingsBoard")
        else:
            raise Exception(f"Login failed: {response.text}")

    def get_headers(self):
        """Get authorization headers"""
        return {
            "Content-Type": "application/json",
            "X-Authorization": f"Bearer {self.token}"
        }

    def get_all_devices(self):
        """Get all devices"""
        response = requests.get(
            f"{self.url}/api/tenant/devices",
            headers=self.get_headers(),
            params={"pageSize": 1000, "page": 0}
        )
        if response.status_code == 200:
            return response.json()["data"]
        return []

    def get_all_assets(self):
        """Get all assets"""
        response = requests.get(
            f"{self.url}/api/tenant/assets",
            headers=self.get_headers(),
            params={"pageSize": 1000, "page": 0, "type": "SI Field"}
        )
        if response.status_code == 200:
            return response.json()["data"]
        return []

    def get_device_credentials(self, device_id):
        """Get device credentials (access token)"""
        response = requests.get(
            f"{self.url}/api/device/{device_id}/credentials",
            headers=self.get_headers()
        )
        if response.status_code == 200:
            return response.json()["credentialsId"]
        return None

    def send_telemetry(self, access_token, telemetry_data):
        """Send telemetry data using device access token"""
        response = requests.post(
            f"{self.url}/api/v1/{access_token}/telemetry",
            json=telemetry_data
        )
        return response.status_code == 200

    def send_asset_telemetry(self, asset_id, telemetry_data):
        """Send telemetry data to asset"""
        response = requests.post(
            f"{self.url}/api/plugins/telemetry/ASSET/{asset_id}/timeseries/ANY",
            headers=self.get_headers(),
            json=telemetry_data
        )
        return response.status_code == 200

    def get_asset_devices(self, asset_id):
        """Get all devices related to an asset"""
        response = requests.get(
            f"{self.url}/api/relations/info",
            headers=self.get_headers(),
            params={
                "fromId": asset_id,
                "fromType": "ASSET"
            }
        )
        if response.status_code == 200:
            relations = response.json()
            device_ids = [rel["to"]["id"] for rel in relations if rel["to"]["entityType"] == "DEVICE"]
            return device_ids
        return []

    def get_device_telemetry(self, device_id, keys):
        """Get latest telemetry from device"""
        keys_param = ",".join(keys)
        response = requests.get(
            f"{self.url}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries",
            headers=self.get_headers(),
            params={"keys": keys_param}
        )
        if response.status_code == 200:
            data = response.json()
            result = {}
            for key, values in data.items():
                if values and len(values) > 0:
                    result[key] = values[0]["value"]
            return result
        return {}

    def initialize_devices(self):
        """Get all devices and their access tokens"""
        devices = self.get_all_devices()
        for device in devices:
            if device['type'].startswith('SI '):
                device_id = device['id']['id']
                token = self.get_device_credentials(device_id)
                if token:
                    self.device_tokens[device['name']] = {
                        'token': token,
                        'type': device['type'],
                        'id': device_id
                    }
                    # Initialize moisture trends
                    if device['type'] == 'SI Soil Moisture Sensor':
                        self.moisture_trends[device['name']] = random.randint(50, 70)

        print(f"✓ Initialized {len(self.device_tokens)} devices")

    def initialize_assets(self):
        """Get all assets"""
        assets = self.get_all_assets()
        for asset in assets:
            self.asset_ids[asset['name']] = asset['id']['id']
        print(f"✓ Initialized {len(self.asset_ids)} assets")

    def simulate_moisture_sensor(self, device_name):
        """Simulate realistic moisture sensor data"""
        # Get current trend
        current_moisture = self.moisture_trends.get(device_name, 60)

        # Random walk with bounds
        change = random.uniform(-2, 2)
        new_moisture = max(30, min(90, current_moisture + change))
        self.moisture_trends[device_name] = new_moisture

        # Simulate occasional irrigation events (moisture increases)
        if new_moisture < 45 and random.random() > 0.7:
            new_moisture += random.uniform(5, 15)
            self.moisture_trends[device_name] = new_moisture

        # Battery decreases slowly
        battery = random.randint(75, 100)

        return {
            "moisture": round(new_moisture, 1),
            "battery": battery
        }

    def simulate_water_meter(self):
        """Simulate water meter data"""
        # Pulse counter increases over time
        return {
            "pulseCounter": random.randint(0, 100),  # Incremental pulses
            "battery": random.randint(75, 100)
        }

    def simulate_smart_valve(self):
        """Simulate smart valve data"""
        return {
            "battery": random.randint(75, 100)
        }

    def calculate_field_telemetry(self, asset_id):
        """Calculate field telemetry based on connected sensors"""
        # Get all devices connected to this field
        device_ids = self.get_asset_devices(asset_id)

        moisture_values = []
        for device_id in device_ids:
            # Get device type
            device_type = None
            for name, info in self.device_tokens.items():
                if info['id'] == device_id:
                    device_type = info['type']
                    break

            if device_type == 'SI Soil Moisture Sensor':
                telemetry = self.get_device_telemetry(device_id, ['moisture'])
                if 'moisture' in telemetry:
                    try:
                        moisture_values.append(float(telemetry['moisture']))
                    except (ValueError, TypeError):
                        pass

        # Calculate average moisture
        avg_moisture = round(sum(moisture_values) / len(moisture_values), 1) if moisture_values else 60.0

        # Determine irrigation state based on moisture
        if avg_moisture < 45:
            irrigation_state = "ACTIVE"
            irrigation_task = "Low moisture - Irrigating"
        elif avg_moisture > 80:
            irrigation_state = "IDLE"
            irrigation_task = "Moisture sufficient"
        else:
            irrigation_state = "IDLE"
            irrigation_task = "None"

        # Simulate water consumption (higher when irrigating)
        water_consumption = random.randint(300, 600) if irrigation_state == "ACTIVE" else random.randint(50, 150)

        return {
            "avgMoisture": avg_moisture,
            "irrigationState": irrigation_state,
            "irrigationTask": irrigation_task,
            "schedulerEvents": json.dumps([]),
            "waterConsumption": water_consumption
        }

    def run_simulation(self):
        """Run continuous telemetry simulation"""
        print("\n" + "="*60)
        print("Starting Telemetry Simulation")
        print("="*60)
        print(f"Sending telemetry every {INTERVAL_SECONDS} seconds")
        print("Press Ctrl+C to stop\n")

        iteration = 0
        while True:
            try:
                iteration += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n[{timestamp}] Iteration {iteration}")
                print("-" * 60)

                # Send device telemetry
                for device_name, device_info in self.device_tokens.items():
                    device_type = device_info['type']
                    token = device_info['token']

                    if device_type == 'SI Soil Moisture Sensor':
                        telemetry = self.simulate_moisture_sensor(device_name)
                    elif device_type == 'SI Water Meter':
                        telemetry = self.simulate_water_meter()
                    elif device_type == 'SI Smart Valve':
                        telemetry = self.simulate_smart_valve()
                    else:
                        continue

                    if self.send_telemetry(token, telemetry):
                        print(f"✓ {device_name}: {telemetry}")

                # Send asset telemetry
                for asset_name, asset_id in self.asset_ids.items():
                    telemetry = self.calculate_field_telemetry(asset_id)
                    if self.send_asset_telemetry(asset_id, telemetry):
                        print(f"✓ {asset_name}: avgMoisture={telemetry['avgMoisture']}, state={telemetry['irrigationState']}")

                time.sleep(INTERVAL_SECONDS)

            except KeyboardInterrupt:
                print("\n\n" + "="*60)
                print("✓ Simulation stopped by user")
                print("="*60 + "\n")
                break
            except Exception as e:
                print(f"✗ Error: {e}")
                time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        simulator = TelemetrySimulator(TB_URL, USERNAME, PASSWORD)
        simulator.initialize_devices()
        simulator.initialize_assets()
        simulator.run_simulation()
    except Exception as e:
        print(f"\n✗ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
