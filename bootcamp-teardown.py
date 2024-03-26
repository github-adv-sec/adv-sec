from gh import client, comments
import sys
import os
import logging
import yaml
import re
import time


# Get Arguments
working_repo = sys.argv[1]
issue_num = sys.argv[2]

# Get Environment Variables
github_token = os.environ.get("GITHUB_TOKEN")
admin_token = os.environ.get("ADMIN_TOKEN")

# Setup clients
admin_client = client.Client(admin_token)

logging.info("Starting bootcamp teardown")
logging.info(f"Working repo: {working_repo}")


# Read config file
def get_config(config_file):
    with open(config_file, "r") as stream:
        try:
            return yaml.safe_load(stream)["bootcamp-teardown"]
        except yaml.YAMLError as e:
            logging.error(e)
            sys.exit(1)


# read the org name from the comment.  WARNING: this is fragile.
def get_org_names(json_obj):
    org_names = []
    for comment in json_obj:
        if comment["user"]["login"] == "github-actions[bot]":
            body = comment["body"]
            matches = re.findall(r"\| \S+ \| [✅❌] \| \[(\S+)\]", body)
            org_names.extend(matches)
    return org_names


def delete_orgs(org_names):
    state = {"error_count": 0, "success": [], "fail": []}
    for org in org_names:
        try:
            admin_client.org.delete(org)
            state["success"].append(org)
            time.sleep(5)
        except:
            state["error_count"] += 1
            state["fail"].append(org)
            pass
    return state


def main():
    # Get config
    config = get_config("config.yml")
    for key, value in config.items():
        logging.info(f"{key}: {value}")

    # Manual delete
    if issue_num != "0":
        issue_ops_client = client.Client(github_token, working_repo, issue_num)
        issue_comments = issue_ops_client.issue.get_comments()
        org_names = get_org_names(issue_comments)
        state = delete_orgs(org_names)
        issue_ops_client.issue.add_comment(
            comments.teardown_complete
            + "### Deleted Orgs: \n\n"
            + "\n".join(state["success"])
            + "\n\n### Failures: \n\n"
            + "\n".join(state["fail"])
        )
        issue_ops_client.issue.apply_label(config["labels"]["done"])
        issue_ops_client.issue.close()

    # Get all open issues
    # elif issue_num == '0':
    #     open_issues = issue_ops_client.issue.get(config['labels']['open'])
    #     for issue in open_issues:
    #         issue_ops_client = client.Client(github_token, working_repo, issue['number'])
    #         issue_comments = issue_ops_client.issue.get_comments()
    #         org_names = get_org_names(issue_comments)
    #         state = delete_orgs(org_names)
    #         issue_ops_client.issue.add_comment(comments.teardown_complete + "### Deleted Orgs: \n\n" + '\n'.join(state['success']) + "\n\n### Failures: \n\n" + '\n'.join(state['fail']))
    #         issue_ops_client.issue.apply_label(config['labels']['done'])
    #         issue_ops_client.issue.close()
    #         time.sleep(5)

    # Compare issue creation date to today's date

    # evaluate if difference is = to or > the config days\

    # For each issue that meets the criteria, delete the orgs

    # Add comment to issue with orgs deleted


if __name__ == "__main__":
    main()
