# FertiRega Backend - ThingsBoard Configuration

IoT irrigation management system using ThingsBoard CE, ChirpStack, and LoRaWAN devices.

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

## 🚀 Quick Start

### Prerequisites

- ThingsBoard CE (Community Edition)
- ChirpStack server running at `http://100.92.66.20`
- ChirpStack API key
- LoRaWAN devices with FertiRega firmware

### Installation

1. **Import Widget Bundle**:
   ```
   ThingsBoard → Widget Library → + → Import widget bundle
   Select: widgets_bundle/fertirega_widgets_bundle.json
   ```

2. **Configure ChirpStack API Key**:
   - Edit each valve control widget in the widget library
   - Replace `YOUR_API_KEY_HERE` with your actual ChirpStack API token

3. **Import Dashboards**:
   ```
   ThingsBoard → Dashboards → + → Import dashboard
   Import: dashboard_new/31b6ecf1-*.json (Overview)
   Import: dashboard_new/58351f95-*.json (Device Details)
   ```

4. **Import Alarm Rule Chain**:
   ```
   ThingsBoard → Rule Chains → + → Import rule chain
   Select: rule_chain/da36c158-*.json
   ```

5. **Assign Rule Chain**:
   ```
   ThingsBoard → Device Profiles → FertiRega LoRa Sensor → Edit
   Set Rule Chain: FertiRega Alarms and Logging
   ```

📖 **See [FERTIREGA_DASHBOARD_SETUP.md](FERTIREGA_DASHBOARD_SETUP.md) for detailed instructions**

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

## 🐛 Troubleshooting

**Widgets not appearing?**
- Verify widget bundle is imported
- Check widget type alias: `fertirega_widgets`

**Valve control not working?**
- Configure ChirpStack API key in widgets
- Verify ChirpStack server is accessible
- Check device EUI resolution (use `eui-{id}` naming)

**Alarms not triggering?**
- Assign rule chain to device profile
- Enable debug mode on rule chain
- Verify telemetry is being received

See [FERTIREGA_DASHBOARD_SETUP.md](FERTIREGA_DASHBOARD_SETUP.md) for detailed troubleshooting.

## 📝 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This repository tracks ThingsBoard entity configurations for the FertiRega project. To contribute:

1. Make changes in ThingsBoard UI
2. Export entities (Manual or via REST API)
3. Update JSON files in this repo
4. Commit and push changes

## 📞 Support

For issues or questions about:
- Dashboard functionality
- Widget customization
- Alarm configuration
- ChirpStack integration

Refer to the comprehensive setup guide: [FERTIREGA_DASHBOARD_SETUP.md](FERTIREGA_DASHBOARD_SETUP.md)

---

**Version**: 2.0 (Complete Dashboard Rebuild)
**Last Updated**: 2025-11-29
**ThingsBoard**: Community Edition
**LoRaWAN Network**: ChirpStack
