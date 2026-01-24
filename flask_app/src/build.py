from pybuilder.core import use_plugin, init  # type: ignore

use_plugin("python.core")
use_plugin("python.flake8")
#use_plugin("python.coverage")
use_plugin("python.distutils")

name = "wednesdays-wicked-adventures"
default_task = ["publish"]


@init
def set_properties(project):
    # source layout
    project.set_property("dir_source_main_python", "src/main")

    # verbosity
    project.set_property("verbose", True)

    # dependency handling
    project.set_property("install_dependencies", True)
    project.set_property("requirements_file", "requirements.txt")

    # flake8
    project.set_property("flake8_break_build", False)

    # packaging
    project.set_property("distutils_packages", ["app"])
    project.set_property(
        "distutils_classifiers",
        [
            "Programming Language :: Python :: 3",
            "Framework :: Flask",
        ],
    )
