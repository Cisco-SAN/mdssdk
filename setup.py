import os
import re
import shutil
import stat

from setuptools import setup, find_packages
from setuptools.command.install import install

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as rf:
    requirements = rf.readlines()

with open("HISTORY.rst") as history_file:
    history = history_file.read().replace(".. :changelog:", "")

def find_version(*file_paths):
    """
    This pattern was modeled on a method from the Python Packaging User Guide:
        https://packaging.python.org/en/latest/single_source_version.html
    We read instead of importing so we don't get import errors if our code
    imports from dependencies listed in install_requires.
    """
    base_module_file = os.path.join(*file_paths)
    with open(base_module_file) as f:
        base_module_data = f.read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", base_module_data, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        SDK_TEMPLATE_PATH = os.path.expanduser("~") + "/mdssdk-templates/"
        self.copytree("templates/", SDK_TEMPLATE_PATH)
        os.environ["NET_TEXTFSM"] = SDK_TEMPLATE_PATH
        exportcmd = "export NET_TEXTFSM=" + SDK_TEMPLATE_PATH
        os.system(exportcmd)
        print("\nPLEASE NOTE: \n"
              "- 'mdssdk' requires NET_TEXTFSM environment variable to be set\n"
              "- This variable points to the directory where the textfsm templates are copied to\n"
              "- Currently the templates are copied to - " + SDK_TEMPLATE_PATH + "\n"
              "- This variable is automatically set when you install 'mdssdk'\n"
              "- Its recommended that you add this env permanently into your .bashrc file\n"
              "- This can be done by adding the below line to your .bashrc file\n"
              + exportcmd + "\n")

    # From : https://stackoverflow.com/a/22331852
    def copytree(self, src, dst, symlinks=False, ignore=None):
        if not os.path.exists(dst):
            os.makedirs(dst)
            shutil.copystat(src, dst)
        lst = os.listdir(src)
        if ignore:
            excl = ignore(src, lst)
            lst = [x for x in lst if x not in excl]
        for item in lst:
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if symlinks and os.path.islink(s):
                if os.path.lexists(d):
                    os.remove(d)
                os.symlink(os.readlink(s), d)
                try:
                    st = os.lstat(s)
                    mode = stat.S_IMODE(st.st_mode)
                    os.lchmod(d, mode)
                except:
                    pass  # lchmod not available
            elif os.path.isdir(s):
                self.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)


setup(
    name="mdssdk",
    version=find_version("mdssdk", "__init__.py"),
    description="Python SDK for Cisco MDS Switches",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author="Cisco Systems, Inc.",
    author_email="subharad@cisco.com",
    packages=find_packages(exclude=("test",)),
    url="https://github.com/Cisco-SAN/mdslib",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    cmdclass={
        "install": PostInstallCommand,
    },
)
