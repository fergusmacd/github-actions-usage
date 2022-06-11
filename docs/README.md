[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fergusmacd_github-action-usage&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fergusmacd_github-action-usage)

# GitHub Actions Billable Minutes

GitHub Actions often take seconds to run but are billable in minutes rounded up. On top of that, MacOS minutes are
multiplied by 10 and Windows minutes multiplied by 2, as per
the [documentation](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#calculating-minute-and-storage-spending)
. This means that a 7 second action runtime will be billed as 1 minute on Ubuntu, 10 minutes on MacOS, and 2 minutes on
Windows. The billable values printed out take these proportions into account.

This GitHub Action prints out two tables:

- total billable usage per repo
- billable usage per repo and workflow

## Prerequisites to Run as an GH Action

- an organisation or repo secret called `ORGANISATION` with the value of your organisation
- a secret called `GITHUBAPIKEY` with the value being a personal access token (PAT) with scope `read:org` - for public
  repos and `repo:full` - for private repos

## Usage

Tested on python 3.9 To make this compatible with running in GHA and locally, we do this

API Key scope:
)

### Running Locally

The docker file and python script can both be run locally in the following ways.

For python, from the python directory

```
pip install -r requirements.txt
# default is warning, see the action.yaml for further details
export LOGLEVEL=debug|info|warning|error
export INPUT_ORGANISATION="myorg"
export INPUT_GITHUBAPIKEY="***"

# from python directory you can run
python main.py

# from root directory try docker
docker build -t gha-costs .

docker run -v $PWD:/app/results -e LOGLEVEL=${LOGLEVEL} -e INPUT_ORGANISATION=${INPUT_ORGANISATION} -e INPUT_GITHUBAPIKEY=${INPUT_GITHUBAPIKEY} -it gha-costs

```

## Relevant Links

The following APIs are used:

- [GitHub Organisation API](https://docs.github.com/en/rest/orgs/orgs#get-an-organization) - to get the number of repos
- [GitHub List Organisational Repos API](https://docs.github.com/en/rest/repos/repos#list-organization-repositories) -
  to get the repo information
- [GitHub List Repository Workflow API](https://docs.github.com/en/rest/actions/workflows#list-repository-workflows) -
  to get the repository workflows
- [GitHub Get Workflow Usage API](https://docs.github.com/en/rest/actions/workflows#get-workflow-usage)

There are plenty of tutorials on prettyprint, I used this one:

- [Zetcode](https://zetcode.com/python/prettytable/)

## Road Map Items

- export to excel and upload to packages
- sorting configuration items
- any requests?

## Other Notes

My background is technologies other than python. Feel free to suggest better ways of doing things.