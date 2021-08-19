import os
import glob


def copy_gs_dataset():
    copy_from = '/home/ai_competition42/dhgwag/CIHP_PGN/datasets/gs_dataset/images/'#'/home/ai_competition42/dhgwag/CIHP_PGN/output/gs_parsing_maps/'
    target_folder = '/home/ai_competition42/dhgwag/Image-Based-Virtual-Try-on-Network-from-Unpaired-Data/appearance_generation/datasets/gs_data/train_img/'



    files = glob.glob(copy_from + '*')

    for f in files:
        title = f.split('.')[-2].split('/')[-1]
        ext = f.split('.')[-1].lower()

        if ext in ['jpg','png']:
            if '_vis' not in title :
                os.system("cp " + f + " " + target_folder)

if __name__ == '__main__':
    #patient_preprocessing()
    copy_gs_dataset()