# Appium Installation Guide

Quick setup guide to install and configure Appium on your local machine for mobile test automation.

## What is Appium?

Appium is an open-source automation framework for mobile apps (Android, iOS, and hybrid). It lets you write tests using the same WebDriver API as Selenium.

**Official documentation**: https://appium.io/docs/en/latest/

## Prerequisites

- **Node.js** (v16 or higher): https://nodejs.org/
- **Java JDK** (for Android): https://www.oracle.com/java/technologies/downloads/
- **Android Studio** (for Android): https://developer.android.com/studio
- **Xcode** (for iOS, macOS only): https://developer.apple.com/xcode/

## Installation

### 1. Install Appium globally

```bash
npm install -g appium
```

Verify installation:
```bash
appium --version
```

### 2. Install Appium drivers

For Android:
```bash
appium driver install uiautomator2
```

For iOS:
```bash
appium driver install xcuitest
```

List installed drivers:
```bash
appium driver list --installed
```

**Driver documentation**: https://appium.io/docs/en/latest/ecosystem/

### 3. Install Appium Inspector (optional but recommended)

Visual tool to inspect app elements and build locators.

Download: https://github.com/appium/appium-inspector/releases

## Android Setup

### 1. Install Android SDK

Through Android Studio or command line tools:
- **SDK Manager guide**: https://developer.android.com/tools/sdkmanager

### 2. Set environment variables

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
export ANDROID_HOME=$HOME/Library/Android/sdk  # macOS
# export ANDROID_HOME=$HOME/Android/Sdk        # Linux
# export ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk  # Windows

export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

Reload:
```bash
source ~/.zshrc  # or ~/.bashrc
```

Verify:
```bash
adb --version
```

### 3. Create/start emulator

```bash
# List available emulators
emulator -list-avds

# Start emulator
emulator -avd <emulator_name>
```

**Emulator setup guide**: https://developer.android.com/studio/run/emulator

## iOS Setup (macOS only)

### 1. Install Xcode Command Line Tools

```bash
xcode-select --install
```

### 2. Install dependencies

```bash
npm install -g ios-deploy
brew install carthage
```

### 3. Configure iOS permissions

**WebDriverAgent setup**: https://appium.io/docs/en/latest/quickstart/uiauto2-driver/

## Running Appium

### Start Appium server

```bash
appium
```

Default: `http://localhost:4723`

### Custom port

```bash
appium -p 4725
```

### With logs

```bash
appium --log-level debug
```

**Server arguments**: https://appium.io/docs/en/latest/cli/args/

## Testing the Setup

### 1. Check device connection

Android:
```bash
adb devices
```

iOS:
```bash
xcrun xctrace list devices
```

### 2. Run the project's test suite

```bash
# From project root
robot tests/atest/your_test.robot
```

## Troubleshooting

### Common issues

- **Port already in use**: Kill existing Appium process or use different port
- **Device not detected**: Check USB debugging enabled (Android) or trust computer (iOS)
- **Driver errors**: Reinstall driver with `appium driver uninstall <driver>` then reinstall

### Useful commands

```bash
# Kill Appium on default port
lsof -ti:4723 | xargs kill -9

# Check Appium doctor
npm install -g appium-doctor
appium-doctor --android
appium-doctor --ios
```

**Appium Doctor**: https://github.com/appium/appium-doctor

## Useful Resources

- **Official Appium docs**: https://appium.io/docs/en/latest/
- **Appium GitHub**: https://github.com/appium/appium
- **Appium Desktop (deprecated, use Inspector)**: https://github.com/appium/appium-inspector
- **Community forum**: https://discuss.appium.io/
- **Desired Capabilities**: https://appium.io/docs/en/latest/guides/caps/

## Next Steps

Once Appium is running:
1. Configure your `.env` file with device capabilities
2. Run the quickstart guide: [07-dev-setup-quickstart.md](07-dev-setup-quickstart.md)
3. Start writing tests with the Agent library

