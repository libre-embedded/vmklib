# =====================================
# generator=datazen
# version=3.2.3
# hash=46e31ace55883ec4b2cd35e03c1f061e
# =====================================

"""
vmklib - Package definition for distribution.
"""

# third-party
try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from vmklib_bootstrap.setup import setup  # type: ignore

# internal
from vmklib import DESCRIPTION, PKG_NAME, VERSION

author_info = {
    "name": "Libre Embedded",
    "email": "vaughn@libre-embedded.com",
    "username": "libre-embedded",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.12",
        "3.13",
    ],
}
setup(
    pkg_info,
    author_info,
)
