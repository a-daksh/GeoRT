# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
from pathlib import Path

_ROOT = Path(os.environ.get("GEORT_DATA_ROOT", Path.home() / ".dexterlab" / "geort"))


def get_package_root() -> Path:
    return Path(os.path.dirname(os.path.realpath(__file__))).parent.resolve()


def to_package_root(path) -> Path:
    return get_package_root() / path


def get_robot_data_root() -> Path:
    p = _ROOT / "robot"
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_user_dir(user: str) -> Path:
    p = _ROOT / "users" / user
    p.mkdir(parents=True, exist_ok=True)
    return p
