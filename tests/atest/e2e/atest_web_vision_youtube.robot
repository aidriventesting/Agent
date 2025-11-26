*** Settings ***
Documentation    Real-world scenario tests using vision mode on popular websites
Resource    ${EXECDIR}/tests/atest/browsers/config.robot
Suite Setup    Open Website
Suite Teardown    Close Browser

*** Test Cases ***
Test YouTube Search And Interact
    [Documentation]    Search on YouTube, play video, read comment and like it
    [Tags]    vision    web    youtube    real-scenario
    
    Go To    https://www.youtube.com/
    Sleep    3s
    
    # Accept cookies if present
    Run Keyword And Ignore Error    Agent.Do    click on Accept all button
    Sleep    2s
    
    # Search for a video
    Agent.Do    click on search box
    Sleep    1s
    
    Agent.Do    type 'robot framework tutorial' in search box
    Sleep    1s
    
    Agent.Do    press Enter key
    Sleep    3s
    
    # Click on first video
    Agent.Do    click on the first video thumbnail
    Sleep    5s
    
    # Scroll down to comments
    Agent.Do    scroll down
    Sleep    2s
    Agent.Do    scroll down
    Sleep    2s
    
    # Read first comment (using check to verify it's visible)
    Agent.check    instruction=verify that comments section is visible
    Sleep    1s
    
    # Like the first comment
    Agent.Do    click on like button of the first comment
    Sleep    1s
    
    # Verify the like was registered
    Agent.check    instruction=verify that the like button is highlighted

Test Amazon Product Search
    [Documentation]    Search for a product on Amazon and add to cart
    [Tags]    vision    web    amazon    real-scenario
    
    Go To    https://www.amazon.com/
    Sleep    3s
    
    # Search for product
    Agent.Do    click on search box
    Sleep    1s
    
    Agent.Do    type 'wireless mouse' in search box
    Sleep    1s
    
    Agent.Do    click on search button
    Sleep    3s
    
    # Click on first product
    Agent.Do    click on the first product image
    Sleep    3s
    
    # Verify product page loaded
    Agent.check    instruction=verify that Add to Cart button is visible

Test Twitter Browse
    [Documentation]    Browse Twitter/X homepage
    [Tags]    vision    web    twitter    real-scenario
    
    Go To    https://twitter.com/
    Sleep    3s
    
    # Verify homepage elements
    Agent.check    instruction=verify that Sign in button is visible
    
    # Click on Explore
    Run Keyword And Ignore Error    Agent.Do    click on Explore link
    Sleep    2s

Test Reddit Browse Subreddit
    [Documentation]    Browse a subreddit on Reddit
    [Tags]    vision    web    reddit    real-scenario
    
    Go To    https://www.reddit.com/r/robotframework/
    Sleep    3s
    
    # Scroll to see posts
    Agent.Do    scroll down
    Sleep    2s
    
    # Verify posts are visible
    Agent.check    instruction=verify that posts are displayed
    
    # Click on first post
    Agent.Do    click on the first post title
    Sleep    3s
    
    # Verify post opened
    Get Url    should contain    reddit.com/r/robotframework/comments

Test LinkedIn Profile Navigation
    [Documentation]    Navigate LinkedIn homepage
    [Tags]    vision    web    linkedin    real-scenario
    
    Go To    https://www.linkedin.com/
    Sleep    3s
    
    # Verify sign in is available
    Agent.check    instruction=verify that Sign in button is visible
    
    # Click on sign in
    Agent.Do    click on Sign in button
    Sleep    2s
    
    Get Url    should contain    login
