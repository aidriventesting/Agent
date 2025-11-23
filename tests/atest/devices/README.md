# Mobile Device Configuration

## Two Options to Run Tests

### Option 1: Local Testing
- Install Appium on your PC
- Connect your Android/iOS device
- Run Appium server locally

### Option 2: BrowserStack Testing  
- Create a BrowserStack account
- Upload your app to BrowserStack
- Configure browserstack.yaml
- Tests run on real devices in the cloud

---

## Configuration

### Where to Configure

| What to configure | File | Location |
|-------------------|------|----------|
| Choose Local or BrowserStack | `settings.yaml` | Line 5: `Device_location` |
| Local device settings | `settings.yaml` | Lines 31-50 |
| BrowserStack credentials | `browserstack.yml` | Project root |

### Quick Setup

**For Local:**
```yaml
# In settings.yaml
Device_location: Local
deviceName_Android: 192.168.50.235:5555  # Your device ID
```

**For BrowserStack:**
```yaml
# In settings.yaml
Device_location: Browserstack

# In browserstack.yml (project root)
userName: your_username
accessKey: your_access_key
app: bs://your_app_id
```

---

## Run Tests

```bash
# Run any test - configuration is automatic
robot tests/atest/e2e/atest_mobile_firsttest.robot
```

The system automatically uses Local or BrowserStack based on `Device_location` in `settings.yaml`.

---

## Prerequisites

**Local:**
- Appium installed: `npm install -g appium`
- Appium running: `appium`
- Device connected: `adb devices` (Android)

**BrowserStack:**
- BrowserStack account
- App uploaded: `browserstack-sdk app upload app.apk`

