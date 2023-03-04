"""
EXTRACT_LICENSES:
uses pip-licenses to collect all licenses.
All the licenses that can are not collected by pip-licenses are downloaded from official repositories.
"""

import os
import sys
import json
import subprocess

import urllib.request

using_pyinstaller = True


def resource_exists(t_url):
    """
    Returns True when an online resource exists.

    :param str t_url: URL of the resource to check
    """
    res = urllib.request.urlopen(t_url)
    return res.getcode() == 200


original_cwd = os.path.abspath(os.getcwd())
script_dir = os.path.dirname(os.path.realpath(__file__))

known_packages = [  # package name and license URL
    ("pygraphviz", "https://raw.githubusercontent.com/pygraphviz/pygraphviz/main/LICENSE")
]

possible_license_url_combinations = [  # URL structure
    ("Author", "Name", "LICENSE"),     # example: url is made of <package author>, <package name>, "LICENSE" where "LICENSE" is the file name
    ("Name", "Name", "LICENSE"),
    ("Author", "Name", "license"),
    ("Name", "Name", "license"),
    ("Author", "Name", "LICENSE.txt"),
    ("Name", "Name", "LICENSE.txt"),
    ("Author", "Name", "license.txt"),
    ("Name", "Name", "license.txt"),
]


if __name__ == "__main__":

    os.chdir(script_dir)

    retcode = subprocess.call(
        [
            "pip-licenses",
            "--from=mixed",
            "--format=markdown",
            "--with-urls",
            "--output-file=brief_licenses.md"
        ],
        shell=True
    )

    if retcode != 0:
        print("ERROR: Couldn't create brief_licenses.md file using pip-licenses")
        sys.exit(retcode)

    retcode = subprocess.call(
        [
            "pip-licenses",
            "--from=mixed",
            "--format=json",
            "--with-urls",
            "--with-authors",
            "--with-license-file",
            "--no-license-path",
            "--with-notice-file",
            "--output-file=licenses.json"
        ],
        shell=True
    )

    if retcode != 0:
        print("ERROR: Couldn't create licenses.json file using pip-licenses")
        sys.exit(retcode)

    with open("licenses.json", "r") as f:
        licenses = json.load(f)

    if not os.path.exists("third-party"):
        os.mkdir("third-party")

    if using_pyinstaller:
        urllib.request.urlretrieve("https://raw.githubusercontent.com/pyinstaller/pyinstaller/master/doc/license.rst", os.path.join("third-party", "PyInstaller_license.txt"))
        urllib.request.urlretrieve("https://raw.githubusercontent.com/python/cpython/main/LICENSE", os.path.join("third-party", "CPython_license.txt"))

    for license in licenses:
        filename = "{}-{}_license.txt".format(license["Name"], license["Version"])
        dest_folder = "third-party"
        dest_path = os.path.join(dest_folder, filename)

        if license["License"] not in ["MIT License", "BSD License"]:
            print("WARNING: Found a '{}' license. Please check the {} file to make sure that you are allowed to share this library".format(license["License"], filename))

        if license["URL"] == "UNKNOWN":
            print("WARNING: '{}' package has NO URL".format(license["Name"]))

        if license["Name"] == "packaging":
            urllib.request.urlretrieve("https://raw.githubusercontent.com/pypa/packaging/main/LICENSE.APACHE", os.path.join(dest_folder, "LICENSE.APACHE"))
            urllib.request.urlretrieve("https://raw.githubusercontent.com/pypa/packaging/main/LICENSE.BSD", os.path.join(dest_folder, "LICENSE.BSD"))

        with open(dest_path, "w") as f:
            if license["LicenseText"] != "UNKNOWN":
                f.write(license["LicenseText"])
                continue

        print("WARNING: license not found for package {}...".format(license["Name"]), end="")

        found = False
        for package in known_packages:
            if license["Name"] == package[0]:
                print("This is a known package: downloading license from source")
                urllib.request.urlretrieve(package[1], dest_path)
                found = True
                break

        if found:
            continue

        if "github.com" in license["URL"]:
            github_license_url = "https://raw.githubusercontent.com/{}/{}/main/{}"
            found = False
            for combination in possible_license_url_combinations:
                if resource_exists(
                    github_license_url.format(
                        license[combination[0]],
                        license[combination[1]],
                        combination[2]
                    )
                ):
                    urllib.request.urlretrieve(
                        github_license_url.format(
                            license[combination[0]],
                            license[combination[1]],
                            combination[2]
                        ),
                        filename
                    )
                    found = True
                    break

            if found:
                print("Downloaded license from GitHub source")
                continue

        print("Unable to Download license from source")

    if using_pyinstaller:
        with open("brief_licenses.md", "a") as f:
            f.write("\n")
            f.write("| CPython (>= 3.7)  | ------- | Python Software Foundation License                 | https://www.python.org/                    |\n")
            f.write("| PyInstaller       | ------- | GPL 2.0 (exception on output bundles)              | https://github.com/pyinstaller/pyinstaller |\n")

        print("WARNING: Remember to share the license of your software")

    os.chdir(original_cwd)
