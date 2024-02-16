from github import Github
from github import Auth
import requests

def git_auth(auth):

# Authentication is defined via github.Auth
# using an access token
    gh = Github(auth=auth)
    # Then play with your Github objects:
    #for repo in my_git.get_user().get_repos():
    #    print(repo.name)
    return(gh)

#  This should be an access token for your github repo
auth = Auth.Token("YOUR ACCESS TOKEN HERE")

my_git = git_auth(auth)

for repo in my_git.get_user().get_repos():
        print(repo.name)
