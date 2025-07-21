import pickle, os


def merge_br():
    dir = '/home/rrs99/scratch/StageDP-master/complete_'
    bracket_ob = {}
    total_keys = 0
    for i in range(1, 28):
        try:
            print(dir + str(i) + os.sep + "cd_article_brackets_" + str(i) + ".p")
            x = pickle.load(open(dir + str(i) + os.sep + "cd_article_brackets_" + str(i) + ".p", "rb"))
            print("keys ", len(x))
            total_keys += len(x)
            bracket_ob.update(x)
        except:
            print("not found ", "cd_article_brackets_" + str(i))
    pickle.dump(bracket_ob, open("/home/rrs99/projects/rrg-mageed/rrs99/code/NeuralEDUSeg-master/ca/claim_with_articles_brackets.p", "wb"))
    print("total keys ", total_keys)
    return


def find_file():
    dir = '/home/rrs99/scratch/StageDP-master/My_data_'
    file_1 = 'train7157.out'
    file_2 = 'train544.out'
    file1_found = False
    file2_found = False
    for i in range(1, 19):
        parse_files = [fname for fname in os.listdir(dir + str(i)) if
                       fname.endswith(".out")]

        if file_1 in parse_files and not file1_found:
            print("file 1 found ", i)
            file1_found = True
        if file_2 in parse_files and not file2_found:
            print("file 2 found ", i)
            file2_found = True

        if file1_found and file2_found:
            break
        print("done dir ", i, len(parse_files))
    return


# find_file()
merge_br()