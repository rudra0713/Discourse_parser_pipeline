import os, sys, shutil, pickle


bracket_dir = '/home/rrs99/scratch/StageDP-master/My_data_'
src_path = '/home/rrs99/projects/rrg-mageed/rrs99/code/NeuralEDUSeg-master/output/'

all_edu_files = pickle.load(open(src_path + 'cd_articles_edus_new.p', "rb"))


def find_occurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def get_edu_name(path):
    slash_occ = find_occurrences(path, '/')[-1]
    stop_occ = find_occurrences(path, '.')[0]
    return path[slash_occ + 1: stop_occ]


bracket_count = 0
one_len_bracket = 0
for folder_count in range(1, 18):
    destination_dir = '/home/rrs99/scratch/StageDP-master/My_data_' + str(folder_count)
    edu_files = [os.path.join(destination_dir, fname) for fname in os.listdir(destination_dir) if fname.endswith('.edus')]
    xml_files = [os.path.join(destination_dir, fname) for fname in os.listdir(destination_dir) if fname.endswith('.xml')]
    merge_files = [os.path.join(destination_dir, fname) for fname in os.listdir(destination_dir) if fname.endswith('.merge')]

    if len(edu_files) != len(merge_files):
        print("error ", folder_count)
        print("edu files ", folder_count, len(edu_files))
        print("merge files ", folder_count, len(merge_files))

        # exact_keys = [get_edu_name(f) for f in edu_files]
    # edu_p = {}
    # for key in exact_keys:
    #     edu_p[key] = all_edu_files[key]
    # bracket_p = pickle.load(open(bracket_dir + str(folder_count) + os.sep + 'cd_article_brackets_' + str(folder_count) + '.p', "rb"))
    #
    # print("len of edus ", len(edu_p))
    # print("len of brackets ", len(bracket_p))
    # for key in edu_p:
    #     try:
    #         if key in bracket_p:
    #             print(key)
    #             bracket_count += 1
    #         if bracket_count == 5:
    #             break
    #
    #     except:
    #         print(key)
    #         print("disaster ")
    #         sys.exit(0)

