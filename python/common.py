import os

# Convenience class for shared methods

## absolute path helps portability when reading properties files
absolute_path = os.path.dirname(os.path.abspath(__file__))

# Convert values to string or None if blank, supports int, boolean an
def convertToString(str):
    if type(str) is int:
        return "{}".format(str)
    if type(str) is bool:
        return "{}".format(str)
    if str is None:
        return 'None'
    if str == "":
        return 'None'
    return str

# Get the API key from the environment
def getGitHubAPIKey():
    return os.environ['INPUT_GITHUBAPIKEY']
