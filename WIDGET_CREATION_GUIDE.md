# FertiRega Widgets - Manual Creation Guide

## ⚠️ Important Note

ThingsBoard CE doesn't support importing custom widget bundles via JSON files the same way as PE. You need to create the widgets manually through the UI.

---

## 📋 Step-by-Step Widget Creation

### Step 1: Create Widget Bundle

1. Go to **Widget Library** in ThingsBoard
2. Click the **+** button (top right)
3. Select **Create new widgets bundle**
4. Fill in:
   - **Title**: `FertiRega Widgets`
   - **Description**: `Custom widgets for FertiRega irrigation management system`
5. Click **Add**

---

### Step 2: Create Widget - Valve 0 Control

1. In Widget Library, find "FertiRega Widgets" bundle
2. Click **Open widgets bundle**
3. Click **+** → **Create new widget type**
4. Select widget type: **Control widget**
5. Fill in the following:

#### Basic Settings
- **Widget type name**: `FertiRega Valve 0 Control`
- **Description**: `Toggle switch control for Valve 0 with ChirpStack HTTP API`

#### Resources Tab
- Leave empty (no external resources needed)

#### HTML Tab
```html
<div class="valve-control-container">
  <div class="valve-header">
    <h3>Valve 0</h3>
    <span class="valve-status" ng-class="{'valve-open': valveStatus === 1, 'valve-closed': valveStatus === 0}">{{valveStatusText}}</span>
  </div>
  <div class="switch-container">
    <label class="switch">
      <input type="checkbox" ng-model="valveChecked" ng-change="toggleValve()">
      <span class="slider round"></span>
    </label>
  </div>
  <div class="valve-info">
    <p>Last Updated: {{lastUpdate | date:'short'}}</p>
  </div>
</div>
```

#### CSS Tab
```css
.valve-control-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  height: 100%;
}

.valve-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.valve-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: #333;
}

.valve-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.valve-open {
  background: #4caf50;
  color: white;
}

.valve-closed {
  background: #9e9e9e;
  color: white;
}

.switch-container {
  margin: 20px 0;
}

.switch {
  position: relative;
  display: inline-block;
  width: 80px;
  height: 40px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 32px;
  width: 32px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: #4caf50;
}

input:checked + .slider:before {
  transform: translateX(40px);
}

.slider.round {
  border-radius: 40px;
}

.slider.round:before {
  border-radius: 50%;
}

.valve-info {
  margin-top: 20px;
  text-align: center;
  color: #666;
  font-size: 12px;
}
```

#### JavaScript Tab
```javascript
self.onInit = function() {
    self.ctx.$scope.valveStatus = 0;
    self.ctx.$scope.valveChecked = false;
    self.ctx.$scope.valveStatusText = 'Closed';
    self.ctx.$scope.lastUpdate = new Date();

    // Subscribe to valve status
    self.ctx.defaultSubscription.subscribe();

    self.ctx.$scope.toggleValve = function() {
        var action = self.ctx.$scope.valveChecked ? 1 : 0;
        var actionText = action === 1 ? 'open' : 'close';

        // Get device EUI from entity name or attributes
        var deviceName = self.ctx.defaultSubscription.entityName;
        var devEui = self.ctx.defaultSubscription.entityId.id;

        // Try to get EUI from attributes if available
        if (self.ctx.datasources && self.ctx.datasources[0] && self.ctx.datasources[0].entity) {
            var entity = self.ctx.datasources[0].entity;
            if (entity.name && entity.name.startsWith('eui-')) {
                devEui = entity.name.replace('eui-', '');
            }
        }

        // Encode command to base64
        var valve = 0; // Valve 0
        var buffer = [valve, action];
        var base64 = btoa(String.fromCharCode.apply(null, buffer));

        var payload = {
            queueItem: {
                confirmed: true,
                data: base64,
                fPort: 2
            }
        };

        // Send HTTP request to ChirpStack
        var url = 'http://100.92.66.20:8080/api/devices/' + devEui + '/queue';

        self.ctx.http.post(url, payload, {
            headers: {
                'Content-Type': 'application/json',
                'Grpc-Metadata-Authorization': 'Bearer YOUR_API_KEY_HERE'
            }
        }).subscribe(
            function(response) {
                self.ctx.$scope.valveStatus = action;
                self.ctx.$scope.valveStatusText = action === 1 ? 'Open' : 'Closed';
                self.ctx.$scope.lastUpdate = new Date();
                self.ctx.showSuccessToast('Valve 0 command sent: ' + actionText);
            },
            function(error) {
                self.ctx.$scope.valveChecked = !self.ctx.$scope.valveChecked;
                self.ctx.showErrorToast('Failed to send valve command: ' + error.message);
            }
        );
    };
};

self.onDataUpdated = function() {
    if (self.ctx.data && self.ctx.data.length > 0) {
        var data = self.ctx.data[0];
        if (data.data && data.data.length > 0) {
            var latestData = data.data[0];
            if (latestData[1] !== undefined) {
                self.ctx.$scope.valveStatus = latestData[1];
                self.ctx.$scope.valveChecked = latestData[1] === 1;
                self.ctx.$scope.valveStatusText = latestData[1] === 1 ? 'Open' : 'Closed';
                self.ctx.$scope.lastUpdate = new Date(latestData[0]);
                self.ctx.detectChanges();
            }
        }
    }
};

self.onDestroy = function() {
};
```

#### Settings Tab
- Leave default

6. Click **Save** and **Apply**

**⚠️ IMPORTANT**: Replace `YOUR_API_KEY_HERE` with your actual ChirpStack API key!

---

### Step 3: Create Widget - Valve 1 Control

Repeat Step 2, but with these changes:

#### Basic Settings
- **Widget type name**: `FertiRega Valve 1 Control`
- **Description**: `Toggle switch control for Valve 1 with ChirpStack HTTP API`

#### HTML Tab
Change line 3: `<h3>Valve 1</h3>`

#### JavaScript Tab
Change line 26: `var valve = 1; // Valve 1`
Change lines 35-36: `'Valve 1 command sent: ' + actionText`

---

### Step 4: Create Widget - Device Attributes

1. Create new widget type: **Latest values**
2. Fill in:

#### Basic Settings
- **Widget type name**: `FertiRega Device Attributes`
- **Description**: `Display device attributes and status information`

#### HTML Tab
```html
<div class="device-attributes-container">
  <div class="attribute-row">
    <div class="attribute-item">
      <span class="attribute-icon">📍</span>
      <div class="attribute-content">
        <span class="attribute-label">Location</span>
        <span class="attribute-value">{{latitude | number:6}}, {{longitude | number:6}}</span>
      </div>
    </div>
    <div class="attribute-item">
      <span class="attribute-icon">🔋</span>
      <div class="attribute-content">
        <span class="attribute-label">Battery</span>
        <span class="attribute-value">{{battery}}%</span>
      </div>
    </div>
  </div>
  <div class="attribute-row">
    <div class="attribute-item">
      <span class="attribute-icon">🌡️</span>
      <div class="attribute-content">
        <span class="attribute-label">Temperature</span>
        <span class="attribute-value">{{temperature | number:1}}°C</span>
      </div>
    </div>
    <div class="attribute-item">
      <span class="attribute-icon">💧</span>
      <div class="attribute-content">
        <span class="attribute-label">Humidity</span>
        <span class="attribute-value">{{humidity | number:1}}%</span>
      </div>
    </div>
  </div>
  <div class="attribute-row">
    <div class="attribute-item">
      <span class="attribute-icon">⏰</span>
      <div class="attribute-content">
        <span class="attribute-label">Last Activity</span>
        <span class="attribute-value">{{lastActivity | date:'short'}}</span>
      </div>
    </div>
    <div class="attribute-item">
      <span class="attribute-icon" ng-class="{'status-active': isActive, 'status-inactive': !isActive}">●</span>
      <div class="attribute-content">
        <span class="attribute-label">Status</span>
        <span class="attribute-value">{{statusText}}</span>
      </div>
    </div>
  </div>
</div>
```

#### CSS Tab
```css
.device-attributes-container {
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  height: 100%;
}

.attribute-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.attribute-row:last-child {
  margin-bottom: 0;
}

.attribute-item {
  display: flex;
  align-items: center;
  flex: 1;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 6px;
  margin: 0 4px;
}

.attribute-item:first-child {
  margin-left: 0;
}

.attribute-item:last-child {
  margin-right: 0;
}

.attribute-icon {
  font-size: 24px;
  margin-right: 12px;
}

.status-active {
  color: #4caf50;
}

.status-inactive {
  color: #f44336;
}

.attribute-content {
  display: flex;
  flex-direction: column;
}

.attribute-label {
  font-size: 11px;
  color: #666;
  text-transform: uppercase;
  margin-bottom: 2px;
}

.attribute-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}
```

#### JavaScript Tab
```javascript
self.onInit = function() {
    self.ctx.$scope.latitude = 0;
    self.ctx.$scope.longitude = 0;
    self.ctx.$scope.battery = 0;
    self.ctx.$scope.temperature = 0;
    self.ctx.$scope.humidity = 0;
    self.ctx.$scope.lastActivity = new Date();
    self.ctx.$scope.isActive = false;
    self.ctx.$scope.statusText = 'Offline';
};

self.onDataUpdated = function() {
    if (self.ctx.data && self.ctx.data.length > 0) {
        for (var i = 0; i < self.ctx.data.length; i++) {
            var dataItem = self.ctx.data[i];
            if (dataItem.data && dataItem.data.length > 0) {
                var latestData = dataItem.data[0];
                var dataKey = dataItem.dataKey.name;

                switch(dataKey) {
                    case 'Server_Lat':
                        self.ctx.$scope.latitude = latestData[1];
                        break;
                    case 'Server_Lon':
                        self.ctx.$scope.longitude = latestData[1];
                        break;
                    case 'battery_percentage':
                        self.ctx.$scope.battery = latestData[1];
                        break;
                    case 'temperature':
                        self.ctx.$scope.temperature = latestData[1];
                        break;
                    case 'humidity':
                        self.ctx.$scope.humidity = latestData[1];
                        break;
                    case 'active':
                        self.ctx.$scope.isActive = latestData[1] === true || latestData[1] === 'true';
                        self.ctx.$scope.statusText = self.ctx.$scope.isActive ? 'Active' : 'Offline';
                        break;
                }

                if (latestData[0]) {
                    self.ctx.$scope.lastActivity = new Date(latestData[0]);
                }
            }
        }
        self.ctx.detectChanges();
    }
};

self.onDestroy = function() {
};
```

---

### Step 5 & 6: Time Picker and Reset Clock Widgets

Due to space constraints in this guide, refer to the complete widget code in:
- `widgets_bundle/fertirega_timepicker.json`
- `widgets_bundle/fertirega_resetclock.json`

Copy the HTML, CSS, and JavaScript from these files when creating those widgets in the UI.

---

## ✅ Verification

After creating all widgets, you should have:
- ✅ Widget bundle: "FertiRega Widgets"
- ✅ 5 custom widgets:
  1. FertiRega Valve 0 Control
  2. FertiRega Valve 1 Control
  3. FertiRega Device Attributes
  4. FertiRega Time Picker (optional)
  5. FertiRega Reset Clock (optional)

---

## 🔑 Configure ChirpStack API Key

For each valve control widget:
1. Edit the widget
2. Go to **JavaScript** tab
3. Find line: `'Grpc-Metadata-Authorization': 'Bearer YOUR_API_KEY_HERE'`
4. Replace `YOUR_API_KEY_HERE` with your ChirpStack API token
5. Save

---

## 🎯 Next Steps

Once widgets are created:
1. Import the dashboards ([QUICK_START.md](QUICK_START.md))
2. Import the alarm rule chain
3. Test valve control functionality

---

## 💡 Alternative: Pre-configured ThingsBoard Instance

If manual widget creation is too tedious, consider:
1. Setting up a fresh ThingsBoard CE instance
2. Creating widgets once
3. Using ThingsBoard's built-in **export functionality** for the entire bundle
4. Importing to other instances

---

## 📞 Need Help?

If you encounter issues:
- Check browser console for JavaScript errors
- Verify ChirpStack API key is correct
- Ensure device names start with `eui-{deviceEui}`
- Test with a simple widget first (Device Attributes)

---

**Created**: 2025-11-29
**For**: ThingsBoard Community Edition
