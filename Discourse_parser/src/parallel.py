import shutil, os, sys, pickle
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)


from os import listdir
from os.path import isfile, join
# source_folder = '../RAW_TEST_2'
source_folder = '/home/rrs99/scratch/StageDP-master/My_data_9'
destination_dir = '/home/rrs99/scratch/StageDP-master/My_data_18'

# for i in range(11, 16):
#     source_folder = '/home/rrs99/scratch/StageDP-master/My_data_' + str(i)
#
out_files = [f for f in listdir(source_folder) if isfile(join(source_folder, f)) and f.endswith('out')]
print("read out files ", len(out_files))
xml_files = [f for f in listdir(source_folder) if isfile(join(source_folder, f)) and f.endswith('xml')]
print("read xml files ", len(xml_files))
#
#     check_file = 'train18272.out'
#     if check_file in out_files:
#         print("found in ", i)
#         break
#     else:
#         print("not found")
#
# pickle.dump(out_files, open("out_files.p", "wb"))
# pickle.dump(xml_files, open("xml_files.p", "wb"))

# out_files = pickle.load(open("out_files.p", "rb"))
# xml_files = pickle.load(open("xml_files.p", "rb"))

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

file_count = 0
folder_count = 18

done = 0
to_do = 0

for o_file in out_files:
    if o_file + '.text.xml' in xml_files:
        done += 1
        continue
    else:
        # if folder_count == 13:
        #     break
        # if file_count == 0:
        #     destination_dir = '/home/rrs99/scratch/StageDP-master/My_data_' + str(folder_count)
            # folder_count += 1
            # os.makedirs(destination_dir)
        file_out = source_folder + os.sep + o_file
        file_text = source_folder + os.sep + o_file + '.text'
        file_edu = source_folder + os.sep + o_file + '.edus'
        # print(file_out)
        # print(file_text)
        # print(file_edu)
        to_do += 1
        # shutil.move(file_out, destination_dir)
        # shutil.move(file_text, destination_dir)
        # shutil.move(file_edu, destination_dir)
        # file_count += 1
        # if file_count == 5000:
        #     print("moved 5000 files to folder ", folder_count)
        #     file_count = 0
print("done ", done)
print("to do ", to_do)
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
