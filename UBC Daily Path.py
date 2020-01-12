import osmnx as ox
import networkx as nx
import folium
import pandas as pd
from geopandas.io import file

#For my Project 3, I have decided to design a function called plot_route that will take in a csv file
#with my daily schedule for school and plot a map of UBC showing where I go throughout the day, with
#node markers for locations I visit and highlighted paths for the shortest path it takes for me to
#walk there. I wanted to change the color of the start and end nodes in order to distinguish them
#from my "path nodes" however I was unable to change specific node colors or overlay two graphs.
#I realized however that because of my use of ox.plot_graph_routes, the path node markers were being
#created twice and therefore have a slightly darker coloration that distinguishes them from the start
#and end. My function plot_route will take in 'fn' which represents the file name of the CSV file as
# a string, I have included a few days as CSV files which will produce different paths.

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


