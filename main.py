import os
import shutil
import random

# 定义输入输出目录和各个风格的比例
# 照片(1670张),艺术画(2048张),动画片(2344张)和素描(3929张)
photo = 1670
art_painting = 2048
cartoon = 2344
sketch = 3929
input_dir = "/content/gdrive/MyDrive/data/PACS_test_1_pic/PACS"
output_dir = "/content/gdrive/MyDrive/data/PACS_train"
# Art painting: 2048 Cartoon: 678 Photo: 678 Sketch: 784
# Sketch: 3929 Art painting: 1217 Cartoon: 1238 Photo: 331
# Photo: 1670 Art painting: 551 Sketch: 538 Cartoon: 466
# Cartoon: 2344 Photo: 776 Sketch: 761 Art painting: 407
train_style_amount = {"art_painting": 2048, "cartoon": 678, "photo": 678, "sketch": 0}
val_style_amount = {"art_painting": 407, "cartoon": 466, "photo": 776, "sketch": 761}
test_style_amount = {"art_painting": 0, "cartoon": 0, "photo": 0, "sketch": 784}
train_style_ratios = {"art_painting": train_style_amount["art_painting"] / art_painting,
                      "cartoon": train_style_amount["cartoon"] / cartoon,
                      "photo": train_style_amount["photo"] / photo,
                      "sketch": train_style_amount["sketch"] / sketch}
val_style_ratios = {"art_painting": val_style_amount["art_painting"] / art_painting,
                    "cartoon": val_style_amount["cartoon"] / cartoon,
                    "photo": val_style_amount["photo"] / photo,
                    "sketch": val_style_amount["sketch"] / sketch}
test_style_ratios = {"art_painting": test_style_amount["art_painting"] / art_painting,
                     "cartoon": test_style_amount["cartoon"] / cartoon,
                     "photo": test_style_amount["photo"] / photo,
                     "sketch": test_style_amount["sketch"] / sketch}
# train_style_ratios = {"art_painting": , "cartoon": 0.1, "photo": 0.1, "sketch": 0.0}
# val_style_ratios = {"art_painting": 0.2, "cartoon": 0.1, "photo": 0.1, "sketch": 0.6}
# test_style_ratios = {"art_painting": 0.0, "cartoon": 0.0, "photo": 0.0, "sketch": 1.0}
styles = ["art_painting", "cartoon", "photo", "sketch"]

######################################### 是否需要清空输出目录 #########################################
# 清空输出目录
weather_clear = True


def copyd(inputdir, outputdir, ratios):
    # 创建输出目录
    if not os.path.exists(outputdir):
        print("\nCreat {}...\n".format(outputdir))
        os.makedirs(outputdir)

    if weather_clear:
        # 清空输出目录
        print("\nClear {}...\n".format(outputdir))
        for label in os.listdir(outputdir):
            label_dir = os.path.join(outputdir, label)
            shutil.rmtree(label_dir)

    # 遍历每个标签文件夹，并将符合比例的照片复制到输出目录中
    for style in styles:
        # 获取当前风格的目录和比例
        print("Copying {}...".format(style))
        style_dir = os.path.join(input_dir, style)
        style_ratio = ratios[style]
        print("Ratio: {}".format(style_ratio))

        # 遍历每个标签文件夹
        for label in os.listdir(style_dir):
            print("Copying {} in style {}...".format(label, style))
            label_dir = os.path.join(style_dir, label)
            output_label_dir = os.path.join(outputdir, label)
            if not os.path.exists(output_label_dir):
                os.makedirs(output_label_dir)

            # 遍历当前标签文件夹下的所有照片，并按照比例随机选择
            photo_list = os.listdir(label_dir)
            select_count = int(len(photo_list) * style_ratio)
            selected_photos = random.sample(photo_list, select_count)
            i = 0
            # 将选中的照片复制到输出目录中
            for photo_name in selected_photos:
                i += 1
                # if(i % 100 == 0):
                # print("Copying {}...".format(i))
                photo_path = os.path.join(label_dir, photo_name)
                output_photo_path = os.path.join(output_label_dir, photo_name)
                shutil.copy(photo_path, output_photo_path)
            print("Finished copying {} of {}, {} photos copied.".format(label, style, select_count))
        print("Finished copying {}.\n".format(style))


train_output_dir = os.path.join(output_dir, "train")
val_output_dir = os.path.join(output_dir, "val")
test_output_dir = os.path.join(output_dir, "test")
# 复制train数据集
print("-----------------------------\nCopying train data...")
# copyd(input_dir, train_output_dir, train_style_ratios)

print("-----------------------------\nCopying val data...")
# copyd(input_dir, val_output_dir, val_style_ratios)

print("-----------------------------\nCopying test data...")
copyd(input_dir, test_output_dir, test_style_ratios)

# 生成train.txt
train_txt_path = os.path.join(output_dir, "train.txt")

print("Generating train.txt...")
print("train.txt path: {}".format(train_txt_path))
print("generate completed!")
