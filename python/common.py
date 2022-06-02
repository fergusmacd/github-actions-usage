import os

# Convenience class for shared methods

# absolute path helps portability when reading properties files
absolute_path = os.path.dirname(os.path.abspath(__file__))


# Convert values to string or None if blank, supports int, boolean an
def converttostring(value):
    if type(value) is int:
        return "{}".format(value)
    if type(value) is bool:
        return "{}".format(value)
    if value is None:
        return 'None'
    if value == "":
        return 'None'
    return value


# Get the API key from the environment
def getgithubapikey():
    return os.environ['INPUT_GITHUBAPIKEY']
