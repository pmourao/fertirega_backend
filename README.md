# FertiRega Backend - ThingsBoard Configuration

IoT irrigation management system using ThingsBoard CE, ChirpStack, and LoRaWAN devices.

## 🚀 Quick Start

**⭐ NEW USER? START HERE**: [THINGSBOARD_CE_IMPORT_INSTRUCTIONS.md](THINGSBOARD_CE_IMPORT_INSTRUCTIONS.md)

**❌ HAD WIDGET IMPORT ERRORS?** See: [WIDGET_IMPORT_SOLUTION.md](WIDGET_IMPORT_SOLUTION.md)

**📋 Quick Reference**: [QUICK_START.md](QUICK_START.md)

---

## 🌟 Features

- **Real-time Monitoring**: Temperature, humidity, battery levels
- **Valve Control**: Remote control of 2 irrigation valves per device via ChirpStack
- **Geolocation**: Device tracking on Google Maps
- **Alarms**: Low battery (<20%) and offline detection (>3h)
- **Scheduling**: Time-based valve automation (customizable)
- **Logging**: Automatic valve status change history

## 📁 Repository Structure

```
fertirega_backend/
├── widgets_bundle/              # Custom ThingsBoard widgets
│   └── fertirega_widgets_bundle.json
├── dashboard/                   # Old/backup dashboards
├── dashboard_new/               # NEW FertiRega dashboards ⭐
│   ├── 31b6ecf1-...json        # Overview Dashboard
│   └── 58351f95-...json        # Device Details Dashboard
├── device/                      # Device configurations
├── device_profile/              # Device profiles (FertiRega LoRa Sensor)
├── rule_chain/                  # Rule chains including alarms
│   └── da36c158-...json        # FertiRega Alarms & Logging ⭐
├── converter/                   # Uplink/downlink data converters
├── integration/                 # TTN/ChirpStack integrations
├── customer/                    # Customer configurations
├── asset_profile/               # Asset profiles
├── notification_*/              # Notification rules, targets, templates
└── FERTIREGA_DASHBOARD_SETUP.md # Complete setup guide ⭐
```

## 📦 What's Included

### Widgets (5 Custom Widgets)
- **Valve 0 Control** - Toggle switch for irrigation valve 0
- **Valve 1 Control** - Toggle switch for irrigation valve 1
- **Device Attributes** - Info panel showing location, battery, temp, humidity
- **Time Picker** - Scheduling interface for valve automation
- **Reset Clock** - Device clock synchronization

### Dashboards (2 Dashboards)
- **FertiRega Overview** - Map view with all devices, device table, alarms
- **FertiRega Device Details** - Single device view with controls and charts

### Rule Chain
- **FertiRega Alarms & Logging** - Battery low, offline detection, valve logging

---

## ⚡ Installation (15 Minutes)

### IMPORTANT: ThingsBoard CE Import Process

**ThingsBoard CE does NOT support widget bundle import** (Professional Edition only).

**You must**:
1. Create widget bundle manually in UI
2. Import individual widgets one by one

### Step-by-Step

1. **Create Widget Bundle** (1 min):
   ```
   ThingsBoard → Widget Library → + → Create new widgets bundle
   Title: FertiRega Widgets
   ```

2. **Import 5 Widgets** (5 min):
   ```
   Widget Library → FertiRega Widgets → + → Import widget type

   Import these files one by one:
   - widgets_bundle/fertirega_valvecontrol_0.json
   - widgets_bundle/fertirega_valvecontrol_1.json
   - widgets_bundle/fertirega_deviceattributes.json
   - widgets_bundle/fertirega_timepicker.json
   - widgets_bundle/fertirega_resetclock.json
   ```

3. **Configure ChirpStack API Key** (5 min):
   - Edit each valve control widget in the widget library
   - Replace `YOUR_API_KEY_HERE` with your actual ChirpStack API token
   - Widgets to update: valvecontrol_0, valvecontrol_1, timepicker, resetclock

4. **Import Dashboards** (2 min):
   ```
   ThingsBoard → Dashboards → + → Import dashboard
   Import: dashboard_new/31b6ecf1-*.json (Overview)
   Import: dashboard_new/58351f95-*.json (Device Details)
   ```

5. **Import Alarm Rule Chain** (2 min):
   ```
   ThingsBoard → Rule Chains → + → Import rule chain
   Select: rule_chain/da36c158-*.json
   ```

6. **Assign Rule Chain** (1 min):
   ```
   ThingsBoard → Device Profiles → FertiRega LoRa Sensor → Edit
   Set Rule Chain: FertiRega Alarms and Logging
   ```

📖 **Complete Guide**: [THINGSBOARD_CE_IMPORT_INSTRUCTIONS.md](THINGSBOARD_CE_IMPORT_INSTRUCTIONS.md)

---

## 🎯 Dashboard Overview

### FertiRega Overview Dashboard
- Google Maps with all devices
- Active devices table
- Active alarms monitor
- Click device → Navigate to details

### FertiRega Device Details Dashboard
- Device information panel
- Valve 0 & 1 toggle controls
- Battery level gauge
- Temperature & humidity charts
- Valve status history
- Scheduling interface

## 🔧 Device Configuration

### Telemetry Keys

| Key | Type | Description |
|-----|------|-------------|
| `temperature` | Timeseries | Temperature in °C |
| `humidity` | Timeseries | Humidity in % |
| `battery_percentage` | Timeseries | Battery level (0-100%) |
| `valve_0_status` | Timeseries | Valve 0 status (0=closed, 1=open) |
| `valve_1_status` | Timeseries | Valve 1 status (0=closed, 1=open) |

### Attribute Keys

| Key | Type | Description |
|-----|------|-------------|
| `Server_Lat` | Server | Device latitude |
| `Server_Lon` | Server | Device longitude |
| `Device_Name` | Server | Device display name |
| `active` | Server | Device active status |

## 🔔 Alarms

| Alarm Type | Severity | Condition |
|------------|----------|-----------|
| Low Battery | WARNING | `battery_percentage < 20%` |
| Device Offline | CRITICAL | No activity for > 3 hours |

## 📡 ChirpStack Integration

### Valve Control Commands

Commands are sent via ChirpStack HTTP API:

```bash
POST http://100.92.66.20:8080/api/devices/{devEui}/queue
Content-Type: application/json
Grpc-Metadata-Authorization: Bearer YOUR_API_KEY

{
  "queueItem": {
    "confirmed": true,
    "data": "<base64_payload>",
    "fPort": 2
  }
}
```

**Payload Format**:
- Byte 0: Valve number (0 or 1)
- Byte 1: Action (0 = close, 1 = open)

**Example**: Open Valve 0 → Bytes `[0, 1]` → Base64 `AAE=`

### fPort Mapping

| fPort | Purpose |
|-------|---------|
| 1 | Uplink telemetry (sensors) |
| 2 | Valve control commands |
| 3 | Scheduling commands (customizable) |
| 4 | Clock synchronization |

## 🛠️ Customization

### Update Scheduling Protocol

The `fertirega_timepicker` widget uses a placeholder scheduling format. To customize:

1. Edit the widget in Widget Library
2. Update the JavaScript encoding logic
3. Match your device's expected payload format

### Adjust Alarm Thresholds

Edit the rule chain (`da36c158-*.json`) to change:
- Battery low threshold (default: 20%)
- Inactivity timeout (default: 3 hours)

## 📊 Data Flow

```
LoRa Device → ChirpStack → TTN Integration → ThingsBoard
    ↓
Converters (Uplink/Downlink)
    ↓
Rule Chain (Alarms & Logging)
    ↓
Dashboard Widgets
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[THINGSBOARD_CE_IMPORT_INSTRUCTIONS.md](THINGSBOARD_CE_IMPORT_INSTRUCTIONS.md)** | ⭐ **START HERE** - Complete step-by-step import guide |
| **[WIDGET_IMPORT_SOLUTION.md](WIDGET_IMPORT_SOLUTION.md)** | Solution for widget import errors in ThingsBoard CE |
| **[QUICK_START.md](QUICK_START.md)** | Quick reference checklist for setup |
| **[FERTIREGA_DASHBOARD_SETUP.md](FERTIREGA_DASHBOARD_SETUP.md)** | Detailed dashboard usage and configuration |
| **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** | Technical architecture and delivery report |
| **[WIDGET_CREATION_GUIDE.md](WIDGET_CREATION_GUIDE.md)** | Manual widget creation (alternative to import) |

---

## 🐛 Troubleshooting

**Cannot import widget bundle?**
- ThingsBoard CE doesn't support bundle import
- Use individual widget import method
- See: [WIDGET_IMPORT_SOLUTION.md](WIDGET_IMPORT_SOLUTION.md)

**Widgets not appearing?**
- Create bundle manually first
- Import widgets one by one
- Verify bundle alias: `fertirega_widgets`

**Valve control not working?**
- Configure ChirpStack API key in widgets (replace `YOUR_API_KEY_HERE`)
- Verify ChirpStack server is accessible at `http://100.92.66.20:8080`
- Check device EUI resolution (use `eui-{deviceEui}` naming convention)

**Alarms not triggering?**
- Assign rule chain to device profile
- Enable debug mode on rule chain
- Verify telemetry is being received

📖 **Complete Troubleshooting**: [THINGSBOARD_CE_IMPORT_INSTRUCTIONS.md](THINGSBOARD_CE_IMPORT_INSTRUCTIONS.md)

## 📝 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This repository tracks ThingsBoard entity configurations for the FertiRega project. To contribute:

1. Make changes in ThingsBoard UI
2. Export entities (Manual or via REST API)
3. Update JSON files in this repo
4. Commit and push changes

## 📞 Support

For issues or questions, consult the documentation:

- **Import Problems**: [WIDGET_IMPORT_SOLUTION.md](WIDGET_IMPORT_SOLUTION.md)
- **Setup Guide**: [THINGSBOARD_CE_IMPORT_INSTRUCTIONS.md](THINGSBOARD_CE_IMPORT_INSTRUCTIONS.md)
- **Dashboard Usage**: [FERTIREGA_DASHBOARD_SETUP.md](FERTIREGA_DASHBOARD_SETUP.md)
- **Technical Details**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

---

**Version**: 2.0 (Complete Dashboard Rebuild)
**Last Updated**: 2025-11-29
**ThingsBoard**: Community Edition
**LoRaWAN Network**: ChirpStack
