# Smart Irrigation Dashboard - Setup Summary

## 📦 What Was Created

I've analyzed your Smart Irrigation dashboard and created a complete setup package to make it work properly in ThingsBoard Community Edition.

### 📂 Location
```
/home/mouraop/Desktop/fertirega_backend/entities/
```

### 📄 Files Created

#### 1. **Device Profile Definitions** (JSON)
- `01_device_profile_soil_moisture.json` - Moisture sensor profile with low battery alarm
- `02_device_profile_water_meter.json` - Water meter profile with low battery alarm
- `03_device_profile_smart_valve.json` - Smart valve profile with low battery alarm

#### 2. **Sample Entity Data** (JSON)
- `04_sample_assets.json` - 3 sample fields (Wheat, Corn, Vegetables)
- `05_sample_devices.json` - 6 sample devices (4 sensors, 1 meter, 1 valve)

#### 3. **Automation Scripts** (Python)
- `setup_irrigation_entities.py` - Automated entity creation script
- `simulate_telemetry.py` - Real-time telemetry simulation
- `diagnose_dashboard.py` - Dashboard health check tool

#### 4. **Documentation**
- `README.md` - Complete setup guide with troubleshooting
- `QUICKSTART.md` - 5-minute quick start guide
- `requirements.txt` - Python dependencies

---

## 🎯 Dashboard Requirements (from Analysis)

### Entity Types Required

#### **SI Field (Asset)**
**Attributes:**
- `cropType` - Type of crop (e.g., "Wheat", "Corn")
- `perimeter` - GeoJSON polygon for field boundaries
- `maxMoistureThreshold` - Maximum moisture level (0-100)
- `minMoistureThreshold` - Minimum moisture level (0-100)
- `criticalAlarmsCount` - Count of critical alarms
- `majorAlarmsCount` - Count of major alarms

**Telemetry:**
- `avgMoisture` - Average moisture across all sensors
- `irrigationState` - Current state ("IDLE" or "ACTIVE")
- `irrigationTask` - Current irrigation task description
- `schedulerEvents` - JSON array of scheduled events
- `waterConsumption` - Daily water consumption (liters)

#### **SI Soil Moisture Sensor (Device)**
**Attributes:**
- `active` - Sensor active status (boolean)
- `latitude` - GPS latitude coordinate
- `longitude` - GPS longitude coordinate
- `maxMoistureThreshold` - Maximum threshold
- `minMoistureThreshold` - Minimum threshold

**Telemetry:**
- `moisture` - Current moisture reading (0-100%)
- `battery` - Battery level (0-100%)

#### **SI Water Meter (Device)**
**Telemetry:**
- `pulseCounter` - Cumulative water flow pulses
- `battery` - Battery level (0-100%)

#### **SI Smart Valve (Device)**
**Telemetry:**
- `battery` - Battery level (0-100%)

### Relations Required
- **Asset → Device**: Each field must have "Contains" relations to its devices
- **Direction**: FROM field TO devices
- **Relation Type**: "Contains"

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
cd /home/mouraop/Desktop/fertirega_backend/entities
pip install -r requirements.txt
```

### Step 2: Configure & Run Setup
Edit `setup_irrigation_entities.py` (lines 10-12) with your ThingsBoard credentials:
```python
TB_URL = "http://localhost:8080"
USERNAME = "tenant@thingsboard.org"
PASSWORD = "tenant"
```

Then run:
```bash
python3 setup_irrigation_entities.py
```

### Step 3: Import Dashboard & Start Simulation
1. Import the dashboard JSON via ThingsBoard UI
2. Run: `python3 simulate_telemetry.py`
3. Open the dashboard

---

## 📊 What Gets Created

### Device Profiles (3)
- SI Soil Moisture Sensor
- SI Water Meter
- SI Smart Valve

All with low battery alarms (<30% triggers CRITICAL alarm)

### Assets (3 Fields)
1. **Field A - Wheat**
   - Min/Max Moisture: 40-80%
   - 2 moisture sensors
   - 1 water meter
   - 1 smart valve

2. **Field B - Corn**
   - Min/Max Moisture: 45-75%
   - 1 moisture sensor

3. **Field C - Vegetables**
   - Min/Max Moisture: 50-85%
   - 1 moisture sensor

### Devices (6)
- 4 × Moisture Sensors (distributed across fields)
- 1 × Water Meter (Field A)
- 1 × Smart Valve (Field A)

### Relations
- All devices properly linked to their parent fields
- Bidirectional "Contains" relationships

### Initial Telemetry
- All devices receive initial telemetry data
- All fields receive calculated metrics
- Dashboard immediately shows data

---

## 🔧 Utility Scripts

### Diagnostics Tool
```bash
python3 diagnose_dashboard.py
```

Checks:
- ✓ Device profiles exist
- ✓ Assets created with proper attributes
- ✓ Devices created with proper attributes
- ✓ Relations established
- ✓ Telemetry data present
- ✓ Dashboard imported

### Telemetry Simulator
```bash
python3 simulate_telemetry.py
```

Features:
- Sends data every 10 seconds (configurable)
- Realistic moisture trends with random walk
- Simulates irrigation events
- Calculates field averages automatically
- Updates irrigation states based on thresholds
- Runs until Ctrl+C

---

## 📋 Dashboard Features Supported

### Main View
- ✅ Fields table with moisture levels
- ✅ Map view with field polygons
- ✅ Map view with sensor locations
- ✅ Moisture history charts
- ✅ Active alarms widget

### Field Detail View
- ✅ Field information card
- ✅ Average moisture gauge
- ✅ Irrigation state display
- ✅ List of sensors in field
- ✅ Sensor locations on map
- ✅ Historical moisture charts
- ✅ Water consumption data

### Sensor Detail View
- ✅ Sensor information card
- ✅ Current moisture reading
- ✅ Battery level
- ✅ Sensor location on map
- ✅ Historical data charts
- ✅ Alarm history

---

## 🎨 Customization Options

### Add More Fields
1. Edit `04_sample_assets.json`
2. Add new field objects with attributes
3. Run `python3 setup_irrigation_entities.py`

### Add More Sensors
1. Edit `05_sample_devices.json`
2. Add new device objects
3. Set `fieldAssociation` to link to a field
4. Run `python3 setup_irrigation_entities.py`

### Change GPS Coordinates
Update latitude/longitude in:
- Asset `perimeter` (field polygon)
- Device `latitude`/`longitude` attributes

### Adjust Moisture Thresholds
Modify in asset/device attributes:
- `minMoistureThreshold` - When to start irrigation
- `maxMoistureThreshold` - When to stop irrigation

### Change Update Frequency
Edit `simulate_telemetry.py`:
```python
INTERVAL_SECONDS = 10  # Change to 30, 60, etc.
```

---

## ⚠️ Important Notes

### Entity Type Names (Case-Sensitive!)
- **Asset Type**: Must be exactly "SI Field"
- **Device Types**: Must be exactly:
  - "SI Soil Moisture Sensor"
  - "SI Water Meter"
  - "SI Smart Valve"

### Attribute Scopes
- Use **SERVER_SCOPE** for all attributes used in dashboard
- Client attributes won't be visible to dashboard widgets

### Telemetry Data Types
- Moisture values: **float** (0-100)
- Battery values: **integer** (0-100)
- Pulse counter: **integer**
- States: **string** ("IDLE", "ACTIVE")

### Relations
- Must be bidirectional (FROM field TO device)
- Relation type must be "Contains"
- Dashboard uses both FROM and TO queries

---

## 🐛 Troubleshooting

### Dashboard Shows "No Data"

**Run diagnostics:**
```bash
python3 diagnose_dashboard.py
```

**Quick fixes:**
1. Verify entity types match exactly (case-sensitive)
2. Check relations exist (Assets → Devices)
3. Ensure telemetry is being sent
4. Verify attribute names match exactly

### Widgets Show Errors

**Check:**
- Entity aliases in dashboard match entity types
- All required attributes exist
- Telemetry keys match exactly
- Relations are properly configured

### Simulation Errors

**Solutions:**
- Verify ThingsBoard is running
- Check credentials are correct
- Ensure devices were created successfully
- Install dependencies: `pip install requests`

---

## 📚 Reference Links

### ThingsBoard Docs
- [Smart Irrigation Template](https://thingsboard.io/docs/pe/solution-templates/smart-irrigation/)
- [Device Profiles](https://thingsboard.io/docs/user-guide/device-profiles/)
- [Entity Relations](https://thingsboard.io/docs/user-guide/entities-and-relations/)
- [Telemetry API](https://thingsboard.io/docs/user-guide/telemetry/)

### Created Files
- Full Guide: [entities/README.md](entities/README.md)
- Quick Start: [entities/QUICKSTART.md](entities/QUICKSTART.md)
- Setup Script: [entities/setup_irrigation_entities.py](entities/setup_irrigation_entities.py)
- Simulator: [entities/simulate_telemetry.py](entities/simulate_telemetry.py)
- Diagnostics: [entities/diagnose_dashboard.py](entities/diagnose_dashboard.py)

---

## ✅ Success Criteria

After setup, you should have:
- [x] 3 device profiles created in ThingsBoard
- [x] 3 field assets with all required attributes
- [x] 6 devices with all required attributes
- [x] Relations established (fields contain devices)
- [x] Initial telemetry sent to all entities
- [x] Dashboard imported and accessible
- [x] Dashboard displays fields on map
- [x] Dashboard shows sensor locations
- [x] Charts display telemetry data
- [x] Simulation running continuously

---

## 🎯 Next Steps

1. **Run the setup script** to create all entities
2. **Import the dashboard** JSON file
3. **Start the simulator** to send continuous data
4. **Open the dashboard** and verify everything works
5. **Customize** fields, sensors, and coordinates to match your needs

---

**Created:** 2025-12-14
**Compatible with:** ThingsBoard CE 3.x
**Status:** Ready to deploy ✅
