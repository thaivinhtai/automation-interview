*** Settings ***
Library  automation_libs.github_api.GithubAPIForSeleniumHQ


*** Test Cases ***
Retrieve information from Github SeleniumHQ
    ${total_open_issue}     get total open issues
    ${list_repo}            get list repo name sorted desc by updated date
    ${most_watchers_repo}   get the most watchers repo

    log to console          ===============================================
    log to console          The total open issues: ${total_open_issue}
    log to console          ===============================================
    log to console          List repos sorted desc:

    FOR     ${repo}     IN      @{list_repo}
        log to console   ${repo.get("repo_full_name")} - ${repo.get("updated_at")}
    END

    log to console          ===============================================
    log to console          The most watchers repo is: ${most_watchers_repo}
