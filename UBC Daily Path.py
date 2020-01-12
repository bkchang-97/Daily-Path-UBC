import osmnx as ox
import networkx as nx
import folium
import pandas as pd
from geopandas.io import file

UBC = ox.gdf_from_place('UBC')

toshow = ox.project_gdf(UBC)
ox.plot_shape(toshow)

unified = UBC.unary_union.convex_hull

G = ox.graph_from_polygon(unified, network_type='walk', truncate_by_edge=True,
                                     clean_periphery=False, simplify=True)
ox.plot_graph(ox.project_graph(G))

def plot_route(fn):

    dataframe = pd.read_csv(fn)
    loa = list(dataframe['Location'])

    routes = []

    for index, address in enumerate(loa):
        if index + 1 <= len(loa) - 1 :
            origin = ox.utils.geocode(address)
            destination = ox.utils.geocode(loa[index + 1])

            origin_node = ox.get_nearest_node(G, origin)
            destination_node = ox.get_nearest_node(G, destination)

            route = nx.shortest_path(G, origin_node, destination_node, weight = 'length')

            routes.append(route)
            
    ox.plot_graph_routes(G, routes, orig_dest_node_color= 'b')

plot_route("Tuesday.csv")


