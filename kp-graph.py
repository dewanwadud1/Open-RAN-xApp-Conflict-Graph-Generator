import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Define the data for the parameters and their associated KPIs
param_data = {
    'Parameter': ['$p_1$', '$p_2$', '$p_3$', '$p_4$', '$p_5$', '$p_6$', '$p_7$', '$p_8$'],
    'KPIs': [
        ['$k_1$', '$k_2$', '$k_3$', '$k_5$'],
        ['$k_1$', '$k_2$', '$k_{41}$', '$k_{42}$'],
        ['$k_2$'],
        ['$k_3$'],
        ['$k_{41}$', '$k_{42}$'],
        ['$k_{41}$', '$k_{42}$'],
        ['$k_5$'],
        ['$k_5$']
    ]
}

# Convert the data into a DataFrame
param_df = pd.DataFrame(param_data)

# Initialize a graph
G_with_kpis = nx.Graph()

# Add nodes to the graph for each parameter
for param in param_df['Parameter']:
    G_with_kpis.add_node(param)

# This dictionary will hold edges as keys and KPIs as values
edge_labels = {}
kpi_to_params = {}

# Add edges to the graph if two parameters share a common KPI
# Also, prepare the labels for the edges with the names of the common KPIs
for i, param1 in param_df.iterrows():
    for j, param2 in param_df.iterrows():
        if i < j:  # To avoid comparing the same pair twice or comparing a parameter with itself
            # Find the intersection of KPIs between two parameters
            common_kpis = set(param1['KPIs']).intersection(set(param2['KPIs']))
            # If there is any common KPI, it means there's a potential connection
            if common_kpis:
                G_with_kpis.add_edge(param1['Parameter'], param2['Parameter'])
                edge_labels[(param1['Parameter'], param2['Parameter'])] = ', '.join(common_kpis)
                for kpi in common_kpis:
                    if kpi not in kpi_to_params:
                        kpi_to_params[kpi] = set()
                    kpi_to_params[kpi].update([param1['Parameter'], param2['Parameter']])

# Remove nodes with no edges
nodes_with_edges = list(G_with_kpis.edges())
nodes_to_remove = [node for node in G_with_kpis.nodes() if G_with_kpis.degree(node) == 0]
G_with_kpis.remove_nodes_from(nodes_to_remove)

# Print the parameter groups for each KPI
for kpi, params in kpi_to_params.items():
    params_group = ', '.join(sorted(params))
    print(f'P_{{{kpi}}}^G = \\{{{params_group}\\}}')

# Draw the graph
plt.figure(figsize=(12, 9))
pos = nx.spring_layout(G_with_kpis, k=0.5, seed=42)  # Adjust k for edge length
nx.draw(G_with_kpis, pos, with_labels=True, node_size=3500, node_color='skyblue', font_size=20, font_weight='bold')

# Draw edge labels
nx.draw_networkx_edge_labels(G_with_kpis, pos, edge_labels=edge_labels, font_color='red')

# Add text for parameter groups on the plot
y_pos = 0.9
for kpi, params in kpi_to_params.items():
    params_group = ', '.join(sorted(params))
    plt.text(0.1, y_pos, f'$P_{{{kpi[1:-1]}}}^G = \\{{{params_group[1:-1]}}}$', horizontalalignment='left',
             verticalalignment='center', transform=plt.gca().transAxes, fontsize=12, color='blue')
    y_pos -= 0.05

plt.title('K-P Graph with KPIs for Parameters in Open-RAN Network', fontsize=15)

# Save the figure
plt.savefig('K-P_graph.pdf', format='pdf')
plt.show()
