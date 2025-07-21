import networkx as nx, pickle, os
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

rel_short = {
    'span': 'sp',
    'Attribution': 'At',
    'Joint': 'Jo',
    'Elaboration': 'El',
    'Enablement': 'En',
    'Explanation': 'Ex',
    'Background': 'Ba',
    'Same-Unit': 'Sa',
    'Contrast': 'Cont.',
    'Textual-Organization': 'Te',
    'Condition': 'Cond.',
    'Cause': 'Ca',
    'Evaluation': 'Ev',
    'Manner-Means': 'Ma',
    'Temporal': 'Te',
    'Topic-Comment': 'Toco',
    'Comparison': 'Com',
    'Topic-Change': 'Toch',
    'Summary': 'Su'

}


def drawing(G, id_ind, store_path='', extra_name_token=''):
    # pickle.dump(G, open("test_tree.p", "wb"))
    # G = pickle.load(open("test_tree.p", "rb"))
    # nx.nx_agraph.write_dot(G, 'test.dot')
    # for edge in G.edges:
    #     print(edge)
    # print("/////////////////")
    plt.rcParams["figure.figsize"] = (20, 20)

    mapping = {}
    for node in G.nodes:
        if 'relation' in G.nodes[node] and len(G.nodes[node]['relation']) > 1:
            # mapping[node] = node

            mapping[node] = node + '_' + rel_short[G.nodes[node]['relation']]
        else:
            mapping[node] = node
    # print(mapping)

    G = nx.relabel_nodes(G, mapping)
    red_nodes = {}
    blue_nodes = {}
    root_nodes = {}
    for node in G.nodes():
        if 'nuclearity' in G.nodes[node] and G.nodes[node]['nuclearity'] == 'N':
            red_nodes[node] = node
        elif 'nuclearity' in G.nodes[node] and G.nodes[node]['nuclearity'] == 'S':
            blue_nodes[node] = node
        else:
            root_nodes[node] = node

    # plt.title('draw_networkx')
    # pos = nx.drawing.layout.spring_layout(G)
    # , k=0.15, iterations=20
    pos = graphviz_layout(G, prog='dot')
    # print(type(pos))
    for i in pos:
        x, y = pos[i][0], pos[i][1]
        x = x * 4  # x coordinate
        y = y * 4  # y coordinate
        pos[i] = (x, y)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='w')

    nx.draw_networkx_labels(G, pos, labels=red_nodes, font_color='r')
    nx.draw_networkx_labels(G, pos, labels=blue_nodes, font_color='b')
    nx.draw_networkx_labels(G, pos, labels=root_nodes, font_color='k')

    # nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
    # nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)
    nx.draw_networkx_edges(G, pos, arrows=True)

    # nx.draw(G, pos, with_labels=True, arrows=True, node_size=500, node_color='w')
    # plt.show()
    # plt.savefig(store_path + os.sep + id_ind + extra_name_token + '.png')
    plt.savefig(store_path + os.sep + id_ind + extra_name_token + '.png')

    plt.clf()
    return


def drawing_ddt(ddt, id_ind, store_path='', extra_name_token=''):
    pos = graphviz_layout(ddt, prog='dot')
    edge_labels = {}
    red_nodes = {}
    blue_nodes = {}
    root_nodes = {}
    for node in ddt.nodes():
        if ddt.nodes[node]['nuclearity'] == 'N':
            red_nodes[node] = node
        elif ddt.nodes[node]['nuclearity'] == 'S':
            blue_nodes[node] = node
        else:
            root_nodes[node] = node
    print("red nodes ", red_nodes)
    for (s,e) in ddt.edges():
        if 'relation' in ddt.edges[s,e] and ddt.edges[s,e]['relation'] in rel_short:
            edge_labels[s,e] = rel_short[ddt.edges[s,e]['relation']]
    print("red nodes ", red_nodes)
    # print("edge labels ", edge_labels)
    nx.draw(ddt, pos, with_labels=True, arrows=True, node_size=500, node_color='w')
    nx.draw_networkx_labels(ddt, pos, labels=red_nodes, font_color='r')
    nx.draw_networkx_labels(ddt, pos, labels=blue_nodes, font_color='b')
    nx.draw_networkx_labels(ddt, pos, labels=root_nodes, font_color='k')

    nx.draw_networkx_edge_labels(ddt, pos, edge_labels=edge_labels, font_color='b')
    # plt.show()
    plt.savefig(store_path + os.sep + id_ind + '_ddt' + extra_name_token + '.png')
    plt.clf()
    return


def drawing_ddt_3pass(ddt, id_ind, store_path='', extra_name_token='', node_ob=None, high_res=False):
    print("drawing image ")
    plt.rcParams["figure.figsize"] = (10, 10)
    # The following line will generate high quality images
    # if high_res:
    #     plt.figure(dpi=1200)
    pos = graphviz_layout(ddt, prog='dot')
    if node_ob:
        print("drawing 3 pass ddt ", ddt.nodes)
        print(node_ob['root_nodes_with_claim'])
        print(node_ob['sim_nodes'])
        print(node_ob['neg_cont_nodes'])
        print(node_ob['agr_nodes'])
    edge_labels = {}
    # red_nodes = {}
    # blue_nodes = {}
    # root_nodes = {}
    # for node in ddt.nodes():
    #     if ddt.nodes[node]['nuclearity'] == 'N':
    #         red_nodes[node] = node
    #     elif ddt.nodes[node]['nuclearity'] == 'S':
    #         blue_nodes[node] = node
    #     else:
    #         root_nodes[node] = node
    # print("red nodes ", red_nodes)

    for (s,e) in ddt.edges():
        if 'relation' in ddt.edges[s,e] and ddt.edges[s,e]['relation'] in rel_short:
            edge_labels[s,e] = rel_short[ddt.edges[s,e]['relation']]
    # print("edge labels ", edge_labels)
    nx.draw(ddt, pos, with_labels=True, arrows=True, node_size=500, node_color='w')

    if node_ob:
        nx.draw_networkx_labels(ddt, pos, labels=node_ob['sim_nodes'], font_color='g')
        nx.draw_networkx_labels(ddt, pos, labels=node_ob['neg_cont_nodes'], font_color='r')
        nx.draw_networkx_labels(ddt, pos, labels=node_ob['agr_nodes'], font_color='b')
        nx.draw_networkx_labels(ddt, pos, labels=node_ob['root_nodes_with_claim'], font_color='k')

    nx.draw_networkx_edge_labels(ddt, pos, edge_labels=edge_labels, font_color='b')
    # plt.show()
    plt.savefig(store_path + os.sep + id_ind + '_ddt' + extra_name_token + '.jpg')
    plt.clf()
    return


def drawing_2():
    for i in range(2):
        G = nx.DiGraph()
        G.add_edges_from(
            [('A', 'B'), ('A', 'C'), ('D', 'B'), ('E', 'C'), ('E', 'F'),
             ('B', 'H'), ('B', 'G'), ('B', 'F'), ('C', 'G')])

        # val_map = {'A': 1.0,
        #            'D': 0.5714285714285714,
        #            'H': 0.0}
        #
        # values = [val_map.get(node, 0.25) for node in G.nodes()]
        # values = [0.57 for i in range(len(G.nodes))]
        # print(values)
        # Specify the edges you want here
        red_edges = []
        # for edge in G.edges:
        #     s, e = edge
        #     if G.nodes[e]['type'] == 'single_edu':
        #         red_edges.append(edge)
        if i == 0:
            red_edges = [('A', 'C'), ('E', 'C')]
        else:
            red_edges = [('D', 'B'), ('E', 'C')]
        black_edges = [edge for edge in G.edges() if edge not in red_edges]

        # Need to create a layout when doing
        # separate calls to draw nodes and edges
        pos = nx.drawing.layout.spring_layout(G)
        # nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
        #                        node_color = values, node_size = 500)
        # nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
        nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
        # plt.show()
        plt.savefig(str(i) + '.png')
        plt.clf()
        return


def test():
    G = nx.DiGraph()
    G.add_edges_from(
        [('A', 'B'), ('A', 'C'), ('C', 'E'), ('E', 'F'),
         ('B', 'H'), ('B', 'G')])
    G.add_edge('A', 'X', weight=5)
    print(G.edges['A', 'X']['weight'])
    G.remove_node('C')
    print(G.edges())
    return


# test()



    # drawing_2()