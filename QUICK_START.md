# FertiRega Dashboard - Quick Start Guide

## ⚡ 5-Minute Setup

### Prerequisites
- ThingsBoard CE running
- ChirpStack API key ready
- Git repository cloned

### Import Checklist

#### ☑️ Step 1: Widget Bundle (2 min)
```
ThingsBoard → Widget Library → + → Import widget bundle
📁 File: widgets_bundle/fertirega_widgets_bundle.json
```

#### ☑️ Step 2: Configure API Key (1 min)
```
Widget Library → FertiRega Widgets → Edit each widget:
- fertirega_valvecontrol_0
- fertirega_valvecontrol_1
- fertirega_timepicker
- fertirega_resetclock

Find: 'Grpc-Metadata-Authorization': 'Bearer YOUR_API_KEY_HERE'
Replace: YOUR_API_KEY_HERE with ChirpStack token
```

**Get ChirpStack API Key**:
1. Login: `http://100.92.66.20`
2. API Keys → Create
3. Copy token

#### ☑️ Step 3: Import Dashboards (1 min)
```
ThingsBoard → Dashboards → + → Import dashboard

1️⃣ dashboard_new/31b6ecf1-ee78-405e-afed-4a0adaa71b6d.json
   Name: FertiRega Overview

2️⃣ dashboard_new/58351f95-46c3-4346-9c89-dcbc876ed726.json
   Name: FertiRega Device Details
```

#### ☑️ Step 4: Import Alarm Rule Chain (1 min)
```
ThingsBoard → Rule Chains → + → Import rule chain
📁 File: rule_chain/da36c158-c659-4aa0-9128-db7ca02dc2c9.json
```

#### ☑️ Step 5: Assign Rule Chain (30 sec)
```
Device Profiles → FertiRega LoRa Sensor → Edit
Rule Chain: FertiRega Alarms and Logging
Save
```

---

## 🎯 Quick Test

### Test Valve Control
1. Open "FertiRega Overview" dashboard
2. Click on a device (map or table)
3. Toggle Valve 0 or Valve 1 switch
4. Check browser console for HTTP request
5. Verify command appears in ChirpStack device queue

### Test Alarms
1. Send test telemetry: `{"battery_percentage": 15}`
2. Wait 30 seconds
3. Check "Active Alarms" widget
4. Should see "Low Battery" alarm

---

## 📂 File Locations

| Component | File |
|-----------|------|
| Widget Bundle | `widgets_bundle/fertirega_widgets_bundle.json` |
| Overview Dashboard | `dashboard_new/31b6ecf1-*.json` |
| Details Dashboard | `dashboard_new/58351f95-*.json` |
| Alarm Rule Chain | `rule_chain/da36c158-*.json` |
| Setup Guide | `FERTIREGA_DASHBOARD_SETUP.md` |
| Implementation Summary | `IMPLEMENTATION_SUMMARY.md` |

---

## 🆘 Troubleshooting

### Widgets not showing?
→ Re-import widget bundle, check alias: `fertirega_widgets`

### Valve control not working?
→ Check ChirpStack API key configuration in widgets

### Navigation broken?
→ Edit dashboard, update navigation action target IDs

### Alarms not appearing?
→ Verify rule chain assigned to device profile

---

## 📖 Full Documentation

See **FERTIREGA_DASHBOARD_SETUP.md** for:
- Detailed import instructions
- ChirpStack configuration
- Dashboard usage guide
- Complete troubleshooting
- Customization options

---

## 🔑 Key Information

**ChirpStack Server**: `http://100.92.66.20:8080`
**Valve Command Port**: fPort 2
**Scheduling Port**: fPort 3 (customize widget)
**Clock Sync Port**: fPort 4

**Alarms**:
- Low Battery: < 20%
- Offline: > 3 hours

**Device Naming**: `eui-{deviceEui}` (recommended)

---

## ✅ Completion Checklist

- [ ] Widget bundle imported
- [ ] ChirpStack API key configured (4 widgets)
- [ ] Both dashboards imported
- [ ] Alarm rule chain imported
- [ ] Rule chain assigned to device profile
- [ ] Tested valve control on 1 device
- [ ] Verified alarm creation works
- [ ] Navigation between dashboards works

**Once all checked → You're ready to go!** 🚀

---

Need help? See:
- `FERTIREGA_DASHBOARD_SETUP.md` - Complete guide
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `README.md` - Project overview
