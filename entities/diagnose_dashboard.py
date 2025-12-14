#!/usr/bin/env python3
"""
ThingsBoard Dashboard Diagnostic Tool
Checks if all required entities exist for the Smart Irrigation dashboard
"""

import requests
import json

# Configuration
TB_URL = "http://localhost:8080"  # Change to your ThingsBoard URL
USERNAME = "tenant@thingsboard.org"  # Change to your username
PASSWORD = "tenant"  # Change to your password

class DashboardDiagnostics:
    def __init__(self, url, username, password):
        self.url = url
        self.token = None
        self.login(username, password)
        self.issues = []
        self.warnings = []

    def login(self, username, password):
        """Login to ThingsBoard and get JWT token"""
        response = requests.post(
            f"{self.url}/api/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json()["token"]
            print("✓ Successfully logged in to ThingsBoard\n")
        else:
            raise Exception(f"Login failed: {response.text}")

    def get_headers(self):
        """Get authorization headers"""
        return {
            "Content-Type": "application/json",
            "X-Authorization": f"Bearer {self.token}"
        }

    def check_device_profiles(self):
        """Check if required device profiles exist"""
        print("[1/6] Checking Device Profiles...")
        print("-" * 60)

        required_profiles = [
            "SI Soil Moisture Sensor",
            "SI Water Meter",
            "SI Smart Valve"
        ]

        response = requests.get(
            f"{self.url}/api/deviceProfiles",
            headers=self.get_headers(),
            params={"pageSize": 1000, "page": 0}
        )

        if response.status_code == 200:
            profiles = response.json()["data"]
            profile_names = [p["name"] for p in profiles]

            for required in required_profiles:
                if required in profile_names:
                    print(f"  ✓ {required}")
                else:
                    print(f"  ✗ {required} - NOT FOUND")
                    self.issues.append(f"Missing device profile: {required}")
        else:
            self.issues.append("Failed to fetch device profiles")

        print()

    def check_assets(self):
        """Check if SI Field assets exist"""
        print("[2/6] Checking Assets (SI Field)...")
        print("-" * 60)

        response = requests.get(
            f"{self.url}/api/tenant/assets",
            headers=self.get_headers(),
            params={"pageSize": 1000, "page": 0, "type": "SI Field"}
        )

        if response.status_code == 200:
            assets = response.json()["data"]
            if len(assets) == 0:
                print(f"  ✗ No 'SI Field' assets found")
                self.issues.append("No SI Field assets exist")
            else:
                print(f"  ✓ Found {len(assets)} SI Field asset(s)")
                for asset in assets:
                    print(f"    - {asset['name']}")
                    self.check_asset_attributes(asset)
        else:
            self.issues.append("Failed to fetch assets")

        print()

    def check_asset_attributes(self, asset):
        """Check if asset has required attributes"""
        asset_id = asset['id']['id']

        # Check server attributes
        response = requests.get(
            f"{self.url}/api/plugins/telemetry/ASSET/{asset_id}/values/attributes/SERVER_SCOPE",
            headers=self.get_headers()
        )

        if response.status_code == 200:
            attributes = response.json()
            attr_keys = [attr['key'] for attr in attributes]

            required_attrs = ['cropType', 'maxMoistureThreshold', 'minMoistureThreshold']
            optional_attrs = ['perimeter', 'criticalAlarmsCount', 'majorAlarmsCount']

            missing_required = [attr for attr in required_attrs if attr not in attr_keys]
            missing_optional = [attr for attr in optional_attrs if attr not in attr_keys]

            if missing_required:
                self.issues.append(f"Asset '{asset['name']}' missing required attributes: {', '.join(missing_required)}")

            if missing_optional:
                self.warnings.append(f"Asset '{asset['name']}' missing optional attributes: {', '.join(missing_optional)}")

    def check_devices(self):
        """Check if SI devices exist"""
        print("[3/6] Checking Devices...")
        print("-" * 60)

        device_types = [
            "SI Soil Moisture Sensor",
            "SI Water Meter",
            "SI Smart Valve"
        ]

        total_devices = 0
        for device_type in device_types:
            response = requests.get(
                f"{self.url}/api/tenant/devices",
                headers=self.get_headers(),
                params={"pageSize": 1000, "page": 0, "type": device_type}
            )

            if response.status_code == 200:
                devices = response.json()["data"]
                count = len(devices)
                total_devices += count

                if count > 0:
                    print(f"  ✓ {device_type}: {count} device(s)")
                    for device in devices[:3]:  # Show first 3
                        print(f"    - {device['name']}")
                    if count > 3:
                        print(f"    ... and {count - 3} more")
                else:
                    print(f"  ⚠ {device_type}: No devices found")
                    self.warnings.append(f"No devices of type '{device_type}' found")

        if total_devices == 0:
            self.issues.append("No SI devices exist")

        print()

    def check_relations(self):
        """Check if relations exist between assets and devices"""
        print("[4/6] Checking Relations (Asset → Device)...")
        print("-" * 60)

        # Get all assets
        response = requests.get(
            f"{self.url}/api/tenant/assets",
            headers=self.get_headers(),
            params={"pageSize": 1000, "page": 0, "type": "SI Field"}
        )

        if response.status_code == 200:
            assets = response.json()["data"]

            for asset in assets:
                asset_id = asset['id']['id']

                # Get relations
                rel_response = requests.get(
                    f"{self.url}/api/relations/info",
                    headers=self.get_headers(),
                    params={"fromId": asset_id, "fromType": "ASSET"}
                )

                if rel_response.status_code == 200:
                    relations = rel_response.json()
                    device_relations = [r for r in relations if r['to']['entityType'] == 'DEVICE']

                    if len(device_relations) > 0:
                        print(f"  ✓ {asset['name']}: {len(device_relations)} device(s) connected")
                    else:
                        print(f"  ✗ {asset['name']}: No devices connected")
                        self.issues.append(f"Asset '{asset['name']}' has no device relations")
        print()

    def check_telemetry(self):
        """Check if recent telemetry exists"""
        print("[5/6] Checking Telemetry Data...")
        print("-" * 60)

        # Check devices
        device_response = requests.get(
            f"{self.url}/api/tenant/devices",
            headers=self.get_headers(),
            params={"pageSize": 5, "page": 0, "type": "SI Soil Moisture Sensor"}
        )

        devices_with_data = 0
        devices_checked = 0

        if device_response.status_code == 200:
            devices = device_response.json()["data"][:3]  # Check first 3

            for device in devices:
                devices_checked += 1
                device_id = device['id']['id']

                tel_response = requests.get(
                    f"{self.url}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries",
                    headers=self.get_headers(),
                    params={"keys": "moisture,battery"}
                )

                if tel_response.status_code == 200:
                    telemetry = tel_response.json()
                    if telemetry and len(telemetry) > 0:
                        print(f"  ✓ {device['name']}: Has telemetry data")
                        devices_with_data += 1
                    else:
                        print(f"  ✗ {device['name']}: No telemetry data")

        if devices_checked > 0 and devices_with_data == 0:
            self.warnings.append("No devices have telemetry data - run simulate_telemetry.py")

        # Check assets
        asset_response = requests.get(
            f"{self.url}/api/tenant/assets",
            headers=self.get_headers(),
            params={"pageSize": 3, "page": 0, "type": "SI Field"}
        )

        if asset_response.status_code == 200:
            assets = asset_response.json()["data"][:3]

            for asset in assets:
                asset_id = asset['id']['id']

                tel_response = requests.get(
                    f"{self.url}/api/plugins/telemetry/ASSET/{asset_id}/values/timeseries",
                    headers=self.get_headers(),
                    params={"keys": "avgMoisture,irrigationState"}
                )

                if tel_response.status_code == 200:
                    telemetry = tel_response.json()
                    if telemetry and len(telemetry) > 0:
                        print(f"  ✓ {asset['name']}: Has telemetry data")
                    else:
                        print(f"  ✗ {asset['name']}: No telemetry data")

        print()

    def check_dashboard(self):
        """Check if dashboard exists"""
        print("[6/6] Checking Dashboard...")
        print("-" * 60)

        response = requests.get(
            f"{self.url}/api/tenant/dashboards",
            headers=self.get_headers(),
            params={"pageSize": 1000, "page": 0}
        )

        if response.status_code == 200:
            dashboards = response.json()["data"]
            irrigation_dashboards = [d for d in dashboards if "Irrigation" in d['title']]

            if len(irrigation_dashboards) > 0:
                for dashboard in irrigation_dashboards:
                    print(f"  ✓ Found dashboard: {dashboard['title']}")
            else:
                print(f"  ⚠ No 'Irrigation' dashboard found")
                self.warnings.append("Dashboard not imported yet - import the JSON file")

        print()

    def print_summary(self):
        """Print diagnostic summary"""
        print("\n" + "="*60)
        print("DIAGNOSTIC SUMMARY")
        print("="*60)

        if len(self.issues) == 0 and len(self.warnings) == 0:
            print("\n✅ All checks passed! Your dashboard should work correctly.\n")
            print("Next steps:")
            print("1. Import the dashboard JSON if not done yet")
            print("2. Run: python3 simulate_telemetry.py")
            print("3. Open the dashboard in ThingsBoard UI")
        else:
            if len(self.issues) > 0:
                print("\n❌ CRITICAL ISSUES FOUND:")
                for i, issue in enumerate(self.issues, 1):
                    print(f"{i}. {issue}")

            if len(self.warnings) > 0:
                print("\n⚠️  WARNINGS:")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"{i}. {warning}")

            print("\n📋 RECOMMENDED ACTIONS:")
            if any("device profile" in issue.lower() for issue in self.issues):
                print("→ Run: python3 setup_irrigation_entities.py")

            if any("No SI Field" in issue for issue in self.issues):
                print("→ Run: python3 setup_irrigation_entities.py")

            if any("No devices" in issue.lower() for issue in self.issues):
                print("→ Run: python3 setup_irrigation_entities.py")

            if any("no device relations" in issue.lower() for issue in self.issues):
                print("→ Check relations in ThingsBoard UI or re-run setup script")

            if any("telemetry" in warning.lower() for warning in self.warnings):
                print("→ Run: python3 simulate_telemetry.py")

            if any("Dashboard" in warning for warning in self.warnings):
                print("→ Import dashboard JSON file via ThingsBoard UI")

        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("ThingsBoard Smart Irrigation Dashboard Diagnostics")
    print("="*60 + "\n")

    try:
        diagnostics = DashboardDiagnostics(TB_URL, USERNAME, PASSWORD)
        diagnostics.check_device_profiles()
        diagnostics.check_assets()
        diagnostics.check_devices()
        diagnostics.check_relations()
        diagnostics.check_telemetry()
        diagnostics.check_dashboard()
        diagnostics.print_summary()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
