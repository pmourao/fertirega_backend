# ThingsBoard Smart Irrigation Dashboard Setup Guide

This guide will help you set up all the necessary entities to make the Smart Irrigation dashboard work properly in ThingsBoard Community Edition.

## 📋 Overview

The Smart Irrigation dashboard requires the following components:

### Device Types
1. **SI Soil Moisture Sensor** - Monitors soil moisture levels
2. **SI Water Meter** - Tracks water consumption
3. **SI Smart Valve** - Controls irrigation valves

### Asset Types
1. **SI Field** - Represents irrigation fields/zones

### Data Structure

```
SI Field (Asset)
├── Attributes
│   ├── cropType (e.g., "Wheat", "Corn", "Vegetables")
│   ├── perimeter (GeoJSON polygon)
│   ├── maxMoistureThreshold (e.g., 80)
│   ├── minMoistureThreshold (e.g., 40)
│   ├── criticalAlarmsCount
│   └── majorAlarmsCount
│
├── Telemetry
│   ├── avgMoisture (average from all sensors)
│   ├── irrigationState ("IDLE" or "ACTIVE")
│   ├── irrigationTask (current task description)
│   ├── schedulerEvents (JSON array)
│   └── waterConsumption (daily consumption)
│
└── Related Devices
    ├── SI Soil Moisture Sensor(s)
    │   ├── Attributes: active, latitude, longitude, thresholds
    │   └── Telemetry: moisture, battery
    │
    ├── SI Water Meter
    │   ├── Telemetry: pulseCounter, battery
    │
    └── SI Smart Valve
        └── Telemetry: battery
```

## 🚀 Quick Start

### Prerequisites

1. ThingsBoard Community Edition installed and running
2. Python 3.7+ installed
3. `requests` library: `pip install requests`

### Step 1: Configure Connection

Edit the following files and update the connection settings:

**In `setup_irrigation_entities.py`:**
```python
TB_URL = "http://localhost:8080"  # Your ThingsBoard URL
USERNAME = "tenant@thingsboard.org"  # Your username
PASSWORD = "tenant"  # Your password
```

**In `simulate_telemetry.py`:**
```python
TB_URL = "http://localhost:8080"  # Your ThingsBoard URL
USERNAME = "tenant@thingsboard.org"  # Your username
PASSWORD = "tenant"  # Your password
```

### Step 2: Run Setup Script

This will create all device profiles, assets, devices, and relationships:

```bash
cd /home/mouraop/Desktop/fertirega_backend/entities
python3 setup_irrigation_entities.py
```

The script will:
- ✓ Create 3 device profiles (Moisture Sensor, Water Meter, Smart Valve)
- ✓ Create 3 sample fields (Field A, B, C)
- ✓ Create 6 sample devices (4 moisture sensors, 1 water meter, 1 valve)
- ✓ Create relationships between fields and devices
- ✓ Send initial telemetry data

### Step 3: Import Dashboard

1. Go to ThingsBoard UI → **Dashboards**
2. Click **+** button → **Import dashboard**
3. Select the file: `/home/mouraop/Desktop/fertirega_backend/dashboard/d1c73db0-d8f8-11f0-89a2-f98bab6d1641.json`
4. Click **Import**

### Step 4: Start Telemetry Simulation

To continuously send realistic telemetry data:

```bash
python3 simulate_telemetry.py
```

This will:
- Send moisture readings every 10 seconds
- Simulate realistic moisture changes
- Update field statistics automatically
- Run until you press Ctrl+C

### Step 5: View Dashboard

1. Navigate to **Dashboards** → **Irrigation Management**
2. You should see:
   - All fields with their average moisture levels
   - Map view with sensor locations
   - Time series charts with moisture history
   - Alarm widgets

## 📁 File Structure

```
entities/
├── 01_device_profile_soil_moisture.json  # Device profile for moisture sensors
├── 02_device_profile_water_meter.json    # Device profile for water meters
├── 03_device_profile_smart_valve.json    # Device profile for smart valves
├── 04_sample_assets.json                 # Sample field assets
├── 05_sample_devices.json                # Sample devices
├── setup_irrigation_entities.py          # Automated setup script
├── simulate_telemetry.py                 # Telemetry simulation script
└── README.md                             # This file
```

## 🔧 Manual Setup (Alternative)

If you prefer to create entities manually:

### 1. Create Device Profiles

**ThingsBoard UI → Profiles → Device Profiles → Add Device Profile**

Create three profiles using the JSON files:
- `01_device_profile_soil_moisture.json`
- `02_device_profile_water_meter.json`
- `03_device_profile_smart_valve.json`

### 2. Create Assets

**ThingsBoard UI → Entities → Assets → Add Asset**

For each field in `04_sample_assets.json`:
1. Set **Type** to "SI Field"
2. Set **Name** and **Label**
3. Go to **Attributes** tab → Add server attributes from the JSON

### 3. Create Devices

**ThingsBoard UI → Entities → Devices → Add Device**

For each device in `05_sample_devices.json`:
1. Set **Type** to device type (e.g., "SI Soil Moisture Sensor")
2. Set **Name** and **Label**
3. Select the corresponding **Device Profile**
4. Go to **Attributes** tab → Add server attributes from the JSON

### 4. Create Relations

**For each field:**
1. Go to **Assets** → Select field → **Relations** tab
2. Click **+** button
3. Select **Direction**: FROM
4. Select **Entity Type**: Device
5. Search and select the devices that belong to this field
6. Set **Relation Type**: Contains
7. Click **Add**

### 5. Send Telemetry

Use the REST API or MQTT to send telemetry data according to the data structure above.

## 📊 Dashboard Features

The dashboard includes:

### Main View (Irrigation Management)
- **Fields Table** - List of all fields with moisture levels
- **Map View** - Geographic view of fields and sensors
- **Moisture History Chart** - Time series data
- **Active Alarms** - Current alarm status

### Field Detail View
- Click on any field to see detailed information
- Individual sensor readings
- Irrigation status and tasks
- Water consumption statistics
- Scheduled irrigation events

### Sensor Detail View
- Click on any sensor to see:
  - Current moisture reading
  - Battery level
  - Historical data
  - Alarm history

## 🔍 Troubleshooting

### Dashboard shows "No data"

1. **Check if entities exist:**
   ```bash
   # Verify in ThingsBoard UI
   Entities → Assets → Filter by "SI Field"
   Entities → Devices → Filter by "SI Soil Moisture Sensor"
   ```

2. **Check if relations are created:**
   - Go to any Field asset → Relations tab
   - You should see devices listed

3. **Check if telemetry is being sent:**
   - Go to any Device → Latest telemetry tab
   - You should see moisture, battery values

4. **Verify device profiles:**
   - Profiles → Device Profiles
   - Ensure profiles are named exactly: "SI Soil Moisture Sensor", "SI Water Meter", "SI Smart Valve"

### Widgets show errors

1. **Entity aliases not resolving:**
   - Dashboard settings → Entity aliases
   - Check if filter types match your entity types exactly

2. **Attribute keys not found:**
   - Verify that entities have all required attributes
   - Check spelling matches exactly (case-sensitive)

### Script errors

1. **Login failed:**
   - Verify TB_URL, USERNAME, PASSWORD are correct
   - Ensure ThingsBoard is running

2. **Import errors:**
   - Install requests: `pip install requests`

3. **Permission denied:**
   - Ensure your user has permissions to create entities
   - Use tenant admin account

## 🎯 Customization

### Adding More Fields

Edit `04_sample_assets.json` and add more field objects, then run:
```bash
python3 setup_irrigation_entities.py
```

### Adding More Sensors

Edit `05_sample_devices.json` and add more device objects with the correct `fieldAssociation`, then run:
```bash
python3 setup_irrigation_entities.py
```

### Adjusting Thresholds

Modify the moisture thresholds in the asset/device attributes:
- `minMoistureThreshold`: When to start irrigation
- `maxMoistureThreshold`: When to stop irrigation

### Changing Telemetry Interval

Edit `simulate_telemetry.py`:
```python
INTERVAL_SECONDS = 10  # Change to desired interval
```

## 📚 Reference

### Required Telemetry Keys

**SI Soil Moisture Sensor:**
- `moisture` (float): 0-100%
- `battery` (integer): 0-100%

**SI Water Meter:**
- `pulseCounter` (integer): Cumulative water flow pulses
- `battery` (integer): 0-100%

**SI Smart Valve:**
- `battery` (integer): 0-100%

**SI Field (Asset):**
- `avgMoisture` (float): Average moisture across all sensors
- `irrigationState` (string): "IDLE" or "ACTIVE"
- `irrigationTask` (string): Current task description
- `schedulerEvents` (JSON string): Array of scheduled events
- `waterConsumption` (integer): Daily water consumption in liters

### Required Attributes

**SI Soil Moisture Sensor:**
- `active` (boolean): Sensor active status
- `latitude` (float): GPS latitude
- `longitude` (float): GPS longitude
- `maxMoistureThreshold` (integer): Max threshold
- `minMoistureThreshold` (integer): Min threshold

**SI Field (Asset):**
- `cropType` (string): Type of crop
- `perimeter` (GeoJSON): Field boundary polygon
- `maxMoistureThreshold` (integer): Max threshold
- `minMoistureThreshold` (integer): Min threshold

## 🆘 Support

If you encounter issues:

1. Check ThingsBoard logs: `/var/log/thingsboard/thingsboard.log`
2. Verify all entity types match exactly (case-sensitive)
3. Ensure relations are bidirectional (FROM field TO device)
4. Check that telemetry data types match (number vs string)

## 📝 Notes

- Entity types are case-sensitive: "SI Field", "SI Soil Moisture Sensor"
- Attribute scopes: Use SERVER_SCOPE for dashboard attributes
- Telemetry timestamps: Use milliseconds since epoch or let ThingsBoard auto-assign
- Relations: Type should be "Contains" for asset-to-device relationships

## ✅ Success Checklist

After setup, verify:
- [ ] 3 device profiles created
- [ ] 3 field assets created with attributes
- [ ] 6 devices created with attributes
- [ ] Relations established (fields contain devices)
- [ ] Initial telemetry sent to all entities
- [ ] Dashboard imported successfully
- [ ] Dashboard displays fields and sensors
- [ ] Map view shows sensor locations
- [ ] Charts show telemetry data
- [ ] Simulation script running without errors

---

**Last Updated:** 2025-12-14
**Compatible with:** ThingsBoard CE 3.x
