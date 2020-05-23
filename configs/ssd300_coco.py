# model settings
input_size = 300
model = dict(
  type='SingleStageDetector',
  pretrained='open-mmlab://vgg16_caffe',
  backbone=dict(
    type='SSDVGG',
    input_size=input_size,
    depth=16,
    with_last_pool=False,
    ceil_mode=True,
    out_indices=(3, 4),
    out_feature_indices=(22, 34),
    l2_norm_scale=20),
  neck=None,
  bbox_head=dict(
    type='SSDHead',
    in_channels=(512, 1024, 512, 256, 256, 256),
    num_classes=80,
    anchor_generator=dict(
      type='SSDAnchorGenerator',
      scale_major=False,
      input_size=input_size,
      basesize_ratio_range=(0.15, 0.9),
      strides=[8, 16, 32, 64, 100, 300],
      ratios=[[2], [2, 3], [2, 3], [2, 3], [2], [2]]),
    bbox_coder=dict(
      type='DeltaXYWHBBoxCoder',
      target_means=[.0, .0, .0, .0],
      target_stds=[0.1, 0.1, 0.2, 0.2])))
cudnn_benchmark = True
train_cfg = dict(
  assigner=dict(
    type='MaxIoUAssigner',
    pos_iou_thr=0.5,
    neg_iou_thr=0.5,
    min_pos_iou=0.,
    ignore_iof_thr=-1,
    gt_max_assign_all=False),
  smoothl1_beta=1.,
  allowed_border=-1,
  pos_weight=-1,
  neg_pos_ratio=3,
  debug=False)
test_cfg = dict(
  nms=dict(type='nms', iou_thr=0.45),
  min_bbox_size=0,
  score_thr=0.02,
  max_per_img=200)

img_norm_cfg = dict(mean=[123.675, 116.28, 103.53], std=[1, 1, 1], to_rgb=True)
test_pipeline = [
  dict(type='LoadImageFromFile'),
  dict(
    type='MultiScaleFlipAug',
    img_scale=(300, 300),
    flip=False,
    transforms=[
      dict(type='Resize', keep_ratio=False),
      dict(type='Normalize', **img_norm_cfg),
      dict(type='ImageToTensor', keys=['img']),
      dict(type='Collect', keys=['img']),
    ])
]

data = dict(
  samples_per_gpu=8,
  workers_per_gpu=3,
  val=dict(pipeline=test_pipeline),
  test=dict(pipeline=test_pipeline))
