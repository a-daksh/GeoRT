# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
from pathlib import Path

_DEXTERLAB_GEORT_DIR = Path.home() / ".dexterlab" / "geort"


def get_package_root():
    return Path(os.path.dirname(os.path.realpath(__file__))).parent.resolve()


def to_package_root(path):
    """Resolve a path relative to the geort package directory."""
    return get_package_root() / path


def get_data_root():
    data_dir = _DEXTERLAB_GEORT_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_checkpoint_root():
    checkpoint_dir = _DEXTERLAB_GEORT_DIR / "checkpoint"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    return checkpoint_dir


def get_human_data_output_path(human_data):
    return get_data_root() / human_data


def get_human_data(name):
    data_root = get_data_root()
    for data_name in os.listdir(data_root):
        if name in data_name:
            return data_root / data_name


if __name__ == '__main__':
    print(get_package_root())
    print(get_human_data_output_path("human"))
