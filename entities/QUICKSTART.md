# 🚀 Quick Start Guide - Smart Irrigation Dashboard

## ⚡ Fast Setup (5 minutes)

### 1. Install Dependencies
```bash
cd /home/mouraop/Desktop/fertirega_backend/entities
pip install -r requirements.txt
```

### 2. Configure Connection
Edit these files and update your ThingsBoard credentials:
- `setup_irrigation_entities.py` (lines 10-12)
- `simulate_telemetry.py` (lines 10-12)
- `diagnose_dashboard.py` (lines 7-9)

```python
TB_URL = "http://localhost:8080"  # Your ThingsBoard URL
USERNAME = "tenant@thingsboard.org"  # Your username
PASSWORD = "tenant"  # Your password
```

### 3. Run Setup
```bash
python3 setup_irrigation_entities.py
```

**Expected Output:**
```
✓ Successfully logged in to ThingsBoard
✓ Created device profile: SI Soil Moisture Sensor
✓ Created device profile: SI Water Meter
✓ Created device profile: SI Smart Valve
✓ Created asset: Field A - Wheat
✓ Created asset: Field B - Corn
✓ Created asset: Field C - Vegetables
✓ Created device: Moisture Sensor A1
...
✓ Setup Complete!
```

### 4. Import Dashboard
1. Open ThingsBoard UI
2. Go to **Dashboards** → **+** → **Import dashboard**
3. Select: `/home/mouraop/Desktop/fertirega_backend/dashboard/d1c73db0-d8f8-11f0-89a2-f98bab6d1641.json`
4. Click **Import**

### 5. Start Simulation
```bash
python3 simulate_telemetry.py
```

Keep this running to continuously send data.

### 6. Open Dashboard
Navigate to **Dashboards** → **Irrigation Management**

---

## 🔍 Troubleshooting

### Problem: Dashboard shows "No data"

**Run diagnostics:**
```bash
python3 diagnose_dashboard.py
```

This will check:
- ✓ Device profiles exist
- ✓ Assets created
- ✓ Devices created
- ✓ Relations established
- ✓ Telemetry data flowing

**Common fixes:**
1. Re-run setup: `python3 setup_irrigation_entities.py`
2. Start simulation: `python3 simulate_telemetry.py`
3. Check entity types are exact: "SI Field", "SI Soil Moisture Sensor"

### Problem: Login failed

- Verify ThingsBoard is running: `http://localhost:8080`
- Check username/password are correct
- Ensure user has admin permissions

### Problem: Import errors

```bash
pip install --upgrade requests
```

---

## 📊 What You Get

### 3 Fields
- Field A - Wheat
- Field B - Corn
- Field C - Vegetables

### 6 Devices
- 4 Moisture Sensors (distributed across fields)
- 1 Water Meter
- 1 Smart Valve

### Real-time Data
- Moisture levels (updates every 10s)
- Battery status
- Irrigation state
- Water consumption

---

## 🎯 Next Steps

### Add More Fields
Edit [04_sample_assets.json](04_sample_assets.json), add more fields, then:
```bash
python3 setup_irrigation_entities.py
```

### Add More Sensors
Edit [05_sample_devices.json](05_sample_devices.json), add more sensors, then:
```bash
python3 setup_irrigation_entities.py
```

### Customize Coordinates
Update GPS coordinates in device attributes:
```json
"latitude": 37.42140,
"longitude": -122.08350
```

### Adjust Update Frequency
Edit `simulate_telemetry.py`:
```python
INTERVAL_SECONDS = 10  # Change to 30, 60, etc.
```

---

## 📚 Full Documentation

See [README.md](README.md) for complete documentation including:
- Manual setup instructions
- Data structure details
- API reference
- Advanced customization

---

## ✅ Verification Checklist

After setup, you should see:
- [ ] 3 Device Profiles in ThingsBoard
- [ ] 3 Field Assets
- [ ] 6 Devices
- [ ] Relations: Fields → Devices
- [ ] Dashboard imported
- [ ] Dashboard shows fields on map
- [ ] Charts display moisture data
- [ ] Simulation running without errors

---

**Setup Time:** ~5 minutes
**Compatible with:** ThingsBoard CE 3.x
**Last Updated:** 2025-12-14
