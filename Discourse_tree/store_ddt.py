from create_discourse_graph_server import compute_edu_count, \
    edu_to_article_mapping, build_graph
import pickle, os
import networkx as nx, argparse
import sys, statistics
from sentence_level_dt_ddt import li_structure_sentence_ddt
from draw_graph import drawing

# file_path = 'random_file.txt'
# sys.stdout = open(file_path, "w")

store_image_directory = 'Discourse_images'
if not os.path.exists(store_image_directory):
    os.makedirs(store_image_directory)


def leaky_sentence_check_from_discourse_tree_sentence(id_index, discourse_tree_sentence, article_to_edu_mapping, sentence_tree_to_edu_tree_mapping, discourse_tree_edu, image_file_name):
    # for node in discourse_tree_sentence.nodes:
    #     if discourse_tree_sentence.nodes[node]['type'] == 'root':
    #         root_node = node
    # root_node = '1_10'
    root_node = [n for n, d in discourse_tree_sentence.in_degree() if d == 0][0]

    dfs_res = list(nx.dfs_edges(discourse_tree_sentence, source=root_node))
    print("before leaky update, final dfs ", dfs_res)
    all_leaky_nodes = []
    while True:
        leaky_found = False

        root_node = [n for n, d in discourse_tree_sentence.in_degree() if d == 0][0]

        dfs_res = list(nx.dfs_edges(discourse_tree_sentence, source=root_node))
        already_used_sources = []

        for (s, _) in dfs_res:
            if s not in already_used_sources:
                already_used_sources.append(s)
                updated_nodes = []
                children = list(discourse_tree_sentence.successors(s))
                # print("children", children)
                for child in children:
                    updated_nodes += child.split("_")
                # updated_nodes += children[0].split("_") + children[1].split("_")
                updated_nodes_set = set(updated_nodes)
                if len(updated_nodes) == 4 and len(updated_nodes_set) == 3:
                    if updated_nodes[1] == updated_nodes[2]:
                        print("leaky sentence found id_index", id_index, children, updated_nodes, article_to_edu_mapping)
                        discourse_tree_sentence, org_leaky_copy = fix_leaky_sentence(id_index, discourse_tree_sentence, children[0], children[1], sentence_tree_to_edu_tree_mapping, discourse_tree_edu, article_to_edu_mapping, image_file_name)
                        all_leaky_nodes.append(org_leaky_copy)
                        leaky_found = True
                        break
                        # sys.exit(0)
        if not leaky_found:
            break
    # drawing(discourse_tree_sentence, id_index, '../Discourse_images/development', '_S_dt_leaky_leaky_fixed')
    root_node = [n for n, d in discourse_tree_sentence.in_degree() if d == 0][0]

    dfs_res = list(nx.dfs_edges(discourse_tree_sentence, source=root_node))
    print("final dfs ", dfs_res)
    return discourse_tree_sentence, all_leaky_nodes


def same_sentence_check(edu_to_sentence_list, edu_i, edu_j):
    if edu_to_sentence_list[int(edu_i)] == edu_to_sentence_list[int(edu_j)]:
        return True
    return False


def sentence_beginning_end_check(article_to_edu_mapping, edu_i, edu_j):
    for key in article_to_edu_mapping:
        if article_to_edu_mapping[key] and article_to_edu_mapping[key][0] == edu_i and article_to_edu_mapping[key][-1] == edu_j:
            return True
    return False


def one_edu_sentence_check(article_to_edu_mapping, edu_i):
    for key in article_to_edu_mapping:
        if len(article_to_edu_mapping[key]) == 1 and edu_i in article_to_edu_mapping[key]:
            return str(key)
    return


def update_node(article_to_edu_mapping, edu_i, edu_j=None):
    start_node = None
    end_node = None
    for key in article_to_edu_mapping:
        if edu_i in article_to_edu_mapping[key]:
            start_node = key
        if edu_j in article_to_edu_mapping[key]:
            end_node = key
    if start_node == end_node or not edu_j:
        return str(start_node)
    return str(start_node) + "_" + str(end_node)


def fix_leaky_sentence(id_index, discourse_tree_sentence, leaky_node_left,
                       leaky_node_right, sentence_tree_to_edu_tree_mapping, discourse_tree_edu, article_to_edu_mapping, image_file_name):
    leaky_edu_lefts = sentence_tree_to_edu_tree_mapping[leaky_node_left]
    leaky_edu_rights = sentence_tree_to_edu_tree_mapping[leaky_node_right]

    print("leaky_edu_left ", leaky_edu_lefts)
    print("leaky_edu_right ", leaky_edu_rights)

    edus_in_leaky_sentence = article_to_edu_mapping[int(leaky_node_left.split("_")[1])]
    # also colud have used int(leaky_node_right.split("_")[0])
    left_subtree_edu_count = {}
    for edu in edus_in_leaky_sentence:
        left_subtree_edu_count[edu] = -1

    right_subtree_edu_count = {}
    for edu in edus_in_leaky_sentence:
        right_subtree_edu_count[edu] = -1

    dfs_left = []
    for leaky_edu_left in leaky_edu_lefts:
        dfs_left_pairs = list(nx.dfs_edges(discourse_tree_edu, source=leaky_edu_left))

        for (s, e) in dfs_left_pairs:
            dfs_left.append(s)
            dfs_left.append(e)
    dfs_left = list(set(dfs_left))

    dfs_right = []
    for leaky_edu_right in leaky_edu_rights:
        dfs_right_pairs = list(nx.dfs_edges(discourse_tree_edu, source=leaky_edu_right))

        for (s, e) in dfs_right_pairs:
            dfs_right.append(s)
            dfs_right.append(e)
    dfs_right = list(set(dfs_right))
    print("dfs_left ", dfs_left)
    print("dfs right ", dfs_right)

    for node in dfs_left:
        node_list = node.split("_")
        for edu in edus_in_leaky_sentence:
            if edu in node_list:
                left_subtree_edu_count[edu] = 0

    for node in dfs_right:
        node_list = node.split("_")
        for edu in edus_in_leaky_sentence:
            if edu in node_list:
                right_subtree_edu_count[edu] = 0

    print("left_subtree_edu_count ", left_subtree_edu_count)
    print("right_subtree_edu_count ", right_subtree_edu_count)
    print("--------")

    left_subtree_edu_count_sum = sum([left_subtree_edu_count[key] for key in left_subtree_edu_count])
    right_subtree_edu_count_sum = sum([right_subtree_edu_count[key] for key in right_subtree_edu_count])

    modify_left = False

    if left_subtree_edu_count_sum == right_subtree_edu_count_sum:
        modify_left = True
    elif left_subtree_edu_count_sum < right_subtree_edu_count_sum:
        modify_left = True
    else:
        modify_left = False
    # choose which subtree to modify
    # how to modify left subtree
    modified = True
    # nx.relabel_nodes(ddt, mapping)
    mapping = {}
    remove_nodes = []
    print("MODIFYING LEFT ", modify_left)
    if modify_left:
        org_leaky_copy = leaky_node_left
        culprit_in_leaky_node = leaky_node_left.split("_")[1]
        while True:
            if not modified:
                break
            print("leaky node left ", leaky_node_left)
            leaky_node = leaky_node_left.split("_")

            if len(leaky_node) == 1 and leaky_node[0] == culprit_in_leaky_node:
                updated_node = str(int(leaky_node[0]) - 1)
                parent_of_leaky_node_left = list(discourse_tree_sentence.predecessors(leaky_node_left))[0]
                if leaky_node_left in discourse_tree_sentence.nodes:
                    print("removing edge between ,,, ", parent_of_leaky_node_left, leaky_node_left)
                    discourse_tree_sentence.remove_edge(parent_of_leaky_node_left, leaky_node_left)
                    if discourse_tree_sentence.in_degree(leaky_node_left) == 0:
                        remove_nodes.append(leaky_node_left)
                discourse_tree_sentence.add_edge(parent_of_leaky_node_left, updated_node)
                print("adding edge between .. => ", parent_of_leaky_node_left, updated_node)
                modified = False
            else:
                updated_node_first_part = str(leaky_node[0])
                updated_node_second_part = str(int(leaky_node[1]) - 1)
                if updated_node_first_part != updated_node_second_part:
                    updated_node = updated_node_first_part + "_" + updated_node_second_part
                    if updated_node in discourse_tree_sentence.nodes:
                        discourse_tree_sentence.add_edge(list(discourse_tree_sentence.predecessors(leaky_node_left))[0], updated_node)
                        remove_nodes.append(leaky_node_left)
                        for node in list(discourse_tree_sentence.successors(leaky_node_left)):
                            if node != updated_node and discourse_tree_sentence.in_degree(node) == 1:
                                remove_nodes.append(node)
                        modified = False
                    else:
                        mapping[leaky_node_left] = updated_node
                        print("mapping ", leaky_node_left, "to -> ", updated_node)
                        leaky_node_left = list(discourse_tree_sentence.successors(leaky_node_left))[1]
                        modified = True
                else:
                    updated_node = updated_node_first_part
                    if updated_node in discourse_tree_sentence.nodes:
                        discourse_tree_sentence.add_edge(list(discourse_tree_sentence.predecessors(leaky_node_left))[0], updated_node)
                        remove_nodes.append(leaky_node_left)
                        for node in list(discourse_tree_sentence.successors(leaky_node_left)):
                            if node != updated_node and discourse_tree_sentence.in_degree(node) == 1:
                                remove_nodes.append(node)
                    modified = False
        print("mapping (left)", mapping)
        print("remove nodes (left)", remove_nodes)
        for node in remove_nodes:
            discourse_tree_sentence.remove_node(node)
        discourse_tree_sentence = nx.relabel_nodes(discourse_tree_sentence, mapping)
    else:
        org_leaky_copy = leaky_node_right
        culprit_in_leaky_node = leaky_node_right.split("_")[0]

        while True:
            if not modified:
                break
            leaky_node = leaky_node_right.split("_")
            if len(leaky_node) == 1 and leaky_node[0] == culprit_in_leaky_node:
                updated_node = str(int(leaky_node[0]) + 1)
                parent_of_leaky_node_right = list(discourse_tree_sentence.predecessors(leaky_node_right))[0]
                if leaky_node_right in discourse_tree_sentence.nodes:
                    print("removing edge between ,,, ", parent_of_leaky_node_right, leaky_node_right)
                    discourse_tree_sentence.remove_edge(parent_of_leaky_node_right, leaky_node_right)
                    if discourse_tree_sentence.in_degree(leaky_node_right) == 0:
                        remove_nodes.append(leaky_node_right)
                discourse_tree_sentence.add_edge(parent_of_leaky_node_right, updated_node)
                print("adding edge between .. => ", parent_of_leaky_node_right, updated_node)
                modified = False
            else:

                updated_node_first_part = str(int(leaky_node[0]) + 1)
                updated_node_second_part = str(leaky_node[1])
                if updated_node_first_part != updated_node_second_part:
                    updated_node = updated_node_first_part + "_" + updated_node_second_part
                    if updated_node in discourse_tree_sentence.nodes:
                        print("adding edge ", list(discourse_tree_sentence.predecessors(leaky_node_right))[0], updated_node)
                        discourse_tree_sentence.add_edge(list(discourse_tree_sentence.predecessors(leaky_node_right))[0], updated_node)
                        remove_nodes.append(leaky_node_right)
                        for node in list(discourse_tree_sentence.successors(leaky_node_right)):
                            if node != updated_node and discourse_tree_sentence.in_degree(node) == 1:
                                remove_nodes.append(node)

                        modified = False
                    else:
                        mapping[leaky_node_right] = updated_node
                        leaky_node_right = list(discourse_tree_sentence.successors(leaky_node_right))[0]
                        modified = True
                else:
                    updated_node = updated_node_first_part
                    if updated_node in discourse_tree_sentence.nodes:
                        print("adding edge ", list(discourse_tree_sentence.predecessors(leaky_node_right))[0], updated_node)
                        discourse_tree_sentence.add_edge(list(discourse_tree_sentence.predecessors(leaky_node_right))[0],
                                                         updated_node)
                        remove_nodes.append(leaky_node_right)
                        for node in list(discourse_tree_sentence.successors(leaky_node_right)):
                            if node != updated_node and discourse_tree_sentence.in_degree(node) == 1:
                                remove_nodes.append(node)
                    modified = False
        print("mapping (right)", mapping)
        print("remove nodes (right)", remove_nodes)
        for node in remove_nodes:
            discourse_tree_sentence.remove_node(node)
        discourse_tree_sentence = nx.relabel_nodes(discourse_tree_sentence, mapping)
    # drawing(discourse_tree_sentence, id_index, store_image_directory, image_file_name)
    # sys.exit(0)

    return discourse_tree_sentence, org_leaky_copy


def build_sentence_dt(id_index, discourse_tree_edu, article_to_edu_mapping, edu_to_sentence_list, image_file_name, print_all=False):
    sentence_tree_to_edu_tree_mapping = {}
    root_node = None
    for node in discourse_tree_edu.nodes:
        if discourse_tree_edu.nodes[node]['type'] == 'root':
            root_node = node
    # root_node = '1_10'
    dfs_res = list(nx.dfs_edges(discourse_tree_edu, source=root_node))
    irrelevant_nodes = []
    # print("dfs ", dfs_res)
    discourse_tree_sentence = nx.DiGraph()
    print("about to build sentence dt.. ")
    for (s, e) in dfs_res:
        if s not in irrelevant_nodes:
            # source will never be of one length, that one length means an edu
            parent_sentence_dt_node = None
            if print_all:
                print("s ", s)
                print("e ", e)
            start_node_after_split = s.split("_")
            end_node_after_split = e.split("_")

            if not same_sentence_check(edu_to_sentence_list, start_node_after_split[0], start_node_after_split[1]) or  sentence_beginning_end_check(article_to_edu_mapping, start_node_after_split[0], start_node_after_split[1]):
                parent_sentence_dt_node = update_node(article_to_edu_mapping, start_node_after_split[0], start_node_after_split[1])
                if print_all:
                    print("parent_sentence_dt_node ", parent_sentence_dt_node)
                if parent_sentence_dt_node:
                    if len(parent_sentence_dt_node.split("_")) == 2:
                        start_parent_sentence_dt_node = parent_sentence_dt_node.split("_")[0]
                        end_parent_sentence_dt_node = parent_sentence_dt_node.split("_")[1]
                        if int(end_parent_sentence_dt_node) - int(start_parent_sentence_dt_node) == 1:
                            discourse_tree_sentence.add_edge(parent_sentence_dt_node, start_parent_sentence_dt_node)
                            if print_all:
                                print("adding edge between immediate -> ", parent_sentence_dt_node, start_parent_sentence_dt_node)
                            discourse_tree_sentence.add_edge(parent_sentence_dt_node, end_parent_sentence_dt_node)
                            if print_all:
                                print("adding edge between immediate -> ", parent_sentence_dt_node, end_parent_sentence_dt_node)

                    if len(e.split("_")) == 1:
                        child_sentence_dt_node = one_edu_sentence_check(article_to_edu_mapping, e)
                        if parent_sentence_dt_node and child_sentence_dt_node and parent_sentence_dt_node != child_sentence_dt_node:
                            if print_all:
                                print("adding edge between if -> ", (s, e), parent_sentence_dt_node, child_sentence_dt_node)
                            discourse_tree_sentence.add_edge(parent_sentence_dt_node, child_sentence_dt_node)
                            if parent_sentence_dt_node in sentence_tree_to_edu_tree_mapping:
                                sentence_tree_to_edu_tree_mapping[parent_sentence_dt_node] += [s]
                            else:
                                sentence_tree_to_edu_tree_mapping[parent_sentence_dt_node] = [s]
                            if child_sentence_dt_node in sentence_tree_to_edu_tree_mapping:
                                sentence_tree_to_edu_tree_mapping[child_sentence_dt_node] += [e]
                            else:
                                sentence_tree_to_edu_tree_mapping[child_sentence_dt_node] = [e]


                                # has to be an edu
                    elif not same_sentence_check(edu_to_sentence_list, end_node_after_split[0], end_node_after_split[1]) or sentence_beginning_end_check(article_to_edu_mapping, end_node_after_split[0], end_node_after_split[1]):
                        child_sentence_dt_node = update_node(article_to_edu_mapping, end_node_after_split[0], end_node_after_split[1])
                        if parent_sentence_dt_node and child_sentence_dt_node and parent_sentence_dt_node != child_sentence_dt_node:
                            if print_all:
                                print("adding edge between else -> ", (s, e), parent_sentence_dt_node, child_sentence_dt_node)

                            discourse_tree_sentence.add_edge(parent_sentence_dt_node, child_sentence_dt_node)
                            if parent_sentence_dt_node in sentence_tree_to_edu_tree_mapping:
                                sentence_tree_to_edu_tree_mapping[parent_sentence_dt_node] += [s]
                            else:
                                sentence_tree_to_edu_tree_mapping[parent_sentence_dt_node] = [s]
                            if child_sentence_dt_node in sentence_tree_to_edu_tree_mapping:
                                sentence_tree_to_edu_tree_mapping[child_sentence_dt_node] += [e]
                            else:
                                sentence_tree_to_edu_tree_mapping[child_sentence_dt_node] = [e]

                            # start_parent_sentence_dt_node = parent_sentence_dt_node.split("_")[0]
                            # end_parent_sentence_dt_node = parent_sentence_dt_node.split("_")[1]
                            # if int(end_parent_sentence_dt_node) - int(start_parent_sentence_dt_node) == 1:
                            #     discourse_tree_sentence.add_edge(parent_sentence_dt_node, start_parent_sentence_dt_node)
                            #     # print("adding edge between immediate -> ", parent_sentence_dt_node, start_parent_sentence_dt_node)
                            #     discourse_tree_sentence.add_edge(parent_sentence_dt_node, end_parent_sentence_dt_node)
                            #     # print("adding edge between immediate -> ", parent_sentence_dt_node, end_parent_sentence_dt_node)
                    else:
                        irrelevant_nodes.append(e)
                        dfs_irrelevant = list(nx.dfs_edges(discourse_tree_edu, source=e))
                        for (_, child_irrelevant) in dfs_irrelevant:
                            irrelevant_nodes.append(child_irrelevant)

    # drawing(discourse_tree_sentence, id_index, store_image_directory, '_S_dt_before')
    add_edge_list = []
    for parent in discourse_tree_sentence.nodes:
        children = list(discourse_tree_sentence.successors(parent))
        if len(children) == 0 or len(children) == 2:
            continue
        if len(children) == 1:
            print("invalid tree ", id_index, parent, children)
            parent_sentences = parent.split("_")  # 1_4  [1, 4]
            children_list = children[0].split("_") # 2_4 [2, 4]
            if parent_sentences[0] in children_list:
                add_edge_list.append((parent, parent_sentences[1], 'right', children[0]))
                # discourse_tree_sentence.add_edge(parent, parent_sentences[1])
            else:
                # adding a new edge between 1_4 and 1
                add_edge_list.append((parent, parent_sentences[0], 'left', children[0]))
                # discourse_tree_sentence.add_edge(parent, parent_sentences[0])
    for pot_edge in add_edge_list:
        if pot_edge[2] == 'left':
            # this is done so dfs over the tree outputs the smaller child to be the left node
            # print("removing edge between ", pot_edge[0], pot_edge[3])
            discourse_tree_sentence.remove_edge(pot_edge[0], pot_edge[3])
            discourse_tree_sentence.add_edge(pot_edge[0], pot_edge[1])
            # print("adding edge between ", pot_edge[0], pot_edge[3])
            discourse_tree_sentence.add_edge(pot_edge[0], pot_edge[3])
        else:
            discourse_tree_sentence.add_edge(pot_edge[0], pot_edge[1])

    # if len(add_edge_list) != 0:
    #     drawing(discourse_tree_sentence, id_index, '../Discourse_images/development', '_S_dt_validated')
    # if print_all:
    #     print("sentence_tree_to_edu_tree_mapping ", sentence_tree_to_edu_tree_mapping)
    print("sentence_tree_to_edu_tree_mapping ", sentence_tree_to_edu_tree_mapping)

    drawing(discourse_tree_sentence, id_index, store_image_directory, image_file_name)
    return discourse_tree_sentence, sentence_tree_to_edu_tree_mapping


def count_nucleus(node, sentence_tree_to_edu_tree_mapping, article_to_edu_mapping, discourse_tree_edu):
    all_edu_nodes = []

    if node in sentence_tree_to_edu_tree_mapping:
        edu_node_collection = sentence_tree_to_edu_tree_mapping[node][0]
        if len(edu_node_collection.split("_")) == 2:
            for edu_index in range(int(edu_node_collection.split("_")[0]), int(edu_node_collection.split("_")[1]) + 1):
                all_edu_nodes.append(str(edu_index))
        else:
            all_edu_nodes.append(edu_node_collection)
    elif int(node) in article_to_edu_mapping:
        all_edu_nodes = article_to_edu_mapping[int(node)]
    else:
        node_splits = node.split("_")
        if len(node_splits) == 2:
            possible_leaky_node_1 = str(int(node_splits[0]) - 1) + "_" + str(node_splits[1])
            possible_leaky_node_2 = str(node_splits[0]) + "_" + str(int(node_splits[1]) + 1)
            print("possible_leaky_node_1 ", possible_leaky_node_1, "possible_leaky_node_2 ", possible_leaky_node_2)
            if possible_leaky_node_1 in sentence_tree_to_edu_tree_mapping:
                edu_node_collection = sentence_tree_to_edu_tree_mapping[possible_leaky_node_1][0]
                if len(edu_node_collection.split("_")) == 2:
                    for edu_index in range(int(edu_node_collection.split("_")[0]),
                                           int(edu_node_collection.split("_")[1]) + 1):
                        all_edu_nodes.append(str(edu_index))
                else:
                    all_edu_nodes.append(edu_node_collection)
            elif possible_leaky_node_2 in sentence_tree_to_edu_tree_mapping:
                edu_node_collection = sentence_tree_to_edu_tree_mapping[possible_leaky_node_2][0]
                if len(edu_node_collection.split("_")) == 2:
                    for edu_index in range(int(edu_node_collection.split("_")[0]),
                                           int(edu_node_collection.split("_")[1]) + 1):
                        all_edu_nodes.append(str(edu_index))
                else:
                    all_edu_nodes.append(edu_node_collection)

    print("count_nucleus -> ", "given node ", node, "all_edu_nodes ", all_edu_nodes)
    number_of_nucleus = 0
    for node in all_edu_nodes:
        if discourse_tree_edu.nodes[node]['nuclearity'] == 'N':
            number_of_nucleus += 1
    return number_of_nucleus


def nuclearity_assignment(id_index, discourse_tree_sentence, discourse_tree_edu, sentence_tree_to_edu_tree_mapping, article_to_edu_mapping, all_leaky_nodes, all_sentences_in_article, image_file_name):
    nuclearity_mapping = {}
    root_node = [n for n, d in discourse_tree_sentence.in_degree() if d == 0][0]
    print("nuclearity_assignment, all_leaky_nodes ", all_leaky_nodes)
    # all leaky nodes is not used later, because, all nodes that were updated to fix the leakiness
    # had to be stored, dev98
    print("discourse tree sentence nodes ", discourse_tree_sentence.nodes)
    for key in sentence_tree_to_edu_tree_mapping:
        temp_list = list(set(sentence_tree_to_edu_tree_mapping[key]))
        if len(temp_list) == 1:
            sentence_tree_to_edu_tree_mapping[key] = temp_list
        else:
            max_diff = 0
            winner_node = None
            # print("key ... -> ", key)
            for node in sentence_tree_to_edu_tree_mapping[key]:
                if len(node.split("_")) == 2:
                    # print("node ... -> ", node)
                    node_diff = int(node.split("_")[1]) - int(node.split("_")[0])
                    if node_diff > max_diff:
                        winner_node = node
                        max_diff = node_diff
            if not winner_node:
                winner_node = temp_list[0]
            sentence_tree_to_edu_tree_mapping[key] = [winner_node]
    print("sentence_tree_to_edu_tree_mapping ....  -> ", sentence_tree_to_edu_tree_mapping)
    for sentence_node in discourse_tree_sentence.nodes:
        if sentence_node != root_node:
            if sentence_node in sentence_tree_to_edu_tree_mapping:
                # print("sentence_node ", sentence_node, sentence_tree_to_edu_tree_mapping[sentence_node][0], discourse_tree_edu.nodes[sentence_tree_to_edu_tree_mapping[sentence_node][0]]['nuclearity'])
                nuclearity_mapping[sentence_node] = discourse_tree_edu.nodes[sentence_tree_to_edu_tree_mapping[sentence_node][0]]['nuclearity']
            else:
                in_edus_nuclearities = []
                if int(sentence_node) in article_to_edu_mapping:
                    for edu in article_to_edu_mapping[int(sentence_node)]:
                        in_edus_nuclearities.append(discourse_tree_edu.nodes[edu]['nuclearity'])
                    try:
                        nuclearity_mapping[sentence_node] = statistics.mode(in_edus_nuclearities)
                    except:
                        nuclearity_mapping[sentence_node] = 'N'
                else:
                    node_splits = sentence_node.split("_")
                    if len(node_splits) == 2:
                        possible_leaky_node_1 = str(int(node_splits[0]) - 1) + "_" + str(node_splits[1])
                        possible_leaky_node_2 = str(node_splits[0]) + "_" + str(int(node_splits[1]) + 1)
                        print("possible_leaky_node_1 ", possible_leaky_node_1, "possible_leaky_node_2 ", possible_leaky_node_2, possible_leaky_node_2 in all_leaky_nodes, possible_leaky_node_2 in sentence_tree_to_edu_tree_mapping)
                        if possible_leaky_node_1 in sentence_tree_to_edu_tree_mapping:
                            nuclearity_mapping[sentence_node] = \
                            discourse_tree_edu.nodes[sentence_tree_to_edu_tree_mapping[possible_leaky_node_1][0]]['nuclearity']
                        elif possible_leaky_node_2 in sentence_tree_to_edu_tree_mapping:
                            nuclearity_mapping[sentence_node] = \
                            discourse_tree_edu.nodes[sentence_tree_to_edu_tree_mapping[possible_leaky_node_2][0]]['nuclearity']

    nuclearity_mapping[root_node] = ''
    for node in discourse_tree_sentence:
        if node not in nuclearity_mapping:
            print("really unfortunate case for nuclearity of node", node)
            nuclearity_mapping[node] = 'S'
    print("nuclearity_mapping ", id_index, nuclearity_mapping)

    for node in discourse_tree_sentence.nodes:
        children = list(discourse_tree_sentence.successors(node))
        if len(children) != 0:
            left_child = children[0]
            right_child = children[1]
            left_child_nuclearity = nuclearity_mapping[left_child]
            right_child_nuclearity = nuclearity_mapping[right_child]
            if left_child_nuclearity == right_child_nuclearity == 'S':
                # we have to assign "N" to one of them
                left_child_nucleus_count = count_nucleus(left_child, sentence_tree_to_edu_tree_mapping, article_to_edu_mapping, discourse_tree_edu)
                right_child_nucleus_count = count_nucleus(right_child, sentence_tree_to_edu_tree_mapping, article_to_edu_mapping, discourse_tree_edu)
                if left_child_nucleus_count < right_child_nucleus_count:
                    nuclearity_mapping[right_child] = 'N'
                elif left_child_nucleus_count >= right_child_nucleus_count:
                    nuclearity_mapping[left_child] = 'N'
                # if count of nucleus for both child are equal,
                # i am just choosing left child randomly


    # sys.exit(0)
    for node in discourse_tree_sentence:
        if node not in nuclearity_mapping:
            print("nuclearity unassigned ", id_index, node)
            sys.exit(0)
    nx.set_node_attributes(discourse_tree_sentence, nuclearity_mapping, 'nuclearity')

    node_type_mapping = {}
    root_node = [n for n, d in discourse_tree_sentence.in_degree() if d == 0][0]
    for node in discourse_tree_sentence.nodes:
        if node == root_node:
            node_type_mapping[node] = 'root'
        elif len(node.split("_")) == 2:
            node_type_mapping[node] = 'combined'
        else:
            node_type_mapping[node] = 'single_edu'

    nx.set_node_attributes(discourse_tree_sentence, node_type_mapping, 'type')
    text_mapping = {}
    for node in discourse_tree_sentence.nodes:
        if discourse_tree_sentence.nodes[node]['type'] == 'single_edu':
            text_mapping[node] = all_sentences_in_article[int(node) - 1]
        else:
            text_mapping[node] = ''

    nx.set_node_attributes(discourse_tree_sentence, text_mapping, 'text')
    # print("----------")
    # print("PROPERTIES .....")
    # for node in discourse_tree_sentence.nodes:
    #     print(node)
    #     print(discourse_tree_sentence.nodes[node]['nuclearity'])
    #     print(discourse_tree_sentence.nodes[node]['type'])
    #     print(discourse_tree_sentence.nodes[node]['text'])
    # print("----------")
    # drawing(discourse_tree_sentence, id_index, store_image_directory, image_file_name)

    return discourse_tree_sentence


def validate_tree(discourse_tree_sentence, id_index):
    problem_found = False
    for parent in discourse_tree_sentence.nodes:
        if len(parent.split("_")) == 2:
            parent_range = [str(node) for node in range(int(parent.split("_")[0]), int(parent.split("_")[1]) + 1)]
            children = list(discourse_tree_sentence.successors(parent))
            children_range = []
            for child in children:
                if len(child.split("_")) == 2:
                    child_range = [str(node) for node in range(int(child.split("_")[0]), int(child.split("_")[1]) + 1)]
                    for node in child_range:
                        children_range.append(node)
                else:
                    children_range.append(child)
            # print("parent and children range ", parent, parent_range, children_range)
            if len(parent_range) != len(children_range):
                print("problem ", id_index, parent)
                problem_found = True
    if not problem_found:
        print("validated ", id_index)
    return


def generate_image_sentence_dt(opt):

    bracket_files = pickle.load(open(opt.output_dir + os.sep + opt.bracket_file_path, 'rb'))
    print("loaded bracket files " , len(bracket_files))
    # article_files = pickle.load(open('../data/data_stance_createdebate_complete/claim_with_articles_only.p', 'rb'))
    edu_files = pickle.load(open(opt.output_dir + os.sep + opt.edu_file_path, 'rb'))
    print("loaded edu files ", len(edu_files))

    # all_test_ids = pickle.load(open('../data/data_stance_createdebate_complete/all_test_ids.p', 'rb'))

    print("loaded all test ids")
    test_claim_article_label = pickle.load(open(opt.output_dir + os.sep + opt.claim_article_file_path, "rb"))
    all_test_ids = [key for key in test_claim_article_label]

    print("loaded test_claim_article_label ")

    write_to_xlsx = False
    worksheet = None
    workbook = None
    draw_graph = True
    write_final_result = False
    no_leaky_count = 0
    ddt_predictions_key = 'ddt_prediction_dst_sentence_ddt_wo_negative_distance'

    # with_negative means negation test has been applied (this leads to a worse performance than
    # wo_negative i.e. no negation test)
    # ddt_prediction_dst_sentence_ddt_wo_negative_stanford means stanford bigram method has been used

    image_file_name_build_sentence_dt = '_S_dt'
    image_file_name_nuclearity = '_S_dt_nuclearity'
    image_file_name_leaky = '_S_dt_leaky_leaky_fixed'
    image_file_name_ddt = '_S_dt_ddt'
    image_file_name_for_aggregation = '_S_dt_3pass_sentence_final_dst_s_stance_wo_negative_distance'
    xlsx_file_name_for_bert_stance = 'development_with_sentence_ddt_wo_negative.xlsx'
    final_result_file = 'development_results_a_vs_sentence_ddt_stance.xlsx'

    start_index = int(opt.start_index)
    end_index = int(opt.end_index)

    failed_ids = []
    print("starting from ", start_index, "going until ", end_index)
    print("bracket files len ", len(bracket_files))

    # check_these_ids = ['test_14']
    per_id_data = {}
    for id_index in all_test_ids:
    # for id_index in check_these_ids:
        claim = test_claim_article_label[id_index]['claim']
        article = test_claim_article_label[id_index]['article']
        label = test_claim_article_label[id_index]['label']

    #     claim_edus = compute_edu_count(claim, edu_files[id_index])
    #     claim_edus_list = [str(k + 1) for k in range(claim_edus)]
    #     print("claim edus list ", claim_edus_list)
    #
    #     edus_list_wo_claim = [str(k + 1) for k in range(len(edu_files[id_index])) if str(k + 1) not in claim_edus_list]
    #     print("........")
    #     discourse_tree = build_graph(edu_files[id_index], bracket_files[id_index])
    #
    #     print("graph built done ..", type(discourse_tree))
    #     if type(discourse_tree) == bool:
    #         failed_ids.append((id_index, 'graph built false'))
    #         continue
    #
    #     # sys.exit(0)
    #     old_edu_to_sentence_list, old_article_to_edu_mapping, old_all_sentences_in_article = edu_to_article_mapping(edus_list_wo_claim, article, discourse_tree, print_all=True)
    #     # old_edu_to_sentence_list, old_article_to_edu_mapping, old_all_sentences_in_article = edu_to_article_mapping_stanford_bigram(edus_list_wo_claim, article, discourse_tree, print_all=False)
    #     for k, edu in enumerate(edu_files[id_index]):
    #         print(k + 1, edu)
    #     print("......")
    #     print("edu_to_sentence_list ", old_edu_to_sentence_list)
    #     print("article_to_edu_mapping ", old_article_to_edu_mapping)
    #     print("all_sentences_in_article ", old_all_sentences_in_article)
    #     print("..........")
    #     # sys.exit(0)
    #     all_sentences_in_article = [claim] + old_all_sentences_in_article
    #     article_to_edu_mapping = {1: [edu_id for edu_id in claim_edus_list]}
    #     max_edu_id = -1
    #     for key in old_article_to_edu_mapping:
    #         if len(old_article_to_edu_mapping[key]) != 0:
    #             article_to_edu_mapping[key + 2] = old_article_to_edu_mapping[key]
    #             max_edu_id = max(max_edu_id, max([int(edu_id) for edu_id in old_article_to_edu_mapping[key]]))
    #     edu_to_sentence_list = [0 for _ in range(max_edu_id + 1)]
    #     edu_to_sentence_list[0] = -1
    #     for key in article_to_edu_mapping:
    #         for edu_id in article_to_edu_mapping[key]:
    #             edu_to_sentence_list[int(edu_id)] = key
    #     print("edu_to_sentence_list ", edu_to_sentence_list)
    #     print("article_to_edu_mapping ", article_to_edu_mapping)
    #     print("all_sentences_in_article ")
    #     for k, sentence in enumerate(all_sentences_in_article):
    #         print(k + 1, sentence)
    #     print("--------------")
    # # sys.exit(0)
    #     discourse_tree_sentence, sentence_tree_to_edu_tree_mapping = build_sentence_dt(id_index, discourse_tree, article_to_edu_mapping, edu_to_sentence_list, image_file_name=image_file_name_build_sentence_dt, print_all=False)
    #
    #     print("created discourse_tree_sentence")
    #     discourse_tree_sentence, all_leaky_nodes = leaky_sentence_check_from_discourse_tree_sentence(id_index, discourse_tree_sentence, article_to_edu_mapping, sentence_tree_to_edu_tree_mapping, discourse_tree, image_file_name = image_file_name_leaky)
    #     # print("all leaky nodes ", all_leaky_nodes)
    #
    #     # if len(all_leaky_nodes) != 0:
    #     # no_leaky_count += 1
    #     print("leaky sentence check done")
    #     discourse_tree_sentence = nuclearity_assignment(id_index, discourse_tree_sentence, discourse_tree,
    #                                          sentence_tree_to_edu_tree_mapping, article_to_edu_mapping,
    #                                          all_leaky_nodes, all_sentences_in_article, image_file_name=image_file_name_nuclearity)
    #     print("nuclearity assignment done ")
    #     # validate_tree(discourse_tree_sentence, id_index)
    #     sentence_ddt = li_structure_sentence_ddt(id_index, discourse_tree_sentence, image_file_name=image_file_name_ddt, store_image_directory=store_image_directory)
    #
    #     print("created sentence_ddt")
    #     pickle.dump(discourse_tree_sentence, open("/scratch/rrs99/Stance_Detection_LST/rfd_sentence_level/rfd_sentence_dt/all" + '/' + id_index + ".p", "wb"))
    #     pickle.dump(sentence_ddt, open("/scratch/rrs99/Stance_Detection_LST/rfd_sentence_level/rfd_sentence_ddt/all" + '/' + id_index + ".p", "wb"))
    #     discourse_extra_info = {
    #         'all_sentences_in_article': all_sentences_in_article,
    #         'article_to_edu_mapping': article_to_edu_mapping
    #     }
    #     pickle.dump(discourse_extra_info, open("/scratch/rrs99/Stance_Detection_LST/rfd_sentence_level/rfd_discourse_extra_info/all" + '/' + id_index + ".p", "wb"))


        try:

            claim_edus = compute_edu_count(claim, edu_files[id_index])
            claim_edus_list = [str(k + 1) for k in range(claim_edus)]
            print("claim edus list ", claim_edus_list)

            edus_list_wo_claim = [str(k + 1) for k in range(len(edu_files[id_index])) if str(k + 1) not in claim_edus_list]
            print("........")
            discourse_tree = build_graph(edu_files[id_index], bracket_files[id_index])

            print("graph built done ..", type(discourse_tree))
            if type(discourse_tree) == bool:
                failed_ids.append((id_index, 'graph built false'))
                continue

            # sys.exit(0)
            old_edu_to_sentence_list, old_article_to_edu_mapping, old_all_sentences_in_article = edu_to_article_mapping(edus_list_wo_claim, article, discourse_tree, print_all=True)
            # old_edu_to_sentence_list, old_article_to_edu_mapping, old_all_sentences_in_article = edu_to_article_mapping_stanford_bigram(edus_list_wo_claim, article, discourse_tree, print_all=False)
            for k, edu in enumerate(edu_files[id_index]):
                print(k + 1, edu)
            print("......")
            print("edu_to_sentence_list ", old_edu_to_sentence_list)
            print("article_to_edu_mapping ", old_article_to_edu_mapping)
            print("all_sentences_in_article ", old_all_sentences_in_article)
            print("..........")
            # sys.exit(0)
            all_sentences_in_article = [claim] + old_all_sentences_in_article
            article_to_edu_mapping = {1: [edu_id for edu_id in claim_edus_list]}
            max_edu_id = -1
            for key in old_article_to_edu_mapping:
                if len(old_article_to_edu_mapping[key]) != 0:
                    article_to_edu_mapping[key + 2] = old_article_to_edu_mapping[key]
                    max_edu_id = max(max_edu_id, max([int(edu_id) for edu_id in old_article_to_edu_mapping[key]]))
            edu_to_sentence_list = [0 for _ in range(max_edu_id + 1)]
            edu_to_sentence_list[0] = -1
            for key in article_to_edu_mapping:
                for edu_id in article_to_edu_mapping[key]:
                    edu_to_sentence_list[int(edu_id)] = key
            print("edu_to_sentence_list ", edu_to_sentence_list)
            print("article_to_edu_mapping ", article_to_edu_mapping)
            print("all_sentences_in_article ")
            for k, sentence in enumerate(all_sentences_in_article):
                print(k + 1, sentence)
            print("--------------")
        # sys.exit(0)
            discourse_tree_sentence, sentence_tree_to_edu_tree_mapping = build_sentence_dt(id_index, discourse_tree, article_to_edu_mapping, edu_to_sentence_list, image_file_name=image_file_name_build_sentence_dt, print_all=False)

            print("created discourse_tree_sentence")
            discourse_tree_sentence, all_leaky_nodes = leaky_sentence_check_from_discourse_tree_sentence(id_index, discourse_tree_sentence, article_to_edu_mapping, sentence_tree_to_edu_tree_mapping, discourse_tree, image_file_name = image_file_name_leaky)
            # print("all leaky nodes ", all_leaky_nodes)

            # if len(all_leaky_nodes) != 0:
            # no_leaky_count += 1
            print("leaky sentence check done")
            discourse_tree_sentence = nuclearity_assignment(id_index, discourse_tree_sentence, discourse_tree,
                                                 sentence_tree_to_edu_tree_mapping, article_to_edu_mapping,
                                                 all_leaky_nodes, all_sentences_in_article, image_file_name=image_file_name_nuclearity)
            print("nuclearity assignment done ")
            # validate_tree(discourse_tree_sentence, id_index)
            sentence_ddt = li_structure_sentence_ddt(id_index, discourse_tree_sentence, image_file_name=image_file_name_ddt, store_image_directory=store_image_directory)

            print("created sentence_ddt")
            discourse_extra_info = {
                'all_sentences_in_article': all_sentences_in_article,
                'article_to_edu_mapping': article_to_edu_mapping,
                'claim': claim,
                'article': article,
                'label': label
            }

            # pickle.dump(discourse_tree_sentence, open("/scratch/rrs99/Stance_Detection_LST/rfd_sentence_level/rfd_sentence_dt/all" + '/' + id_index + ".p", "wb"))
            # pickle.dump(sentence_ddt, open("/scratch/rrs99/Stance_Detection_LST/rfd_sentence_level/rfd_sentence_ddt/all" + '/' + id_index + ".p", "wb"))
            # pickle.dump(discourse_extra_info, open("/scratch/rrs99/Stance_Detection_LST/rfd_sentence_level/rfd_discourse_extra_info/all" + '/' + id_index + ".p", "wb"))
            per_id_data[id_index] = {'sentence_dt': discourse_tree_sentence, 'sentence_ddt': sentence_ddt, 'extra_info': discourse_extra_info}

        except Exception as e:
            print("Exception ", e)
            failed_ids.append((id_index, e))
            pass

    pickle.dump(per_id_data, open(args.output_dir + os.sep + args.output_file, "wb"))

    pickle.dump(failed_ids, open(args.output_dir + os.sep + 'failed_ids.p', "wb"))
    print("failed ids -> ", len(failed_ids))
    return


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_index', required=False, help='path to data directory.', default='0')
    parser.add_argument('--end_index', required=False, help='path to data directory.', default='10000')
    parser.add_argument('--bracket_file_path', default='')
    parser.add_argument('--edu_file_path', default='')
    parser.add_argument('--claim_article_file_path', default='')
    parser.add_argument('--output_dir', default='')
    parser.add_argument('--output_file', default='')

    return parser.parse_args()


if __name__ == '__main__':

    args = arg_parse()
    generate_image_sentence_dt(args)



