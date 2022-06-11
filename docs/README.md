[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fergusmacd_github-action-usage&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fergusmacd_github-action-usage)

# GitHub Actions Billable Usage Audit

## Action Use Case

Heavy usage of GitHub Actions (GHA) soon adds up. Once the limits have been reached the workflows will just stop unless
a billing buffer has been set up. This can be extremely disruptive, if say the billing user is on holiday, or hard to
reach. Even worse it's hard for repo owners to see what the usage is as billing info is restricted to admins. GitHub can
send a usage CSV to admins listing every single run but there is too much information to easily isolate heavy usage
repos and wokrflows.

Furthermore, MacOS usage is charged at 10x, Windows 2x the rate of Ubuntu machines. This means that a 7 second action
runtime will be billed as 1 minute on Ubuntu, 10 minutes on MacOS, and 2 minutes on Windows. MacOS builds can take 20-30
minutes and costs can soon build up. The billable values printed out take these proportions into account.

This action was set up to solve the following problems:

- give clear visibility of GitHub Action billing usage to all users
- show total usage per repo
- show total usage per repo and workflow
- show usage by machine type, i.e. Ubuntu, MacOS and Windows

To do this, the GHA prints out two tables:

- total billable usage per repo
- billable usage per repo and workflow

in the prettyprint formatted ASCII tables like this

```
+-------------------------------+--------+-------+---------+
| Repo Name                     | Ubuntu | MacOS | Windows |
+-------------------------------+--------+-------+---------+
| aws-infra                     |   0    |   0   |    0    |
| cicd-images                   |   0    |   0   |    0    |
| terraform-github-repository   |   0    |   0   |    0    |
| ---------                     |  ----  |  ---- |   ----  |
| Total Costs                   |   30   |   0   |    0    |
| ---------                     |  ----  |  ---- |   ----  |
+-------------------------------+--------+-------+---------+

+-------------------------------+---------------------+--------+-------+---------+
| Repo Name                     | Workflow            | Ubuntu | MacOS | Windows |
+-------------------------------+---------------------+--------+-------+---------+
| aws-infra                     | automerge.yml       |   0    |   0   |    0    |
|                               | close-stale-prs.yml |   0    |   0   |    0    |
|                               | enforce-labels.yml  |   0    |   0   |    0    |
|                               | labeler.yml         |   0    |   0   |    0    |
|                               | release.yml         |   0    |   0   |    0    |
|                               | setup-terraform.yml |   0    |   0   |    0    |
| --------                      | --------            | -----  | ----- |  -----  |
| --------                      | --------            | -----  | ----- |  -----  |
| github-audit                  | automerge.yml       |   0    |   0   |    0    |
|                               | close-stale-prs.yml |   15   |   0   |    0    |
|                               | enforce-labels.yml  |   0    |   0   |    0    |
|                               | labeler.yml         |   0    |   0   |    0    |
|                               | release.yml         |   0    |   0   |    0    |
|                               | setup-terraform.yml |   0    |   0   |    0    |
| --------                      | --------            | -----  | ----- |  -----  |
| terraform-github-repository   | No workflows        |        |       |         |
| --------                      | --------            | -----  | ----- |  -----  |
+-------------------------------+---------------------+--------+-------+---------+
```

## Prerequisites to Run as an GH Action

- an organisation or repo secret called `ORGANISATION` with the value of your organisation
- a secret called `GITHUBAPIKEY` with the value being a personal access token (PAT) with scope `read:org` - for public
  repos and `repo:full` - for private repos

## Usage

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
```

For Docker, run from the root directory

```
# from root directory
docker build -t gha-billable-usage .

export LOGLEVEL=debug|info|warning|error
export INPUT_ORGANISATION="myorg"
export INPUT_GITHUBAPIKEY="***"
docker run -v $PWD:/app/results -e LOGLEVEL=${LOGLEVEL} -e INPUT_ORGANISATION=${INPUT_ORGANISATION} -e INPUT_GITHUBAPIKEY=${INPUT_GITHUBAPIKEY} -it gha-billable-usage

```

## Relevant Links

[Billing documentation](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#calculating-minute-and-storage-spending)

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

- alerts when limits are closed to being reached
- export to excel and upload to packages
- sorting by different criteria, e.g. tags or ownership
- test coverage
- colouring console
- any requests?

## Other Notes

My background is technologies other than python. Feel free to suggest better ways of doing things.
