import os
import torch
# 0. pt模型下载及初始化
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
model.eval()

x = torch.randn(1, 3, 640, 640)
y = torch.randn(1, 3, 320, 320)

model(x, y)
# 1. pt-->torchscript
traced_script_module = torch.jit.trace(model, (x, y))
traced_script_module.save("ts.pt")

# 2. ts --> pnnx --> ncnn
os.system("pnnx ts.pt inputshape=[1,3,640,640] inputshape2=[1,3,320,320]")
# os.system("pnnx ts.pt")

# 3. ncnn ---> optmize---->ncnn
os.system("ncnnoptimize ts.ncnn.param ts.ncnn.bin opt.param opt.bin 1")  # 数字0 代表fp32 ；1代表fp16

# 如果急用，请参考nihui写的教程进行转换。------》https://zhuanlan.zhihu.com/p/471357671
# 上述步骤执行后报错：
# 报错内容如下：
# ```log
# ############# pass_level1
# no attribute value
# unknown Parameter value kind prim::Constant
# no attribute value
# no attribute value
# no attribute value
# ############# pass_level2
# ############# pass_level3
# assign unique operator name pnnx_unique_0 to model.model.model.0.conv
# assign unique operator name pnnx_unique_1 to model.model.model.9.m
# assign unique operator name pnnx_unique_2 to model.model.model.9.m
# ############# pass_level4
# ############# pass_level5
# ############# pass_ncnn
# insert_reshape_pooling 4
# insert_reshape_pooling 4
# insert_reshape_pooling 4
# create_custom_layer aten::type_as
# model has custom layer, shape_inference skipped
# model has custom layer, estimate_memory_footprint skipped
# ```
# c++运行后报错：
# ```
# layer aten::type_as not exists or registered
# ```
