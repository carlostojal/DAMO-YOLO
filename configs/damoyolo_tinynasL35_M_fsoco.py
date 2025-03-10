#!/usr/bin/env python3

import os

from damo.config import Config as MyConfig


class Config(MyConfig):
    def __init__(self):
        super(Config, self).__init__()

        self.miscs.exp_name = os.path.split(
            os.path.realpath(__file__))[1].split('.')[0]
        self.miscs.eval_interval_epochs = 3
        self.miscs.ckpt_interval_epochs = 2
        # optimizer
        self.train.batch_size = 6
        self.train.base_lr_per_img = 0.01 / 64
        self.train.min_lr_ratio = 0.05
        self.train.weight_decay = 5e-4
        self.train.momentum = 0.9
        self.train.no_aug_epochs = 2
        self.train.warmup_epochs = 1
        self.train.total_epochs = 15

        # augment
        self.train.augment.transform.image_max_range = (640, 640)
        self.train.augment.mosaic_mixup.mixup_prob = 0.15
        self.train.augment.mosaic_mixup.degrees = 10.0
        self.train.augment.mosaic_mixup.translate = 0.2
        self.train.augment.mosaic_mixup.shear = 2.0
        self.train.augment.mosaic_mixup.mosaic_scale = (0.1, 2.0)

        self.dataset.train_ann = ('fsoco_train_coco', )
        self.dataset.val_ann = ('fsoco_val_coco', )

        # backbone
        structure = self.read_structure(
            './damo/base_models/backbones/nas_backbones/tinynas_L35_kxkx.txt')
        TinyNAS = {
            'name': 'TinyNAS_csp',
            'net_structure_str': structure,
            'out_indices': (2, 3, 4),
            'with_spp': True,
            'use_focus': True,
            'act': 'silu',
            'reparam': True,
        }

        self.model.backbone = TinyNAS

        GiraffeNeckV2 = {
            'name': 'GiraffeNeckV2',
            'depth': 1.5,
            'hidden_ratio': 1.0,
            'in_channels': [128, 256, 512],
            'out_channels': [128, 256, 512],
            'act': 'silu',
            'spp': False,
            'block_name': 'BasicBlock_3x3_Reverse',
        }

        self.model.neck = GiraffeNeckV2

        ZeroHead = {
            'name': 'ZeroHead',
            'num_classes': 5,
            'in_channels': [128, 256, 512],
            'stacked_convs': 0,
            'reg_max': 16,
            'act': 'silu',
            'nms_conf_thre': 0.05,
            'nms_iou_thre': 0.7,
            'legacy': False,
        }
        self.model.head = ZeroHead

        self.dataset.class_names = ['unknown_cone', 'yellow_cone', 'blue_cone', 'orange_cone', 'large_orange_cone']
