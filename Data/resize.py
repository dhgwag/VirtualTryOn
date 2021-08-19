import os
import glob
from PIL import Image


def resize_gs_dataset():
    copy_from = '/home/ai_competition42/dhgwag/Image-Based-Virtual-Try-on-Network-from-Unpaired-Data/appearance_generation/datasets/gs_data/train_label/'
    target_folder = '/home/ai_competition42/dhgwag/Image-Based-Virtual-Try-on-Network-from-Unpaired-Data/appearance_generation/datasets/gs_resize_data/train_label/'



    files = glob.glob(copy_from + '*')

    for f in files:
        title = f.split('.')[-2].split('/')[-1]
        ext = f.split('.')[-1].lower()

        if ext in ['jpg','png']:
            input_img = Image.open(f)
            input_img = input_img.resize((256,512),Image.LANCZOS)
            input_img.save(target_folder+title+'.'+ext)

if __name__ == '__main__':
    #patient_preprocessing()
    resize_gs_dataset()