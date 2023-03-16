import os
import shutil
import random

# 定义输入输出目录和各个风格的比例
input_dir = "/content/gdrive/MyDrive/data/PACS_test_1_pic/PACS"
output_dir = "/content/gdrive/MyDrive/data/PACS_train"
train_style_ratios = {"art_painting": 0.8, "cartoon": 0.1, "photo": 0.1, "sketch": 0.0}
val_style_ratios = {"art_painting": 0.2, "cartoon": 0.1, "photo": 0.1, "sketch": 0.6}
test_style_ratios = {"art_painting": 0.0, "cartoon": 0.0, "photo": 0.0, "sketch": 1.0}


def copyd(inputdir, outputdir, ratios):
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历每个标签文件夹，并将符合比例的照片复制到输出目录中
    for style in ratios:
        # 获取当前风格的目录和比例
        print("Copying {}...".format(style))
        style_dir = os.path.join(input_dir, style)
        style_ratio = ratios[style]

        # 遍历每个标签文件夹
        for label in os.listdir(style_dir):
            print("Copying {}...".format(label))
            label_dir = os.path.join(style_dir, label)
            output_label_dir = os.path.join(output_dir, label)
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
                if(i % 10 == 0):
                    print("Copying {}...".format(i))
                photo_path = os.path.join(label_dir, photo_name)
                output_photo_path = os.path.join(output_label_dir, photo_name)
                shutil.copy(photo_path, output_photo_path)
            print("Copy {} imgs".format(i))
# 复制train数据集
print("Copying train data...")
train_output_dir = os.path.join(output_dir, "train")
copyd(input_dir, train_output_dir, train_style_ratios)
print("Copying val data...")
val_output_dir = os.path.join(output_dir, "val")
copyd(input_dir, val_output_dir, val_style_ratios)
print("Copying test data...")
test_output_dir = os.path.join(output_dir, "test")
copyd(input_dir, test_output_dir, test_style_ratios)

# 生成train.txt
train_txt_path = os.path.join(output_dir, "train.txt")

print("Generating train.txt...")
print("train.txt path: {}".format(train_txt_path))
print("generate completed!")