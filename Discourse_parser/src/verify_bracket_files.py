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
    bracket_file = pickle.load(open(destination_dir + os.sep + "cd_article_brackets_" + str(folder_count) + ".p", "rb"))

    # if len(edu_files) != len(bracket_file):
    # print("folder count ", folder_count)
    # except:
    #     print("no file ", folder_count)
    proper_fault = 0
    improper_fault = 0
    # for val in bracket_file:
    #     if len(bracket_file[val]) > 0:
    #         print(bracket_file[val])
    #         sys.exit(0)
    for val in bracket_file:
        if len(bracket_file[val]) == 0:
            bracket_file[val] = [((1,1), 'Nucleus', '')]
            # print("zero error ", folder_count, val)
            if len(all_edu_files[val]) == 1:
                proper_fault += 1
            else:
                improper_fault += 1

    pickle.dump(bracket_file, open(destination_dir + os.sep + 'cd_article_brackets_new_' + str(folder_count) + ".p", "wb"))
    # print("proper/ improper ", proper_fault, improper_fault)
    # for val in bracket_file:
    #     if len(bracket_file[val]) == 1:
    #         print("one error ", folder_count, val, bracket_file[val])
    # for val in bracket_file:
    #     max_edu = 0
    #
    #     for lines in bracket_file[val]:
    #         a, _, _ = lines
    #
    #         x, y = a
    #         max_edu = max(max_edu, max(x, y))
    #     if max_edu != len(all_edu_files[val]):
    #         print("error .. ", folder_count, val, max_edu, len(all_edu_files[val]))
