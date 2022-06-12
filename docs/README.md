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

### As a GitHub Action

Create a file called `gha-audit.yml` in your workflows directory, paste the following as the contents and you are good
to go

```
name: GHA Billable Audit
on: push
jobs:
  gha-billable-minutes-report:
    runs-on: ubuntu-latest
    steps:
      - name: GitHub Actions Billable Usage Audit
        uses: fergusmacd/github-action-usage@v0.4.0
        # pass user input as arguments
        with:
          organisation: ${{secrets.ORGANISATION}}
          gitHubAPIKey: ${{secrets.GITHUBAPIKEY}} # default token in GitHub Workflow
          loglevel: error # not required, change to debug if misbehaving
```

### Running Locally

The docker file and python script can both be run locally in the following ways.

### Running with Python

For python, from the python directory

```shell
pip install -r requirements.txt
# default is warning, see the action.yaml for further details
# GHA environment variables prepend INPUT_ to values passed in
export INPUT_LOGLEVEL=debug|info|warning|error
export INPUT_ORGANISATION="myorg"
export INPUT_GITHUBAPIKEY="***"

# from python directory you can run
python main.py
```

### Running with Docker

For Docker, run from the root directory

```shell
# from root directory
docker build -t gha-billable-usage .
# GHA environment variables prepend INPUT_ to values passed in
export INPUT_LOGLEVEL=debug|info|warning|error
export INPUT_ORGANISATION="myorg"
export INPUT_GITHUBAPIKEY="***"
docker run -v $PWD:/app/results -e INPUT_LOGLEVEL=${INPUT_LOGLEVEL} -e INPUT_ORGANISATION=${INPUT_ORGANISATION} -e INPUT_GITHUBAPIKEY=${INPUT_GITHUBAPIKEY} -it gha-billable-usage
```

## Common Errors

When problems happen, the best thing to do is set the log level to `debug` like this locally

```shell
export LOGLEVEL="debug"
```

Or change the loglevel input in the GHA

The following one happens when running locally and the `INPUT_GITHUBAPIKEY` environment variable has not been exported

```shell
python3 main.py
Traceback (most recent call last):
  File "/github-action-usage/python/main.py", line 5, in <module>
    from ghaworkflows import *
  File "/github-action-usage/python/ghaworkflows.py", line 9, in <module>
    github_api_key = getgithubapikey()
  File "/github-action-usage/python/common.py", line 24, in getgithubapikey
    return os.environ['INPUT_GITHUBAPIKEY']
  File "/usr/local/Cellar/python@3.9/3.9.12/Frameworks/Python.framework/Versions/3.9/lib/python3.9/os.py", line 679, in __getitem__
    raise KeyError(key) from None
KeyError: 'INPUT_GITHUBAPIKEY'

```

This error happens when the PAT has expired or does not have sufficient permissions

```shell
python3 main.py                                                     
Traceback (most recent call last):
  File "/github-action-usage/python/main.py", line 92, in <module>
    main()
  File "/github-action-usage/python/main.py", line 30, in main
    repoNames = getreposfromorganisation(org)
  File "/github-action-usage/python/ghorg.py", line 27, in getreposfromorganisation
    totalPrivateRepos = json_data["total_private_repos"]
KeyError: 'total_private_repos'
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
- test scripts
- colouring console
- any requests?

## Other Notes

My background is technologies other than python. Feel free to suggest better ways of doing things.