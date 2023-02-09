#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Github API Object for SeleniumHQ
"""

from framework_modules.fundamental_auto_libs.api_util import \
    send_request_and_receive_response
from datetime import datetime

from test_data.common_variables import GITHUB_ORG


class GithubAPIForSeleniumHQ:
    """

    """

    __host = "https://api.github.com"
    __organization_endpoint = __host + "/orgs/{}"
    __common_headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    __organization_issue_endpoint = __organization_endpoint + "/issues"
    __organization_repos_endpoint = __organization_endpoint + "/repos"

    def get_org_info(self, org_name: str = GITHUB_ORG) -> dict:
        """Get Organization info.

        Parameters
        ----------
        org_name : str
            Organization's name.

        Returns
        -------
        dict
        """
        response = send_request_and_receive_response(
            method="GET", headers=self.__common_headers,
            uri=self.__organization_endpoint.format(org_name)
        )
        if response.get("status_code") == 200:
            return response.get("message")
        return {}

    def get_all_public_repos_of_org(self, org_name: str = GITHUB_ORG) -> dict:
        """Get all public repos of the organization.

        Parameters
        ----------
        org_name : str
            Organization's name.

        Returns
        -------
        dict
        """
        response = send_request_and_receive_response(
            method="GET", headers=self.__common_headers,
            uri=self.__organization_repos_endpoint.format(org_name)
        )
        if response.get("status_code") == 200:
            return response.get("message")
        return {}

    def get_total_open_issues(self, org_name: str = GITHUB_ORG) -> int:
        """Get total open issues of the organization.

        Parameters
        ----------
        org_name : str
            The Organization's name.

        Returns
        -------
        int
            Total open issues.
        """
        public_repos = self.get_all_public_repos_of_org(org_name)
        total_open_issues = 0
        for repo in public_repos:
            total_open_issues += repo.get("open_issues")
        return total_open_issues

    def get_list_repo_name_sorted_desc_by_updated_date(
            self, org_name: str = GITHUB_ORG) -> list:
        """Get list repo name sorted desc by updated date of the organization.

        Parameters
        ----------
        org_name : str
            Organization name.

        Returns
        -------
        list
        """
        strtime_format = "%Y-%m-%dT%H:%M:%SZ"
        public_repos = self.get_all_public_repos_of_org(org_name)
        list_repos = [{
            "repo_full_name": public_repo.get("full_name"),
            "updated_at": public_repo.get("updated_at")
        } for public_repo in public_repos]
        list_repos.sort(
            key=lambda element_: datetime.strptime(
                element_.get("updated_at"), strtime_format
            ),
            reverse=True
        )
        return list_repos

    def get_the_most_watchers_repo(self, org_name: str = GITHUB_ORG) -> dict:
        """Get the most watchers repo.

        Parameters
        ----------
        org_name : str
            Organisation's name.

        Returns
        -------
        dict
        """
        public_repos = self.get_all_public_repos_of_org(org_name)
        result = {
            "repo_full_name": public_repos[0].get("full_name"),
            "number_of_watchers": public_repos[0].get("watchers")
        }
        for repo in public_repos[1:]:
            if repo.get("watchers") > result.get("number_of_watchers"):
                result["repo_full_name"] = repo.get("full_name")
                result["number_of_watchers"] = repo.get("watchers")
        return result


if __name__ == "__main__":
    github_api = GithubAPIForSeleniumHQ()
    # github_api.get_org_info()
    print(github_api.get_total_open_issues())
    for element in github_api.get_list_repo_name_sorted_desc_by_updated_date():
        print(element)
    print(datetime.strptime("2023-02-08T03:36:43Z", "%Y-%m-%dT%H:%M:%SZ")
          <= datetime.strptime("2022-10-08T07:54:07Z", "%Y-%m-%dT%H:%M:%SZ"))
