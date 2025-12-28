*** Settings ***
Documentation    Keywords for BrowserStack testing
Variables    ${EXECDIR}/tests/atest/config/settings.yaml
Variables    ${EXECDIR}/browserstack.yml

*** Variables ***
# BrowserStack remote URL (utilise userName et accessKey de browserstack.yml)
${DEVICE_PROVIDER_URL}      ${userName}:${accessKey}@hub-cloud.browserstack.com
${remote_url}               https://${DEVICE_PROVIDER_URL}/wd/hub

