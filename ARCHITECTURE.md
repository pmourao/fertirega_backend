# FertiRega System Architecture

## 🏗️ System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FERTIREGA IOT SYSTEM                        │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌─────────────────┐
│              │  LoRa   │              │  MQTT   │                 │
│ LoRa Devices │────────▶│  ChirpStack  │────────▶│  ThingsBoard CE │
│              │         │              │         │                 │
└──────────────┘         └──────────────┘         └─────────────────┘
  • Valve 0/1               • Gateway              • Dashboards
  • Temp/Hum                • Uplink/Downlink      • Widgets
  • Battery                 • Device Queue         • Rule Chains
                            • API Server           • Alarms
```

## 📊 Data Flow

### Uplink (Device → ThingsBoard)

```
LoRa Device
    │
    │ [LoRa Packet]
    ▼
ChirpStack Gateway
    │
    │ [Decoded Payload]
    ▼
ChirpStack Network Server
    │
    │ [MQTT Publish]
    ▼
ThingsBoard Integration
    │
    │ [Uplink Converter]
    ▼
ThingsBoard Telemetry DB
    │
    │ [Rule Chain Processing]
    ▼
┌───────────────┬──────────────┬──────────────┐
│ Alarms        │ Dashboards   │ Logging      │
└───────────────┴──────────────┴──────────────┘
```

### Downlink (ThingsBoard → Device)

```
User clicks valve switch in dashboard
    │
    │ [Widget JavaScript]
    ▼
HTTP POST to ChirpStack API
    │ http://100.92.66.20:8080/api/devices/{eui}/queue
    │ Headers: Grpc-Metadata-Authorization: Bearer <API_KEY>
    │ Body: {"queueItem": {"data": "AAE=", "fPort": 2}}
    ▼
ChirpStack Network Server
    │
    │ [Queue Downlink]
    ▼
ChirpStack Gateway
    │
    │ [LoRa Transmission]
    ▼
LoRa Device
    │
    │ [Decode & Execute]
    ▼
Valve 0/1 Opens/Closes
    │
    │ [Confirmation Uplink]
    ▼
ThingsBoard (Status Update)
```

## 🎨 Dashboard Architecture

### Overview Dashboard

```
┌────────────────────────────────────────────────────────────┐
│ FERTIREGA OVERVIEW                                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌─────────────────────────┐  ┌─────────────────────┐    │
│  │                         │  │  Active Devices      │    │
│  │   Google Maps           │  │  ┌─────────────────┐│    │
│  │                         │  │  │ Device 1  🟢    ││    │
│  │   📍 Device 1 (Green)   │  │  │ Device 2  🟢    ││    │
│  │   📍 Device 2 (Green)   │  │  │ Device 3  🔴    ││    │
│  │   📍 Device 3 (Red)     │  │  └─────────────────┘│    │
│  │                         │  └─────────────────────┘    │
│  │  [Click marker →        │  ┌─────────────────────┐    │
│  │   Navigate to details]  │  │  Active Alarms       │    │
│  │                         │  │  ⚠️ Low Battery     │    │
│  └─────────────────────────┘  │  🔴 Device Offline  │    │
│                                └─────────────────────┘    │
└────────────────────────────────────────────────────────────┘

Entity Alias: "FertiRega Devices" (all devices of type)
State: "default"
Navigation: Click → Device Details (state-based)
```

### Device Details Dashboard

```
┌────────────────────────────────────────────────────────────────┐
│ FERTIREGA DEVICE DETAILS              [← Back to Overview]    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────┐  ┌────────────┐                │
│  │ Device: eui-70b3...      │  │  Battery   │                │
│  │ Lat: 38.7223             │  │    🔋      │                │
│  │ Lon: -9.1393             │  │    85%     │                │
│  │ Temp: 24.5°C  Hum: 60%   │  │            │                │
│  │ Status: 🟢 Active        │  └────────────┘                │
│  └──────────────────────────┘                                 │
│                                                                │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐  │
│  │ Valve 0      │ │ Valve 1      │ │  Schedule Valve      │  │
│  │ ━━━━●        │ │ ●━━━━        │ │  Valve: [0▼]         │  │
│  │ 🟢 Open      │ │ ⚪ Closed    │ │  Start: [DateTime]   │  │
│  │              │ │              │ │  Duration: [60 min]  │  │
│  └──────────────┘ └──────────────┘ │  [Send Schedule]     │  │
│                                    └──────────────────────┘  │
│                                                                │
│  ┌──────────────────────────┐  ┌──────────────────────────┐  │
│  │  Temperature (24h)       │  │  Humidity (24h)          │  │
│  │  📈                      │  │  📈                      │  │
│  │     ╱╲   ╱╲             │  │      ╱╲  ╱╲             │  │
│  │    ╱  ╲ ╱  ╲            │  │     ╱  ╲╱  ╲            │  │
│  └──────────────────────────┘  └──────────────────────────┘  │
│                                                                │
│  ┌──────────────────────────┐  ┌──────────────────────────┐  │
│  │  Valve 0 Status Log      │  │  Valve 1 Status Log      │  │
│  │  ▂▂▔▔▔▂▂▔▔▂▂            │  │  ▔▔▔▂▂▂▔▔▔▂▂            │  │
│  └──────────────────────────┘  └──────────────────────────┘  │
│                                                                │
└────────────────────────────────────────────────────────────────┘

Entity Alias: "Selected Device" (from navigation state)
State: "deviceDetails" (parameterized)
Widgets: Device Info, Valve Controls, Charts, Scheduler
```

## ⚙️ Widget Component Architecture

### Valve Control Widget (Internal)

```
┌─────────────────────────────────────────────┐
│ fertirega_valvecontrol_0                    │
├─────────────────────────────────────────────┤
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ Template HTML                           │ │
│ │ • Header: "Valve 0"                     │ │
│ │ • Status Badge: "Open" / "Closed"       │ │
│ │ • Toggle Switch: ng-model="valveChecked"│ │
│ │ • Last Updated: timestamp               │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ Template CSS                            │ │
│ │ • Switch styling (iOS-style)            │ │
│ │ • Color coding (green/gray)             │ │
│ │ • Responsive layout                     │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ Controller Script (JavaScript)          │ │
│ │                                         │ │
│ │ onInit():                               │ │
│ │   - Initialize state                    │ │
│ │   - Subscribe to telemetry              │ │
│ │                                         │ │
│ │ toggleValve():                          │ │
│ │   1. Get device EUI                     │ │
│ │   2. Encode command: [0, 1] → Base64    │ │
│ │   3. Build payload: {queueItem: {...}}  │ │
│ │   4. HTTP POST to ChirpStack            │ │
│ │   5. Handle response / error            │ │
│ │                                         │ │
│ │ onDataUpdated():                        │ │
│ │   - Update switch state from telemetry  │ │
│ │   - Refresh UI (detectChanges)          │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Config:                                     │
│ • Datasource: valve_0_status (timeseries)  │ │
│ • Entity Alias: selected_device            │ │
│ • Type: RPC                                │ │
└─────────────────────────────────────────────┘
```

## 🔔 Alarm Rule Chain Flow

```
                    ┌─────────────────┐
                    │ Message Input   │
                    │ (Telemetry)     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌─────────────┐
    │ Battery     │ │ Inactivity   │ │ Valve       │
    │ Check       │ │ Check        │ │ Logger      │
    │ < 20%?      │ │ > 3h?        │ │ Transform   │
    └──────┬──────┘ └──────┬───────┘ └──────┬──────┘
           │               │                 │
      [True]          [True]            [Always]
           │               │                 │
           ▼               ▼                 ▼
    ┌─────────────┐ ┌──────────────┐ ┌─────────────┐
    │ Create      │ │ Create       │ │ Save to     │
    │ Low Battery │ │ Device       │ │ Timeseries  │
    │ Alarm       │ │ Offline      │ │             │
    │ (WARNING)   │ │ Alarm        │ │ valve_log   │
    └─────────────┘ │ (CRITICAL)   │ └─────────────┘
                    └──────────────┘

Alarm Details:
• Low Battery: {batteryLevel, ts}
• Device Offline: {lastActivityTime, inactivityHours}

Logging Format:
{
  "valve": 0 or 1,
  "status": 0 or 1,
  "statusText": "Open" / "Closed",
  "timestamp": epoch_ms
}
```

## 🔐 Security Considerations

### Current Implementation

```
Browser (Widget JS)
    │
    │ [HTTP POST with API Key in Headers]
    │ ⚠️ API Key visible in client-side code
    ▼
ChirpStack API
```

**Risk**: API key exposed in browser JavaScript

### Recommended Production Setup

```
Browser (Widget)
    │
    │ [ThingsBoard RPC Call]
    ▼
ThingsBoard Server
    │
    │ [Rule Chain: RPC to REST Integration]
    ▼
ChirpStack API
    │ API Key stored server-side (secure)
    ▼
Device Queue
```

**Benefit**: API key never leaves ThingsBoard server

### Implementation Steps

1. Create REST integration in ThingsBoard
2. Configure ChirpStack endpoint + API key
3. Create rule chain: RPC → REST Integration
4. Update widgets to use ThingsBoard RPC instead of direct HTTP

## 📦 Entity Dependencies

```
┌──────────────────────┐
│ Widget Bundle        │
│ fertirega_widgets    │
└──────────┬───────────┘
           │
           │ [Required by]
           ▼
┌──────────────────────┐     ┌──────────────────────┐
│ Overview Dashboard   │────▶│ Device Profile       │
│ 31b6ecf1-...        │     │ FertiRega LoRa       │
└──────────┬───────────┘     └──────────┬───────────┘
           │                            │
           │ [Navigates to]             │ [Assigned to]
           ▼                            ▼
┌──────────────────────┐     ┌──────────────────────┐
│ Details Dashboard    │     │ Rule Chain           │
│ 58351f95-...        │     │ da36c158-...         │
└──────────────────────┘     └──────────────────────┘
           │                            │
           │ [Uses]                     │ [Creates]
           ▼                            ▼
┌──────────────────────┐     ┌──────────────────────┐
│ Entity Aliases       │     │ Alarms               │
│ • FertiRega Devices  │     │ • Low Battery        │
│ • Selected Device    │     │ • Device Offline     │
└──────────────────────┘     └──────────────────────┘
```

## 🗂️ Database Schema (Simplified)

### Telemetry (Time-Series)

```sql
-- Temperature readings
ts           | entity_id | key         | value
1732915200000| device-1  | temperature | 24.5
1732915260000| device-1  | temperature | 24.7

-- Valve status
ts           | entity_id | key             | value
1732915200000| device-1  | valve_0_status  | 0
1732915260000| device-1  | valve_0_status  | 1

-- Valve logs (generated by rule chain)
ts           | entity_id | key             | value
1732915260000| device-1  | valve_status_log| '{"valve":0,"status":1,...}'
```

### Attributes

```sql
-- Device attributes
entity_id | scope  | key        | value
device-1  | SERVER | Server_Lat | "38.7223"
device-1  | SERVER | Server_Lon | "-9.1393"
device-1  | SERVER | active     | true
```

### Alarms

```sql
-- Active alarms
entity_id | type         | severity | status      | details
device-1  | Low Battery  | WARNING  | ACTIVE_UNACK| {"batteryLevel":15}
device-2  | Device Offline| CRITICAL | ACTIVE_ACK  | {"inactivityHours":4.5}
```

## 🌐 Network Topology

```
┌────────────────────────────────────────────────────────────────┐
│                         NETWORK LAYOUT                         │
└────────────────────────────────────────────────────────────────┘

┌──────────────┐                    ┌──────────────┐
│ Field        │                    │ Server Room  │
│              │                    │              │
│  LoRa Devices│                    │ ChirpStack   │
│  📡📡📡     │◀────LoRa──────────▶│ 100.92.66.20 │
│              │   (863-870 MHz)    │ Port: 8080   │
└──────────────┘                    └──────┬───────┘
                                           │
                                           │ MQTT
                                           │
                                    ┌──────▼───────┐
                                    │ ThingsBoard  │
                                    │ (Local/Cloud)│
                                    │ Port: 8080   │
                                    └──────┬───────┘
                                           │
                                           │ HTTPS
                                           │
                                    ┌──────▼───────┐
                                    │ Web Browser  │
                                    │ (Dashboard)  │
                                    └──────────────┘
```

## 🔄 State Management

### Dashboard Navigation States

```
Overview Dashboard
    │
    │ State: "default"
    │ Entity: null
    │
    │ [User clicks device marker]
    │
    ▼
Navigation Action
    │
    │ Type: "Navigate to new dashboard state"
    │ Target: Device Details Dashboard
    │ State Param: entityId = selected_device_id
    │
    ▼
Device Details Dashboard
    │
    │ State: "deviceDetails"
    │ Entity: device-1 (from state param)
    │ Alias: "Selected Device" → resolves to entity from param
    │
    │ [User clicks "Back to Overview"]
    │
    ▼
Navigation Action
    │
    │ Type: "Navigate to other dashboard"
    │ Target: Overview Dashboard ID
    │
    ▼
Overview Dashboard (loop)
```

## 📈 Performance Considerations

### Widget Updates

- **Telemetry Polling**: 1-second intervals (realtime)
- **Batch Size**: 1 latest value per key
- **Websocket**: Used for live updates
- **HTTP**: Used for ChirpStack commands

### Data Retention

- **Telemetry**: Default TTL (configurable)
- **Valve Logs**: Same as telemetry
- **Alarms**: Cleared manually or via rule

### Scalability

- **Devices**: Tested with ~10, can scale to 100s
- **Concurrent Users**: Dashboard can handle multiple viewers
- **API Rate Limits**: ChirpStack may have limits (check docs)

## 🎓 Key Technologies

| Layer | Technology |
|-------|------------|
| **Frontend** | ThingsBoard Dashboards, Angular.js Widgets |
| **Backend** | ThingsBoard CE (Java, Cassandra/PostgreSQL) |
| **Communication** | MQTT (TTN), HTTP REST (ChirpStack) |
| **LoRa Network** | ChirpStack Network Server |
| **LoRa Protocol** | LoRaWAN 1.0.3 |
| **Data Encoding** | Base64, JSON |

---

**This architecture document provides a complete technical overview of the FertiRega IoT system.**

For setup instructions, see `QUICK_START.md` or `FERTIREGA_DASHBOARD_SETUP.md`.
