import pickle, os, argparse
# use this script for large datasets, it will split the files in multiple folders


def parse_args():
    parser = argparse.ArgumentParser('Discourse segmentation pipeline')
    parser.add_argument('--article_file_path', type=str)
    parser.add_argument('--edu_file_path', type=str)
    parser.add_argument('--output_dir', type=str)

    return parser.parse_args()


args = parse_args()
articles = pickle.load(open(args.article_file_path, "rb"))
edus = pickle.load(open(args.edu_file_path, "rb"))

folder_count = 1
output_data_dir = args.output_dir + '_' + str(folder_count)

if not os.path.exists(output_data_dir):
    os.makedirs(output_data_dir)

file_count = 0
print("total keys ", len(edus))
for key in articles:

    with open(output_data_dir + os.sep + key + '.out', "w") as a_file:
        a_file.write(articles[key])

    with open(output_data_dir + os.sep + key + '.out.edus', "w") as e_file:
        for val in edus[key]:
            e_file.write(val + '\n')
    file_count += 1
    if file_count == 1000:
        print("done with folder ", folder_count)
        file_count = 0
        folder_count += 1
        output_data_dir = '_'.join(output_data_dir.split("_")[:-1])  + "_" + str(folder_count)
        if not os.path.exists(output_data_dir):
            os.makedirs(output_data_dir)

# print("ended with folder ", folder_count)
print("writing out and edu files complete")