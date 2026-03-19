#!/usr/bin/env python3
import os
import pathlib

import PySide6
import shiboken6
from auditwheel.main import main
from auditwheel.policy import _POLICY_JSON_MAP as POLICY_JSON_MAP

if __name__ == "__main__":
    os.environ["LD_LIBRARY_PATH"] += f";{pathlib.Path(shiboken6.__file__).parent}"
    os.environ["LD_LIBRARY_PATH"] += f";{pathlib.Path(PySide6.__file__).parent}"
    print(f"LD_LIBRARY_PATH for auditwheel: {os.environ["LD_LIBRARY_PATH"]}")
    main()
