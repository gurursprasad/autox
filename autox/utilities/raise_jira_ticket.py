import os

import requests
from jira import JIRA

from autox.aws.aws_ec2_util import get_public_ip


def get_app_version_info():
    head_node_url = get_public_ip()
    api_url = f"http://{head_node_url}:5000/v1/info"
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    return response_data["Manifest"]["appVersion"]


def create_jira_issue_with_attachment(
    server_url, username, password, project_key, summary, description, issue_type, attachment_paths
):
    jira_options = {"server": server_url}
    jira = JIRA(options=jira_options, basic_auth=(username, password))

    issue_dict = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
        "labels": ["automated-bug"],
    }
    issue = jira.create_issue(fields=issue_dict)

    for path in attachment_paths:
        if os.path.isfile(path):
            with open(path, "rb") as file:
                jira.add_attachment(issue=issue, attachment=file)
        else:
            print(f"File not found: {path}")

    print(f"Issue {issue.key} created and attachments uploaded.")
    return issue


# if __name__ == "__main__":
#     SERVER_URL = "https://atlassian.net/"
#     USERNAME = "gurursprasad@gmail.com"
#     PASSWORD = "jkfdhsjkjfds"  # Use API token instead of password for security

#     PROJECT_KEY = "X" # id: 1 # X Top Level
#     SUMMARY = "<<Automation - Example bug summary>>"
#     DESCRIPTION = "Detailed description of the bug."
#     ISSUE_TYPE = "Bug"

#     ATTACHMENT_PATHS = ["/home/ubuntu/automated_tests/compute_tests/pytest/test/report.html"]

#     create_jira_issue_with_attachment(SERVER_URL, USERNAME, PASSWORD, PROJECT_KEY, SUMMARY, DESCRIPTION, ISSUE_TYPE, ATTACHMENT_PATHS)
