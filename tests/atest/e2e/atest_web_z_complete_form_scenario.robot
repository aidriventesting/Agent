*** Settings ***
Documentation    Complete E2E scenario on a real website: Wikipedia article exploration
...              This test simulates a real user journey: search, navigate, read, and explore Wikipedia
Library    Browser
Resource    ${EXECDIR}/tests/atest/browsers/config.robot

*** Variables ***
${WIKIPEDIA_URL}    https://en.wikipedia.org

*** Test Cases ***
Test Real World Wikipedia Navigation Scenario
    [Documentation]    Real-world scenario: User searches for Robot Framework on Wikipedia,
    ...                explores the article, navigates to related topics, and uses various interactions
    [Tags]    web    e2e    real-world    wikipedia
    
    # === Step 1: Open Wikipedia ===
    Open Website    ${WIKIPEDIA_URL}
    Sleep    ${delay}s
    Agent.check    instruction=verify that we are on the Wikipedia homepage
    Sleep    ${delay}s
    
    # === Step 2: Search for Robot Framework ===
    Agent.do    instruction=type "Robot Framework" in the search box
    Sleep    ${delay}s
    Agent.check    instruction=verify that the search suggestions appear with Robot Framework
    Sleep    ${delay}s
    
    # === Step 3: Submit search ===
    Agent.do    instruction=press Enter key to search
    Sleep    ${delay}s
    Agent.check    instruction=verify that we are on the Robot Framework Wikipedia page
    Sleep    ${delay}s
    
    # === Step 4: Read the introduction by hovering ===
    Agent.do    instruction=hover over the text particpate in the 2025 international science photo competition
    Sleep    ${delay}s
    Agent.check    instruction=verify that the text "participate in the 2025 international science photo competition" is underlined
    Sleep    ${delay}s
    
    # === Step 5: Scroll down to read more content ===
    Agent.do    instruction=scroll down to read more about Robot Framework
    Sleep    ${delay}s
    Agent.check    instruction=verify that we can see more content about Robot Framework
    Sleep    ${delay}s
    
    # === Step 6: Continue scrolling to explore ===
    Agent.do    instruction=scroll down to see the History section
    Sleep    ${delay}s
    Agent.check    instruction=verify that we can see different sections of the article
    Sleep    ${delay}s
    
    # === Step 7: Scroll to a specific section (Examples) ===
    Agent.do    instruction=scroll to the Examples section at the bottom
    Sleep    ${delay}s
    Agent.check    instruction=verify that we can see the Examples section
    Sleep    ${delay}s
    
    # === Step 8: Scroll back up ===
    Agent.do    instruction=scroll up to go back to the top of the article
    Sleep    ${delay}s
    Agent.check    instruction=verify that we are back near the top of the page
    Sleep    ${delay}s
    
    # === Step 9: Click on a related link (Python programming language) ===
    Agent.do    instruction=click on the Python link in the article
    Sleep    ${delay}s
    Agent.check    instruction=verify that we are now on the Python programming language page
    Sleep    ${delay}s
    
    # === Step 10: Explore Python page by scrolling ===
    Agent.do    instruction=scroll down to read about Python
    Sleep    ${delay}s
    Agent.check    instruction=verify that we can see content about Python
    Sleep    ${delay}s
    
    # === Step 11: Navigate back to Robot Framework ===
    Agent.do    instruction=go back to the previous page
    Sleep    ${delay}s
    Agent.check    instruction=verify that we are back on the Robot Framework page
    Sleep    ${delay}s
    
    # === Step 12: Scroll to footer ===
    Agent.do    instruction=scroll to the footer at the bottom of the page
    Sleep    ${delay}s
    Agent.check    instruction=verify that we can see the Wikipedia footer with links
    Sleep    ${delay}s
    
    # === Step 13: Final check - hover over Wikipedia logo ===
    Agent.do    instruction=scroll up to the top of the page
    Sleep    ${delay}s
    Agent.do    instruction=hover over the Wikipedia logo
    Sleep    ${delay}s
    Agent.check    instruction=verify that the Wikipedia logo is visible
    Sleep    ${delay}s
    
    Close Browser

