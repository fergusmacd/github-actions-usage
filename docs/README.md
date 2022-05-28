# GitHub Actions Costs

GitHub action that calculates GitHub action costs for all repos and writes to Excel

## Usage

Tested on python 3.9 To make this compatible with running in GHA and locally, we do this

```
pip install -r requirements.txt

export LOGLEVEL=debug|info|warning|error
export INPUT_ORGANISATION="myorg"
export INPUT_GITHUBAPIKEY="***"
# from python directory you can run
python main.py

# from root directory try docker
docker build -t gha-costs .

docker run -v $PWD:/app/results -e LOGLEVEL=${LOGLEVEL} -e INPUT_ORGANISATION=${INPUT_ORGANISATION} -e INPUT_GITHUBAPIKEY=${INPUT_GITHUBAPIKEY} -it gha-costs

```
