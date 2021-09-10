import configparser
import traceback

github_repository_url = "https://github.com/mario33881/blif2graph"


def show_error(t_err):
    """
    Shows the "please, report this to the developer" message.
    :param Exception t_err: error from which to extract the traceback
    """
    print("\nTraceback:\n")
    traceback.print_tb(t_err.__traceback__)
    print("")
    type_of_error = type(t_err)
    print(type_of_error.__name__, str(t_err))

    print("\nPlease, (if someone didn't post this error already) create a Github Issue here: '{}'\n"
          "to help the developer to fix the problem\n".format(github_repository_url + "/issues"))


def parse_styles_file(t_filepath):
    """
    Parses the INI style file and 
    returns the content as a dictionary.

    :param str t_filepath: INI style file path
    :return dict parsed_styles: <t_filepath> file content as a dictionary
    """
    config = configparser.ConfigParser()
    config.read(t_filepath)

    parsed_styles = {}
    for section in config.sections():
        parsed_styles[section] = {}
        for key in config[section]:
            parsed_styles[section][key] = config[section][key]
    
    return parsed_styles
