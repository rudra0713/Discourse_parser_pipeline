import os, sys, shutil
import pickle


new_dir = '/home/rrs99/scratch/StageDP-master/complete_28'
if not os.path.exists(new_dir):
    print("creating directory")
    os.makedirs(new_dir)

file_count = 0
total_edu_files = 0
total_xml_files = 0
total_text_files = 0
total_bracket_files = 0
for folder_count in range(1, 29):
    destination_dir = '/home/rrs99/scratch/StageDP-master/complete_' + str(folder_count)
    edu_files = [os.path.join(destination_dir, fname) for fname in os.listdir(destination_dir) if fname.endswith('.edus')]
    merge_files = [os.path.join(destination_dir, fname) for fname in os.listdir(destination_dir) if fname.endswith('.merge')]
    text_files = [os.path.join(destination_dir, fname) for fname in os.listdir(destination_dir) if fname.endswith('.text')]

    bracket_file = pickle.load(open(destination_dir + os.sep + "cd_article_brackets_" + str(folder_count) + ".p", "rb"))
    print("folder count -------- ", folder_count)
    print(len(text_files), len(edu_files), len(merge_files))
    total_edu_files += len(edu_files)
    total_xml_files += len(merge_files)
    total_text_files += len(text_files)
    total_bracket_files += len(bracket_file)

    if len(edu_files) == len(merge_files) == len(text_files):
        pass
    else:
        for f in edu_files:
            if f[:-5] + 'merge' not in merge_files:
                file_out = f[:-5]
                file_text = f[:-5] + '.text'
                # print(f)

                file_edus = destination_dir + os.sep + f
                # shutil.move(file_out, new_dir)
                # shutil.move(file_text, new_dir)
                # shutil.move(f, new_dir)
    print("---->")

                # print(f)
                # file_count += 1
                # if file_count == 2:
                #     sys.exit(0)

        # print("error....")
print("total_edu_files", total_edu_files)
print("total_xml_files", total_xml_files)
print("total_text_files", total_text_files)
print("total_bracket_files", total_bracket_files)