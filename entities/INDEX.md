# 📁 Smart Irrigation Dashboard - File Index

## 🎯 Start Here

If you're new to this setup, start with these files in order:

1. **[SETUP_SUMMARY.md](../SETUP_SUMMARY.md)** - Overview of the complete solution
2. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start guide
3. **[README.md](README.md)** - Complete documentation

## 📚 Documentation Files

| File | Purpose | When to Use |
|------|---------|-------------|
| [SETUP_SUMMARY.md](../SETUP_SUMMARY.md) | High-level overview | First read - understand what you're getting |
| [QUICKSTART.md](QUICKSTART.md) | Quick setup guide | When you want to get started fast (5 min) |
| [README.md](README.md) | Complete guide | Full documentation with troubleshooting |
| [STRUCTURE.md](STRUCTURE.md) | Entity structure reference | Understand the data model and hierarchy |
| [INDEX.md](INDEX.md) | This file | Find the right file for your needs |

## 🔧 Configuration Files

| File | Type | Purpose |
|------|------|---------|
| [01_device_profile_soil_moisture.json](01_device_profile_soil_moisture.json) | JSON | Moisture sensor device profile |
| [02_device_profile_water_meter.json](02_device_profile_water_meter.json) | JSON | Water meter device profile |
| [03_device_profile_smart_valve.json](03_device_profile_smart_valve.json) | JSON | Smart valve device profile |
| [04_sample_assets.json](04_sample_assets.json) | JSON | Sample field assets (3 fields) |
| [05_sample_devices.json](05_sample_devices.json) | JSON | Sample devices (4 sensors + meter + valve) |

## 🐍 Python Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [setup_irrigation_entities.py](setup_irrigation_entities.py) | Create all entities | `python3 setup_irrigation_entities.py` |
| [simulate_telemetry.py](simulate_telemetry.py) | Continuous telemetry | `python3 simulate_telemetry.py` |
| [diagnose_dashboard.py](diagnose_dashboard.py) | Health check | `python3 diagnose_dashboard.py` |

## 🎓 Learning Path

### Beginner - Just Getting Started
1. Read [SETUP_SUMMARY.md](../SETUP_SUMMARY.md)
2. Follow [QUICKSTART.md](QUICKSTART.md)
3. Run `setup_irrigation_entities.py`
4. Import dashboard
5. Run `simulate_telemetry.py`

### Intermediate - Customization
1. Review [STRUCTURE.md](STRUCTURE.md) to understand the data model
2. Edit [04_sample_assets.json](04_sample_assets.json) to add/modify fields
3. Edit [05_sample_devices.json](05_sample_devices.json) to add/modify devices
4. Re-run `setup_irrigation_entities.py`

### Advanced - Troubleshooting
1. Run `diagnose_dashboard.py` to identify issues
2. Review [README.md](README.md) troubleshooting section
3. Check entity types, attributes, and relations
4. Verify telemetry data types and scopes

## 🔍 Quick Reference

### I want to...

**...get started quickly**
→ [QUICKSTART.md](QUICKSTART.md)

**...understand the system architecture**
→ [STRUCTURE.md](STRUCTURE.md)

**...add more fields**
→ Edit [04_sample_assets.json](04_sample_assets.json), then run `setup_irrigation_entities.py`

**...add more sensors**
→ Edit [05_sample_devices.json](05_sample_devices.json), then run `setup_irrigation_entities.py`

**...troubleshoot issues**
→ Run `diagnose_dashboard.py`, then check [README.md](README.md) troubleshooting

**...change GPS coordinates**
→ Edit latitude/longitude in [04_sample_assets.json](04_sample_assets.json) and [05_sample_devices.json](05_sample_devices.json)

**...modify device profiles**
→ Edit the 01-03 JSON files, then manually update in ThingsBoard UI

**...understand data requirements**
→ [STRUCTURE.md](STRUCTURE.md) - See "Entity Breakdown" section

**...check if everything is working**
→ Run `diagnose_dashboard.py`

**...send test data**
→ Run `simulate_telemetry.py`

## 📊 File Dependencies

```
setup_irrigation_entities.py
  ├── requires: 01_device_profile_soil_moisture.json
  ├── requires: 02_device_profile_water_meter.json
  ├── requires: 03_device_profile_smart_valve.json
  ├── requires: 04_sample_assets.json
  └── requires: 05_sample_devices.json

simulate_telemetry.py
  └── requires: Entities created by setup_irrigation_entities.py

diagnose_dashboard.py
  └── requires: ThingsBoard connection (entities optional)
```

## 🎯 File Sizes

| File | Size | Type |
|------|------|------|
| 01_device_profile_soil_moisture.json | 1.8K | Config |
| 02_device_profile_water_meter.json | 1.8K | Config |
| 03_device_profile_smart_valve.json | 1.8K | Config |
| 04_sample_assets.json | 2.1K | Data |
| 05_sample_devices.json | 3.1K | Data |
| setup_irrigation_entities.py | 12K | Script |
| simulate_telemetry.py | 11K | Script |
| diagnose_dashboard.py | 13K | Script |
| requirements.txt | 17B | Config |
| README.md | 11K | Docs |
| QUICKSTART.md | 3.6K | Docs |
| STRUCTURE.md | 32K | Docs |
| SETUP_SUMMARY.md | ~12K | Docs |

**Total:** ~94K of configuration, scripts, and documentation

## 💡 Tips

### First Time Setup
1. Don't skip the [SETUP_SUMMARY.md](../SETUP_SUMMARY.md) - it explains the big picture
2. Use [QUICKSTART.md](QUICKSTART.md) for rapid deployment
3. Run `diagnose_dashboard.py` after setup to verify

### Customization
1. Always edit JSON files before running scripts
2. GPS coordinates are in decimal format (e.g., 37.4219, -122.084)
3. Entity type names are case-sensitive
4. Keep field associations in sync when editing

### Troubleshooting
1. Run diagnostics first: `python3 diagnose_dashboard.py`
2. Check ThingsBoard logs: `/var/log/thingsboard/thingsboard.log`
3. Verify entity types match exactly (case-sensitive)
4. Ensure relations are bidirectional

### Production Deployment
1. Update GPS coordinates to real locations
2. Adjust moisture thresholds per crop type
3. Configure proper alarm recipients
4. Set up rule chains for automated irrigation
5. Implement proper device provisioning

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| "No data" in dashboard | Run `simulate_telemetry.py` |
| Login failed | Check credentials in script configs |
| Entity not found | Re-run `setup_irrigation_entities.py` |
| Wrong coordinates | Edit JSON files and re-run setup |
| Dashboard not found | Import the dashboard JSON manually |
| Alarms not showing | Check device profiles have alarms configured |

## ✅ Validation Commands

Check if everything is set up correctly:

```bash
# 1. Verify files exist
ls -lh *.json *.py *.md

# 2. Check Python dependencies
pip list | grep requests

# 3. Test ThingsBoard connection
python3 diagnose_dashboard.py

# 4. View what will be created
cat 04_sample_assets.json | python3 -m json.tool
cat 05_sample_devices.json | python3 -m json.tool
```

## 🔗 External Resources

- **Dashboard JSON**: `/home/mouraop/Desktop/fertirega_backend/dashboard/d1c73db0-d8f8-11f0-89a2-f98bab6d1641.json`
- **ThingsBoard Docs**: https://thingsboard.io/docs/
- **Smart Irrigation Template**: https://thingsboard.io/docs/pe/solution-templates/smart-irrigation/
- **REST API Docs**: https://thingsboard.io/docs/api/

## 📝 Notes

- All entity types are case-sensitive
- Attribute scope must be SERVER_SCOPE for dashboard visibility
- Relations must be bidirectional (FROM and TO)
- Telemetry timestamps can be auto-assigned by ThingsBoard
- Device profiles can only be created via API or UI (not bulk import)

---

**Last Updated:** 2025-12-14
**Version:** 1.0
**Purpose:** Navigation guide for Smart Irrigation setup files
