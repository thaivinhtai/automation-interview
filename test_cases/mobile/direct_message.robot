*** Settings ***
Resource  ../../automation_libs/robot_bdd_keywords/app_bdd_keywords.robot


*** Test Cases ***
Verify sending a direct message in the mobile app

    Given The user logs in to the mobile app
    When The user starts a new chat and send a message
    Then The message should be sent
