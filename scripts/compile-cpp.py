"""
build the cmake project, compile the code and install into local site-packages dir
"""

import subprocess
import sys
from pathlib import Path

_repo = Path(__file__).parent.parent
_site_packages = next((Path(sys.executable).parent.parent / "lib").glob("python*")) / "site-packages"


def main():
    subprocess.check_call(
        [
            "cmake",
            "-S",
            str(_repo),
            "-B",
            "cmake-build-release",
        ]
    )

    subprocess.check_call(
        [
            "cmake",
            "--build",
            "cmake-build-release",
            "-j",
            "8",
        ]
    )

    subprocess.check_call(
        [
            "cmake",
            "--install",
            "cmake-build-release",
            "--prefix",
            str(_site_packages),
        ]
    )


if __name__ == "__main__":
    main()
