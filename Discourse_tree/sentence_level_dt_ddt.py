from create_discourse_graph_server import find_my_top_node, parent, find_head_edu, is_root
import networkx as nx
from draw_graph import drawing_ddt


def li_structure_sentence_ddt(id_index, G, image_file_name, store_image_directory):

    ddt = nx.DiGraph()
    # print("USING LI STRUCTURE TO DRAW SENTENCE DDT..")

    # drawing(G, id_ind, '../Discourse_images/development_recheck')
    edu_nodes = [node for node in G.nodes if G.nodes[node]['type'] == 'single_edu']
    ddt.add_node('0', type='super_root', nuclearity='')

    for edu in edu_nodes:

        P = find_my_top_node(G, edu, print_all=False)
        if is_root(G, P):
            ddt.add_node(edu, text=G.nodes[edu]['text'], nuclearity=G.nodes[edu]['nuclearity'])

            ddt.add_edge('0', edu, relation='')
            # ddt.add_node(edu, type='root')
        else:
            P = parent(G, P)
            # print("parent P -> ", P)
            ddt.add_node(edu, text=G.nodes[edu]['text'], nuclearity=G.nodes[edu]['nuclearity'])

            edu_2 = find_head_edu(G, P)
            # if edu == '15':
            #     print("edu 2 ", edu_2)

            ddt.add_edge(edu_2, edu)

    # drawing_ddt(ddt, id_index, store_image_directory, image_file_name)
    return ddt


