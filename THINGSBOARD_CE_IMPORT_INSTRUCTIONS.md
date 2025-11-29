# ThingsBoard CE Widget Import Instructions

## ✅ SOLUTION CONFIRMED: Individual Widget Import

**IMPORTANT DISCOVERY**: ThingsBoard Community Edition **DOES support importing individual widgets**, but **NOT widget bundles**.

The individual widget JSON files in `widgets_bundle/` directory are ready for import!

---

## 📋 Step-by-Step Import Process

### Step 1: Create Widget Bundle Manually (1 minute)

1. Login to ThingsBoard at your instance URL
2. Navigate to: **Widget Library** (left sidebar)
3. Click the **"+"** button (top right)
4. Select **"Create new widgets bundle"**
5. Fill in:
   - **Title**: `FertiRega Widgets`
   - **Description**: `Custom widgets for FertiRega irrigation management system`
   - **Image**: Leave empty
6. Click **"Add"**

✅ **Bundle created!** Now you can import widgets into it.

---

### Step 2: Import Individual Widgets (5 minutes)

You have **5 widgets** to import. For each widget, follow these steps:

#### Widget 1: Valve 0 Control

1. Go to **Widget Library** → **FertiRega Widgets** bundle
2. Click **"+"** button → **"Import widget type"**
3. Select file: `widgets_bundle/fertirega_valvecontrol_0.json`
4. Click **"Import"**

✅ **Expected result**: "FertiRega Valve 0 Control" widget appears in the bundle

---

#### Widget 2: Valve 1 Control

1. In the same **FertiRega Widgets** bundle
2. Click **"+"** → **"Import widget type"**
3. Select file: `widgets_bundle/fertirega_valvecontrol_1.json`
4. Click **"Import"**

✅ **Expected result**: "FertiRega Valve 1 Control" widget appears

---

#### Widget 3: Device Attributes

1. Click **"+"** → **"Import widget type"**
2. Select file: `widgets_bundle/fertirega_deviceattributes.json`
3. Click **"Import"**

✅ **Expected result**: "FertiRega Device Attributes" widget appears

---

#### Widget 4: Time Picker (Scheduler)

1. Click **"+"** → **"Import widget type"**
2. Select file: `widgets_bundle/fertirega_timepicker.json`
3. Click **"Import"**

✅ **Expected result**: "FertiRega Time Picker" widget appears

---

#### Widget 5: Reset Clock

1. Click **"+"** → **"Import widget type"**
2. Select file: `widgets_bundle/fertirega_resetclock.json`
3. Click **"Import"**

✅ **Expected result**: "FertiRega Reset Clock" widget appears

---

### Step 3: Configure ChirpStack API Key (CRITICAL - 5 minutes)

Each valve control widget needs your ChirpStack API key configured.

#### Get ChirpStack API Key

1. Login to ChirpStack: `http://100.92.66.20`
2. Navigate to: **API Keys** (left sidebar)
3. Click **"Create"**
4. Give it a name: `ThingsBoard Integration`
5. **Copy the generated token** (you'll need this!)

#### Update Widgets with API Key

For **each of these 4 widgets**, update the API key:

1. **fertirega_valvecontrol_0**
2. **fertirega_valvecontrol_1**
3. **fertirega_timepicker**
4. **fertirega_resetclock**

**Steps for each widget**:

1. Go to **Widget Library** → **FertiRega Widgets**
2. Find the widget → Click **pencil icon** (Edit)
3. In the **JavaScript** tab, find this line:
   ```javascript
   'Grpc-Metadata-Authorization': 'Bearer YOUR_API_KEY_HERE'
   ```
4. Replace `YOUR_API_KEY_HERE` with your actual ChirpStack API token
5. Click **"Apply"** (bottom right)
6. Repeat for all 4 widgets

✅ **All widgets configured!**

---

### Step 4: Import Dashboards (2 minutes)

#### Import Dashboard 1: FertiRega Overview

1. Navigate to: **Dashboards** (left sidebar)
2. Click **"+"** → **"Import dashboard"**
3. Select file: `dashboard_new/31b6ecf1-ee78-405e-afed-4a0adaa71b6d.json`
4. Click **"Import"**

✅ **Dashboard imported**: "FertiRega Overview"

---

#### Import Dashboard 2: FertiRega Device Details

1. Click **"+"** → **"Import dashboard"**
2. Select file: `dashboard_new/58351f95-46c3-4346-9c89-dcbc876ed726.json`
3. Click **"Import"**

✅ **Dashboard imported**: "FertiRega Device Details"

---

### Step 5: Import Alarm Rule Chain (2 minutes)

1. Navigate to: **Rule Chains** (left sidebar)
2. Click **"+"** → **"Import rule chain"**
3. Select file: `rule_chain/da36c158-c659-4aa0-9128-db7ca02dc2c9.json`
4. Click **"Import"**

✅ **Rule chain imported**: "FertiRega Alarms and Logging"

---

### Step 6: Assign Rule Chain to Device Profile (1 minute)

1. Navigate to: **Profiles** → **Device Profiles** (left sidebar)
2. Find your device profile: **"FertiRega LoRa Sensor"** (or your profile name)
3. Click **pencil icon** (Edit)
4. In the **Rule Chain** dropdown, select: **"FertiRega Alarms and Logging"**
5. Click **"Save"**

✅ **Rule chain assigned!** Alarms will now be generated automatically.

---

## 🎯 Verification Checklist

After completing all steps, verify:

- [ ] **Widget Library** → **FertiRega Widgets** shows 5 widgets:
  - FertiRega Valve 0 Control
  - FertiRega Valve 1 Control
  - FertiRega Device Attributes
  - FertiRega Time Picker
  - FertiRega Reset Clock

- [ ] All 4 RPC widgets have ChirpStack API key configured (no `YOUR_API_KEY_HERE`)

- [ ] **Dashboards** shows 2 dashboards:
  - FertiRega Overview
  - FertiRega Device Details

- [ ] **Rule Chains** shows:
  - FertiRega Alarms and Logging

- [ ] Device profile has rule chain assigned

---

## 🧪 Testing

### Test 1: View Overview Dashboard

1. Go to **Dashboards** → **FertiRega Overview**
2. You should see:
   - Google Maps with device markers
   - Active Devices table
   - Active Alarms table

### Test 2: Navigate to Device Details

1. On Overview dashboard, click any device marker on the map
2. Should navigate to **FertiRega Device Details** dashboard
3. Should show device-specific data

### Test 3: Control a Valve

1. On Device Details dashboard
2. Find **Valve 0 Control** widget
3. Toggle the switch ON
4. **Expected**:
   - Toast notification: "Valve 0 command sent: open"
   - Check browser console for HTTP POST to ChirpStack
5. Verify in ChirpStack:
   - Go to `http://100.92.66.20` → Devices → Your Device → Queue
   - Should see queued downlink command

### Test 4: Trigger an Alarm

1. Send test telemetry with low battery:
   ```json
   {"battery_percentage": 15}
   ```
2. Wait 30 seconds
3. Check **Active Alarms** widget on Overview dashboard
4. Should see: **"Low Battery"** alarm with WARNING severity

---

## 🐛 Troubleshooting

### ❌ "Unable to import widget type"

**Possible causes**:
1. Widget bundle "FertiRega Widgets" doesn't exist → Create it first (Step 1)
2. File is corrupted → Re-download from git repository
3. Wrong file selected → Verify file name matches widget

**Solution**: Ensure bundle exists, then retry import

---

### ❌ Valve control not working (no command sent)

**Possible causes**:
1. ChirpStack API key not configured → Shows `YOUR_API_KEY_HERE` in code
2. Device EUI not resolved correctly
3. ChirpStack server unreachable

**Solution**:
1. Edit widget → Verify API key is configured (Step 3)
2. Check browser console for error messages
3. Test ChirpStack API manually:
   ```bash
   curl -X GET http://100.92.66.20:8080/api/devices/{devEui} \
     -H "Grpc-Metadata-Authorization: Bearer YOUR_API_KEY"
   ```

---

### ❌ Dashboard shows "No data"

**Possible causes**:
1. Devices don't have required telemetry keys
2. Entity alias not resolving devices
3. Device profile doesn't match filter

**Solution**:
1. Verify devices have these telemetry keys:
   - `temperature`, `humidity`, `battery_percentage`
   - `valve_0_status`, `valve_1_status`
2. Verify devices have these attributes:
   - `Server_Lat`, `Server_Lon`, `Device_Name`, `active`
3. Edit dashboard → Check entity alias configuration

---

### ❌ Navigation between dashboards broken

**Possible causes**:
- Dashboard IDs changed during import

**Solution**:
1. Edit **Overview Dashboard**
2. Google Maps widget → **Actions** → **markerClick**
3. Update target dashboard to "FertiRega Device Details"
4. Edit **Device Details Dashboard**
5. Back button widget → **Actions** → **headerButton**
6. Update target dashboard to "FertiRega Overview"

---

## 📊 Required Data Format

### Telemetry Keys

Your devices must send these telemetry keys:

```json
{
  "temperature": 25.3,
  "humidity": 65.2,
  "battery_percentage": 85.0,
  "valve_0_status": 0,
  "valve_1_status": 1
}
```

- `valve_X_status`: `0` = closed, `1` = open

### Server Attributes

Your devices must have these server attributes:

```json
{
  "Server_Lat": "38.7223",
  "Server_Lon": "-9.1393",
  "Device_Name": "Field A - Sensor 1",
  "active": true
}
```

- `active`: `true` = online, `false` = offline

---

## 🎉 Success!

Once all steps are completed, you should have:

✅ **5 custom widgets** in FertiRega Widgets bundle
✅ **2 dashboards** (Overview + Device Details)
✅ **Valve control** via ChirpStack HTTP API
✅ **Automatic alarms** for low battery and offline devices
✅ **Valve status logging** for historical tracking
✅ **Map visualization** with device markers
✅ **Charts** for temperature, humidity, battery trends

---

## 📁 File Reference

| Widget | File |
|--------|------|
| Valve 0 Control | `widgets_bundle/fertirega_valvecontrol_0.json` |
| Valve 1 Control | `widgets_bundle/fertirega_valvecontrol_1.json` |
| Device Attributes | `widgets_bundle/fertirega_deviceattributes.json` |
| Time Picker | `widgets_bundle/fertirega_timepicker.json` |
| Reset Clock | `widgets_bundle/fertirega_resetclock.json` |

| Dashboard | File |
|-----------|------|
| Overview | `dashboard_new/31b6ecf1-ee78-405e-afed-4a0adaa71b6d.json` |
| Device Details | `dashboard_new/58351f95-46c3-4346-9c89-dcbc876ed726.json` |

| Rule Chain | File |
|------------|------|
| Alarms & Logging | `rule_chain/da36c158-c659-4aa0-9128-db7ca02dc2c9.json` |

---

## 📝 Notes

### Why Individual Widget Import?

**ThingsBoard CE** does not support importing complete widget bundles from JSON files. This is a **Professional Edition (PE) exclusive feature**.

However, **CE does support importing individual widget types** into an existing bundle.

**The solution**:
1. Create empty bundle manually (UI)
2. Import individual widgets one by one (JSON files)

This approach works perfectly and gives you the same result!

### Widget Bundle Structure

The widget bundle JSON files you attempted to import (`fertirega_widgets_bundle.json`, `fertirega_widgets_FIXED.json`, etc.) are used for:
- Git repository storage
- Documentation
- Reference

They **cannot be directly imported into ThingsBoard CE**.

The individual widget files (e.g., `fertirega_valvecontrol_0.json`) are the ones that **can be imported**.

---

## 🚀 Next Steps

After successful import:

1. **Test valve control** with a real device
2. **Verify alarm triggering** (low battery, offline)
3. **Customize scheduling widget** (provide device protocol)
4. **Set up notification targets** (email, SMS for alarms)
5. **Add more devices** to see full dashboard capabilities

---

## 📞 Support

If you encounter issues during import:

1. Check browser console for JavaScript errors
2. Verify file paths are correct
3. Ensure ThingsBoard version compatibility (CE 3.x+)
4. Review this guide's troubleshooting section

---

**Estimated Total Time**: 15-20 minutes
**Difficulty**: Easy (just follow the steps!)
**Result**: Fully functional FertiRega irrigation management dashboard

---

**Generated by**: Claude (Anthropic)
**Date**: 2025-11-29
**ThingsBoard**: Community Edition
**Import Method**: Individual Widget JSON Files
