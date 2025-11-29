# FertiRega Dashboard Setup Guide

## 📋 Table of Contents
1. [Overview](#overview)
2. [What Was Created](#what-was-created)
3. [Import Instructions](#import-instructions)
4. [ChirpStack Configuration](#chirpstack-configuration)
5. [Dashboard Usage](#dashboard-usage)
6. [Troubleshooting](#troubleshooting)

---

## Overview

This guide covers the complete FertiRega irrigation management dashboard system for ThingsBoard CE. The solution includes:

- **2 Dashboards**: Overview (map view) and Device Details (control & monitoring)
- **5 Custom Widgets**: Valve controls, device attributes, time picker, reset clock
- **1 Alarm Rule Chain**: Battery alerts, offline detection, valve logging

---

## What Was Created

### 📁 File Structure

```
fertirega_backend/
├── widgets_bundle/
│   └── fertirega_widgets_bundle.json       # Custom widgets bundle
├── dashboard_new/
│   ├── 31b6ecf1-ee78-405e-afed-4a0adaa71b6d.json  # Overview Dashboard
│   └── 58351f95-46c3-4346-9c89-dcbc876ed726.json  # Device Details Dashboard
├── rule_chain/
│   └── da36c158-c659-4aa0-9128-db7ca02dc2c9.json  # Alarms & Logging
└── FERTIREGA_DASHBOARD_SETUP.md            # This file
```

### 🎨 Custom Widgets

| Widget | Type | Purpose |
|--------|------|---------|
| `fertirega_valvecontrol_0` | RPC | Control Valve 0 via ChirpStack |
| `fertirega_valvecontrol_1` | RPC | Control Valve 1 via ChirpStack |
| `fertirega_deviceattributes` | Latest | Display device info (location, battery, sensors) |
| `fertirega_timepicker` | Static | Schedule valve operations |
| `fertirega_resetclock` | RPC | Sync device clock with server |

### 📊 Dashboards

#### 1. FertiRega Overview
- **File**: `31b6ecf1-ee78-405e-afed-4a0adaa71b6d.json`
- **Features**:
  - Google Maps with all FertiRega devices
  - Color-coded markers (green=active, red=offline)
  - Device info tooltips (temp, humidity, battery, valve status)
  - Click device → Navigate to details
  - Active devices table
  - Active alarms table

#### 2. FertiRega Device Details
- **File**: `58351f95-46c3-4346-9c89-dcbc876ed726.json`
- **Features**:
  - Device information panel
  - Battery level gauge
  - Valve 0 & 1 toggle controls
  - Scheduling interface
  - Temperature & humidity charts (24h history)
  - Valve status history charts
  - Back to overview button

### 🔔 Alarm Rule Chain

**File**: `da36c158-c659-4aa0-9128-db7ca02dc2c9.json`

**Alarms**:
1. **Low Battery** (WARNING) - Triggers when `battery_percentage < 20%`
2. **Device Offline** (CRITICAL) - Triggers after 3 hours of inactivity

**Logging**:
- Automatically logs all valve status changes to timeseries
- Creates structured log entries with timestamp, valve #, and status

---

## Import Instructions

### Step 1: Import Widget Bundle

1. **Login to ThingsBoard**
2. Navigate to **Widget Library**
3. Click the **+** button (top right) → **Import widget bundle**
4. Select file: `widgets_bundle/fertirega_widgets_bundle.json`
5. Click **Import**

✅ You should now see "FertiRega Widgets" in your widget library.

### Step 2: Configure ChirpStack API Key

**IMPORTANT**: Before importing dashboards, you must update the ChirpStack API key in the widget bundle.

1. In **Widget Library**, find "FertiRega Widgets"
2. Click on each valve control widget (fertirega_valvecontrol_0 and fertirega_valvecontrol_1)
3. Edit the widget
4. In the **JavaScript** tab, find the line:
   ```javascript
   'Grpc-Metadata-Authorization': 'Bearer YOUR_API_KEY_HERE'
   ```
5. Replace `YOUR_API_KEY_HERE` with your actual ChirpStack API key
6. Click **Apply** and **Save**

**To get your ChirpStack API Key**:
- Login to ChirpStack at `http://100.92.66.20`
- Go to **API Keys** → **Create**
- Copy the generated token
- Paste it into the widget configuration

### Step 3: Import Dashboards

#### Import Overview Dashboard
1. Navigate to **Dashboards**
2. Click **+** → **Import dashboard**
3. Select file: `dashboard_new/31b6ecf1-ee78-405e-afed-4a0adaa71b6d.json`
4. Click **Import**

#### Import Device Details Dashboard
1. Click **+** → **Import dashboard**
2. Select file: `dashboard_new/58351f95-46c3-4346-9c89-dcbc876ed726.json`
3. Click **Import**

### Step 4: Link Dashboards

After importing both dashboards, you need to update the navigation links:

1. **Edit Overview Dashboard**:
   - Open the Overview dashboard
   - Click **Edit** (pencil icon)
   - Find the **Google Maps** widget settings
   - In **Actions** → **markerClick**, verify the target dashboard state
   - Save

2. **Edit Device Details Dashboard**:
   - Open the Device Details dashboard
   - Click **Edit**
   - Find the **Back to Overview** button
   - In **Actions** → **buttonClick**, update the target dashboard ID to the Overview dashboard ID
   - Save

### Step 5: Import Alarm Rule Chain

1. Navigate to **Rule Chains**
2. Click **+** → **Import rule chain**
3. Select file: `rule_chain/da36c158-c659-4aa0-9128-db7ca02dc2c9.json`
4. Click **Import**

### Step 6: Assign Rule Chain to Device Profile

1. Navigate to **Device Profiles**
2. Find "FertiRega LoRa Sensor" profile
3. Edit the profile
4. In **Rule Chain**, select "FertiRega Alarms and Logging"
5. Save

---

## ChirpStack Configuration

### API Endpoint

The widgets are configured to send commands to:
```
http://100.92.66.20:8080/api/devices/{devEui}/queue
```

### Command Format

**Valve Control** (fPort 2):
```javascript
{
  "queueItem": {
    "confirmed": true,
    "data": "<base64_encoded_payload>",
    "fPort": 2
  }
}
```

**Payload Structure**:
- Byte 0: Valve number (0 or 1)
- Byte 1: Action (0 = close, 1 = open)

**Example**: To open Valve 0:
- Bytes: `[0, 1]`
- Base64: `AAE=`

### Device EUI Resolution

The widgets try to extract the device EUI in the following order:
1. From entity name if it starts with `eui-` (e.g., `eui-70b3d57ed006996d`)
2. From entity ID (fallback)

**Recommendation**: Name your devices with the format `eui-{deviceEui}` for automatic resolution.

### Scheduling Format (To Be Customized)

The time picker widget uses **fPort 3** for scheduling commands. The payload format is currently:
```json
{
  "valve": 0,              // 0 or 1
  "startTime": 1234567890, // Unix timestamp (ms)
  "duration": 60,          // Minutes
  "repeat": "daily"        // "none", "daily", "weekly"
}
```

**TODO**: Update the `fertirega_timepicker` widget with your actual device scheduling protocol.

### Clock Sync (fPort 4)

The reset clock widget sends a Unix timestamp (4 bytes, big-endian) on fPort 4.

---

## Dashboard Usage

### Using the Overview Dashboard

1. **Open the Dashboard**:
   - Navigate to **Dashboards** → "FertiRega Overview"

2. **View Devices on Map**:
   - All FertiRega devices appear as markers
   - Green markers = active devices
   - Red markers = inactive/offline devices
   - Hover over markers to see device info

3. **Navigate to Device Details**:
   - Click on any map marker
   - OR click on a row in the device table
   - You'll be redirected to the Device Details dashboard

4. **Monitor Alarms**:
   - Check the "Active Alarms" widget for any issues
   - Alarms appear for low battery or offline devices

### Using the Device Details Dashboard

1. **Control Valves**:
   - Toggle the switch for Valve 0 or Valve 1
   - The widget sends a command to ChirpStack
   - You'll see a toast notification confirming the command
   - The valve status updates automatically when the device reports back

2. **Monitor Sensor Data**:
   - View current temperature and humidity in the Device Information panel
   - Check the battery level gauge
   - Review historical charts for trends

3. **Schedule Operations**:
   - Use the Time Picker widget to schedule valve operations
   - Select valve, start time, duration, and repeat mode
   - Click "Send Schedule"

4. **Return to Overview**:
   - Click the "← Back to Overview" button in the top right

### Understanding Valve Status

- **Open** = Green badge, switch ON, status value = 1
- **Closed** = Gray badge, switch OFF, status value = 0

Status changes are logged automatically by the alarm rule chain.

---

## Troubleshooting

### Widgets Not Appearing

**Problem**: Custom widgets show as "Widget type not found"

**Solution**:
1. Verify the widget bundle was imported successfully
2. Check that the widget bundle alias is `fertirega_widgets`
3. Re-import the widget bundle if necessary

### Valve Control Not Working

**Problem**: Clicking valve switches doesn't control the device

**Checklist**:
- [ ] ChirpStack API key is configured in the widget
- [ ] ChirpStack server is accessible at `http://100.92.66.20:8080`
- [ ] Device EUI is correctly resolved (check browser console for errors)
- [ ] Device is online and connected to ChirpStack
- [ ] ChirpStack API accepts the command format

**Debug Steps**:
1. Open browser developer console (F12)
2. Toggle a valve switch
3. Check for HTTP errors in the Network tab
4. Verify the request payload matches the expected format
5. Check ChirpStack device queue for queued messages

### Dashboard Navigation Not Working

**Problem**: Clicking on devices doesn't navigate to details

**Solution**:
1. Edit the Overview dashboard
2. Check the Google Maps widget actions
3. Ensure the "Navigate to new dashboard state" action points to the correct dashboard
4. Save and try again

### Alarms Not Triggering

**Problem**: Low battery or offline alarms not appearing

**Checklist**:
- [ ] Rule chain is imported
- [ ] Rule chain is assigned to the device profile
- [ ] Devices are using the "FertiRega LoRa Sensor" profile
- [ ] Telemetry data is being received (check device telemetry)

**Debug Steps**:
1. Navigate to **Rule Chains** → "FertiRega Alarms and Logging"
2. Enable **Debug Mode**
3. Send test telemetry with `battery_percentage: 15`
4. Check rule chain events for processing

### Map Not Showing Devices

**Problem**: Google Maps widget is empty

**Checklist**:
- [ ] Devices have `Server_Lat` and `Server_Lon` attributes
- [ ] Entity alias "FertiRega Devices" is correctly configured
- [ ] Device type matches "FertiRega LoRa Sensor"
- [ ] Google Maps API key is configured (if using Google Maps provider)

**Alternative**: Use OpenStreetMap provider:
1. Edit the Overview dashboard
2. Edit the Google Maps widget
3. Change `provider` to `openstreet-map`
4. Save

### Scheduling Not Working

**Problem**: Schedule commands don't reach the device

**Solution**:
1. The time picker widget uses a placeholder scheduling format
2. You need to customize it based on your device's protocol
3. Edit the `fertirega_timepicker` widget
4. Update the payload encoding in the JavaScript code
5. Ensure the fPort matches your device's expectation

---

## Next Steps

### Recommended Customizations

1. **Update Scheduling Protocol**:
   - Share your device's scheduling command format
   - Update the `fertirega_timepicker` widget accordingly

2. **Configure Google Maps API** (Optional):
   - Get a Google Maps API key
   - Add it to ThingsBoard: **System Settings** → **General** → **Google Maps API Key**

3. **Set Up Notifications** (Optional):
   - Create notification targets (email, SMS, etc.)
   - Link them to the alarm rules

4. **Customize Alarm Thresholds**:
   - Edit the rule chain to adjust battery threshold (currently 20%)
   - Adjust inactivity timeout (currently 3 hours)

### Git Sync for ThingsBoard CE

Since ThingsBoard CE doesn't have native Git integration, here are your options:

#### Option 1: Manual Export/Import
- Export entities via UI after making changes
- Commit JSON files to Git manually
- Import on other instances

#### Option 2: REST API Script
Create a script to automate export using ThingsBoard REST API:

```bash
#!/bin/bash
# export_entities.sh

TB_URL="http://your-thingsboard-url"
USERNAME="your@email.com"
PASSWORD="yourpassword"

# Login and get token
TOKEN=$(curl -X POST "$TB_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
  | jq -r '.token')

# Export dashboards
curl -H "X-Authorization: Bearer $TOKEN" \
  "$TB_URL/api/dashboard/{dashboardId}" > dashboard.json

# Commit to git
git add .
git commit -m "Update ThingsBoard entities"
git push
```

#### Option 3: Upgrade to ThingsBoard PE
ThingsBoard Professional Edition includes:
- Native Git integration
- Automatic entity synchronization
- Version control UI

---

## Support & Further Customization

If you need additional features or customizations:

1. **Device EUI Mapping**: If your device names don't follow the `eui-{id}` format
2. **Additional Sensors**: Add more telemetry keys to widgets
3. **Custom Scheduling**: Implement your specific scheduling protocol
4. **Multi-tenant Setup**: Configure customer hierarchies
5. **Advanced Alarms**: Add more alarm conditions (valve stuck, etc.)

---

## Summary

You now have:
✅ Custom widget bundle with 5 FertiRega widgets
✅ Overview dashboard with map and device navigation
✅ Device details dashboard with valve control and monitoring
✅ Alarm rule chain for battery and offline alerts
✅ Automatic valve status logging

**Next**: Import the entities following the steps above and configure your ChirpStack API key!
