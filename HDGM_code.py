def R_distance(G, node_i):
    shortest_paths = nx.single_source_shortest_path_length(G, node_i)
    max_distance = max(shortest_paths.values())
    farthest_nodes = [node for node, distance in shortest_paths.items() if
                      distance == max_distance and node != node_i]
    return farthest_nodes

def Improved_cut_off_radius(G, cut_off_radius_value):
    longset_degree = {}
    farthest_nodes_list = []
    Improved_cut_off_radius = {}
    for node in G:
        farthest_nodes_list = R_distance(G, node)
        list_length = len(farthest_nodes_list)
        degree_sum = 0
        if list_length != 0:
            for v in farthest_nodes_list:
                degree_value = G.degree[v]
                degree_sum += degree_value
            longset_degree[node] = degree_sum / list_length
        else:
            longset_degree[node] = 0
    for node1 in G:
        ans = math.sqrt(longset_degree[node1] / G.degree[node1])
        Improved_cut_off_radius[node1] = cut_off_radius_value[node1] / (1 + ans)
    return Improved_cut_off_radius

def cut_off_radius(G):
    truncation_radius_dict = {}
    for node in G:
        shortest_path_lengths = nx.shortest_path_length(G, source=node)
        truncation_radius = max(shortest_path_lengths.values())
        truncation_radius_dict[node] = truncation_radius
        print(node,shortest_path_lengths)
    return truncation_radius_dict

def Kz(G):
    a = 0.1
    K_x = {}
    for node in G:
        ans = 0
        node_degree = G.degree(node)
        neighbors = list(G.neighbors(node))
        sum = 0
        for i in neighbors:
            sum += G.degree(i)
        ans = a * node_degree + (1 - a) * sum
        K_x[node] = ans
    return K_x

def HD(G, H_index_node, K):
    b = 0.7
    sp_i = {}
    for node in G:
        e_squared = b* K[node] + (1 - b) * H_index_node[node]
        sp_i[node] = e_squared
    return sp_i

def h_index_centrality(graph):
    centrality = {}
    for node in graph.nodes:
        neighbors = list(graph.neighbors(node))
        degrees = [graph.degree(n) for n in neighbors]
        # 计算H指数
        h = 0
        while h <= len(degrees) and sum(1 for d in degrees if d >= h) >= h:
            h += 1
        centrality[node] = h - 1
    return centrality

def H_index_i(G):
    H_index_node = {}
    centrality = h_index_centrality(G)

    for i in G:
        sum_value = 0
        neighbors_i = list(G.neighbors(i))
        num_sum = sum(G.degree(neighbor) for neighbor in neighbors_i)
        for j in neighbors_i:
            k1 = G.degree(j) / num_sum
            ans = k1 * centrality[j]
            sum_value += ans

        H_index_node[i] = centrality[i] + sum_value

    return H_index_node

def HDGM(G, HD_value, Improved_cut_off_radius_value):
    GGC_i = {}
    for node_i in G:
        GGC_sum = 0
        shortest_paths = nx.single_source_shortest_path_length(G, node_i)
        for key in shortest_paths:
            if shortest_paths[key] <= Improved_cut_off_radius_value[node_i] and key != node_i:
                ans = (HD_value[node_i] * HD_value[key]) / (shortest_paths[key] * shortest_paths[key])
                GGC_sum += ans
        GGC_i[node_i] = GGC_sum
    return GGC_i