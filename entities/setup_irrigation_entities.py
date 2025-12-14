#!/usr/bin/env python3
"""
ThingsBoard Smart Irrigation Entity Setup Script
This script creates all necessary entities for the Smart Irrigation dashboard
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta

# Configuration
TB_URL = "http://localhost:8080"  # Change to your ThingsBoard URL
USERNAME = "tenant@thingsboard.org"  # Change to your username
PASSWORD = "tenant"  # Change to your password

class ThingsBoardClient:
    def __init__(self, url, username, password):
        self.url = url
        self.token = None
        self.login(username, password)

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

    def create_device_profile(self, profile_data):
        """Create device profile"""
        response = requests.post(
            f"{self.url}/api/deviceProfile",
            headers=self.get_headers(),
            json=profile_data
        )
        if response.status_code == 200:
            profile = response.json()
            print(f"✓ Created device profile: {profile_data['name']}")
            return profile
        else:
            print(f"✗ Failed to create device profile {profile_data['name']}: {response.text}")
            return None

    def get_device_profile_by_name(self, name):
        """Get device profile by name"""
        response = requests.get(
            f"{self.url}/api/deviceProfiles",
            headers=self.get_headers(),
            params={"pageSize": 1000, "page": 0}
        )
        if response.status_code == 200:
            profiles = response.json()["data"]
            for profile in profiles:
                if profile["name"] == name:
                    return profile
        return None

    def create_asset(self, asset_data):
        """Create asset"""
        response = requests.post(
            f"{self.url}/api/asset",
            headers=self.get_headers(),
            json=asset_data
        )
        if response.status_code == 200:
            asset = response.json()
            print(f"✓ Created asset: {asset_data['name']}")
            return asset
        else:
            print(f"✗ Failed to create asset {asset_data['name']}: {response.text}")
            return None

    def create_device(self, device_data):
        """Create device"""
        response = requests.post(
            f"{self.url}/api/device",
            headers=self.get_headers(),
            json=device_data
        )
        if response.status_code == 200:
            device = response.json()
            print(f"✓ Created device: {device_data['name']}")
            return device
        else:
            print(f"✗ Failed to create device {device_data['name']}: {response.text}")
            return None

    def save_attributes(self, entity_type, entity_id, attributes, scope="SERVER_SCOPE"):
        """Save entity attributes"""
        response = requests.post(
            f"{self.url}/api/plugins/telemetry/{entity_type}/{entity_id}/attributes/{scope}",
            headers=self.get_headers(),
            json=attributes
        )
        if response.status_code == 200:
            print(f"✓ Saved attributes for {entity_type} {entity_id}")
            return True
        else:
            print(f"✗ Failed to save attributes: {response.text}")
            return False

    def create_relation(self, from_id, from_type, to_id, to_type, relation_type="Contains"):
        """Create relation between entities"""
        relation_data = {
            "from": {
                "entityType": from_type,
                "id": from_id
            },
            "to": {
                "entityType": to_type,
                "id": to_id
            },
            "type": relation_type,
            "typeGroup": "COMMON"
        }
        response = requests.post(
            f"{self.url}/api/relation",
            headers=self.get_headers(),
            json=relation_data
        )
        if response.status_code == 200:
            print(f"✓ Created relation from {from_type} to {to_type}")
            return True
        else:
            print(f"✗ Failed to create relation: {response.text}")
            return False

    def get_device_credentials(self, device_id):
        """Get device credentials (access token)"""
        response = requests.get(
            f"{self.url}/api/device/{device_id}/credentials",
            headers=self.get_headers()
        )
        if response.status_code == 200:
            return response.json()
        return None

    def send_telemetry(self, access_token, telemetry_data):
        """Send telemetry data using device access token"""
        response = requests.post(
            f"{self.url}/api/v1/{access_token}/telemetry",
            json=telemetry_data
        )
        if response.status_code == 200:
            return True
        else:
            print(f"✗ Failed to send telemetry: {response.text}")
            return False

    def send_asset_telemetry(self, asset_id, telemetry_data):
        """Send telemetry data to asset"""
        response = requests.post(
            f"{self.url}/api/plugins/telemetry/ASSET/{asset_id}/timeseries/ANY",
            headers=self.get_headers(),
            json=telemetry_data
        )
        if response.status_code == 200:
            return True
        else:
            print(f"✗ Failed to send asset telemetry: {response.text}")
            return False


def setup_irrigation_system():
    """Main setup function"""
    print("\n" + "="*60)
    print("ThingsBoard Smart Irrigation System Setup")
    print("="*60 + "\n")

    # Initialize client
    client = ThingsBoardClient(TB_URL, USERNAME, PASSWORD)

    # Step 1: Create Device Profiles
    print("\n[1/6] Creating Device Profiles...")
    print("-" * 60)

    with open('01_device_profile_soil_moisture.json', 'r') as f:
        moisture_profile = json.load(f)
        client.create_device_profile(moisture_profile)

    with open('02_device_profile_water_meter.json', 'r') as f:
        meter_profile = json.load(f)
        client.create_device_profile(meter_profile)

    with open('03_device_profile_smart_valve.json', 'r') as f:
        valve_profile = json.load(f)
        client.create_device_profile(valve_profile)

    time.sleep(1)

    # Get device profile IDs
    moisture_profile_id = client.get_device_profile_by_name("SI Soil Moisture Sensor")["id"]["id"]
    meter_profile_id = client.get_device_profile_by_name("SI Water Meter")["id"]["id"]
    valve_profile_id = client.get_device_profile_by_name("SI Smart Valve")["id"]["id"]

    # Step 2: Create Assets (Fields)
    print("\n[2/6] Creating Assets (Fields)...")
    print("-" * 60)

    with open('04_sample_assets.json', 'r') as f:
        assets_data = json.load(f)

    assets = {}
    for asset_data in assets_data:
        attributes = asset_data.pop('attributes', {})
        asset = client.create_asset(asset_data)
        if asset:
            assets[asset['name']] = asset
            # Save attributes
            if 'server' in attributes:
                client.save_attributes('ASSET', asset['id']['id'], attributes['server'])

    time.sleep(1)

    # Step 3: Create Devices
    print("\n[3/6] Creating Devices...")
    print("-" * 60)

    with open('05_sample_devices.json', 'r') as f:
        devices_data = json.load(f)

    devices = {}
    for device_data in devices_data:
        attributes = device_data.pop('attributes', {})
        field_association = device_data.pop('fieldAssociation', None)

        # Get device profile ID
        profile_name = device_data.pop('deviceProfileName')
        if profile_name == "SI Soil Moisture Sensor":
            device_data['deviceProfileId'] = {"id": moisture_profile_id, "entityType": "DEVICE_PROFILE"}
        elif profile_name == "SI Water Meter":
            device_data['deviceProfileId'] = {"id": meter_profile_id, "entityType": "DEVICE_PROFILE"}
        elif profile_name == "SI Smart Valve":
            device_data['deviceProfileId'] = {"id": valve_profile_id, "entityType": "DEVICE_PROFILE"}

        device = client.create_device(device_data)
        if device:
            devices[device['name']] = {
                'entity': device,
                'field': field_association
            }
            # Save attributes
            if 'server' in attributes:
                client.save_attributes('DEVICE', device['id']['id'], attributes['server'])

    time.sleep(1)

    # Step 4: Create Relations
    print("\n[4/6] Creating Relations between Assets and Devices...")
    print("-" * 60)

    for device_name, device_info in devices.items():
        device = device_info['entity']
        field_name = device_info['field']

        if field_name and field_name in assets:
            asset = assets[field_name]
            client.create_relation(
                asset['id']['id'],
                'ASSET',
                device['id']['id'],
                'DEVICE',
                'Contains'
            )

    time.sleep(1)

    # Step 5: Send Initial Telemetry to Devices
    print("\n[5/6] Sending Initial Telemetry to Devices...")
    print("-" * 60)

    for device_name, device_info in devices.items():
        device = device_info['entity']
        credentials = client.get_device_credentials(device['id']['id'])

        if credentials:
            access_token = credentials['credentialsId']

            if device['type'] == 'SI Soil Moisture Sensor':
                telemetry = {
                    "moisture": random.randint(45, 75),
                    "battery": random.randint(80, 99)
                }
            elif device['type'] == 'SI Water Meter':
                telemetry = {
                    "pulseCounter": random.randint(100000, 150000),
                    "battery": random.randint(80, 99)
                }
            elif device['type'] == 'SI Smart Valve':
                telemetry = {
                    "battery": random.randint(80, 99)
                }

            if client.send_telemetry(access_token, telemetry):
                print(f"✓ Sent telemetry to {device_name}: {telemetry}")

    time.sleep(1)

    # Step 6: Send Initial Telemetry to Assets
    print("\n[6/6] Sending Initial Telemetry to Assets...")
    print("-" * 60)

    for asset_name, asset in assets.items():
        asset_telemetry = {
            "avgMoisture": random.randint(50, 70),
            "irrigationState": "IDLE",
            "irrigationTask": "None",
            "schedulerEvents": json.dumps([]),
            "waterConsumption": random.randint(100, 500)
        }

        if client.send_asset_telemetry(asset['id']['id'], asset_telemetry):
            print(f"✓ Sent telemetry to {asset_name}: avgMoisture={asset_telemetry['avgMoisture']}")

    print("\n" + "="*60)
    print("✓ Setup Complete!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Go to your ThingsBoard instance")
    print("2. Navigate to Dashboards")
    print("3. Import the dashboard JSON file")
    print("4. The dashboard should now display your Fields and Sensors")
    print("\nTo send continuous telemetry, run: python3 simulate_telemetry.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        setup_irrigation_system()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
