*** Settings ***
Documentation    Keywords for local testing
Variables    ${EXECDIR}/tests/atest/config/settings.yaml

*** Variables ***
# Variables calculées depuis settings.yaml
${remote_url}               ${remote_url_local}
${appPackage}               ${app_package_Android}
${appActivity}              ${app_activity_Android}

# Desired Capabilities for local Android
&{DESIRED_CAPABILITIES_Android}
...                         appium:deviceName=${deviceName_Android}
...                         platformName=${platformName_Android}
...                         appium:appPackage=${appPackage}
...                         appium:appActivity=${appActivity}
...                         appium:automationName=${automationName_Android}
...                         appium:noReset=${noReset_Android}
...                         appium:language=${language_Android}
...                         appium:locale=${locale_Android}

# Desired Capabilities for local iOS
&{DESIRED_CAPABILITIES_iOS}
...                         appium:deviceName=${deviceName_iOS}
...                         platformName=${platformName_iOS}
...                         appium:app=${appPath_iOS}
...                         appium:automationName=${automationName_iOS}
...                         bundleId=${bundleId}
...                         udid=${udid}
...                         xcodeOrgId=${xcodeOrgId}
...                         xcodeSigningId=${xcodeSigningId}
...                         fullReset=${fullReset_iOS}
...                         appium:language=${language_iOS}
...                         appium:locale=${locale_iOS}
...                         ${AllowPopupCap_iOS}=true
