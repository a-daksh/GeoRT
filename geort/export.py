# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import torch
from geort.formatter import HandFormatter
from geort.model import IKModel
from geort.utils.path import get_user_dir
from geort.utils.config_utils import load_json, parse_config_keypoint_info, parse_config_joint_limit


class GeoRTRetargetingModel:
    def __init__(self, model_path, config_path):
        config = load_json(config_path)
        keypoint_info = parse_config_keypoint_info(config)
        joint_lower_limit, joint_upper_limit = parse_config_joint_limit(config)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.human_ids = keypoint_info["human_id"]
        self.model = IKModel(keypoint_joints=keypoint_info["joint"]).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        self.qpos_normalizer = HandFormatter(joint_lower_limit, joint_upper_limit)

    def forward(self, keypoints):
        keypoints = keypoints[self.human_ids]
        t = torch.from_numpy(keypoints).unsqueeze(0).reshape(1, -1, 3).float().to(self.device)
        joint_normalized = self.model.forward(t)
        return self.qpos_normalizer.unnormalize(joint_normalized.detach().cpu().numpy())[0]


def load_model(user: str, hand: str, epoch: int = 0) -> GeoRTRetargetingModel:
    checkpoint_dir = get_user_dir(user) / f"{hand}_checkpoint"
    model_path = checkpoint_dir / (f"epoch_{epoch}.pth" if epoch > 0 else "last.pth")
    config_path = checkpoint_dir / "config.json"
    return GeoRTRetargetingModel(model_path=model_path, config_path=config_path)
