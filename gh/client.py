import requests
import logging
import json
import gh.gh as gh


class Client:
    def __init__(self, token, working_repo=None, issue_num=None):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }
        self.base_url = "https://api.github.com"
        self.graphql_url = "https://api.github.com/graphql"
        self.issue = gh.Issue(self, working_repo, issue_num)
        self.user = gh.User(self)
        self.repo = gh.Repo(self)
        self.org = gh.Org(self)
        self.enterprise = gh.Enterprise(self)
