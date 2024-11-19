import requests
import networkx as nx
import folium
from geopy.distance import geodesic
import heapq
import os

def fetch_osm_data(bbox):

    query = f"""
    [out:json];
    (
      way["highway"]( {bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]} );
      >;
    );
    out body;
    """
    url = "http://overpass-api.de/api/interpreter"
    response = requests.post(url, data={'data': query})
    response.raise_for_status()
    return response.json()

def osm_to_graph(osm_data):
    """
    Converts OSM data into a network graph.
    """
    G = nx.Graph()

    for element in osm_data['elements']:
        if element['type'] == 'node':
            G.add_node(
                element['id'],
                x=element['lon'],
                y=element['lat']
            )

    for element in osm_data['elements']:
        if element['type'] == 'way' and 'nodes' in element:
            for u, v in zip(element['nodes'], element['nodes'][1:]):
                if u in G.nodes and v in G.nodes:
                    coord_u = (G.nodes[u]['y'], G.nodes[u]['x'])
                    coord_v = (G.nodes[v]['y'], G.nodes[v]['x'])
                    distance = geodesic(coord_u, coord_v).meters
                    G.add_edge(u, v, weight=distance)

    return G

def nearest_node(graph, lat, lon):

    closest_node = None
    min_distance = float('inf')

    for node, data in graph.nodes(data=True):
        node_coords = (data['y'], data['x'])
        distance = geodesic((lat, lon), node_coords).meters
        if distance < min_distance:
            closest_node = node
            min_distance = distance

    return closest_node

def dijkstra(graph, start, end):

    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    previous_nodes = {node: None for node in graph.nodes}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            path = []
            while previous_nodes[current_node] is not None:
                path.append(current_node)
                current_node = previous_nodes[current_node]
            path.append(start)
            return path[::-1]

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.neighbors(current_node):
            weight = graph.edges[current_node, neighbor]['weight']
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return None

def create_map(route_nodes, city_a, city_b, total_distance_km):

    m = folium.Map(location=city_a, zoom_start=15)

    folium.PolyLine(route_nodes, color="blue", weight=4, opacity=0.7).add_to(m)

    folium.Marker(location=city_a, popup="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(location=city_b, popup="End", icon=folium.Icon(color='red')).add_to(m)

    legend_html = f"""
    <div style="position: fixed; 
                bottom: 10px; left: 10px; width: 200px; height: 120px; 
                background-color: white; border:2px solid black; z-index:9999; font-size:12px;
                padding: 10px;">
        <b>Route Information</b><br>
        <b>Start:</b> {city_a}<br>
        <b>End:</b> {city_b}<br>
        <b>Total Distance:</b> {total_distance_km:.2f} km
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m

def calculate_total_distance(route_nodes):

    total_distance = 0
    for i in range(len(route_nodes) - 1):
        total_distance += geodesic(route_nodes[i], route_nodes[i + 1]).meters
    return total_distance / 1000

def main():
    # Start and end coordinates
    city_a = (50.0560141, 19.9308824)  # Wawel
    city_b = (50.0433374, 19.9640778)  # Bagry

    ''' Kraków
    min_lat = 50.0: Minimum latitude (South boundary of the box)
    min_lon = 19.8: Minimum longitude (West boundary of the box)
    max_lat = 50.1: Maximum latitude (North boundary of the box)
    max_lon = 20.0: Maximum longitude (East boundary of the box)
    '''
    bbox = (50.0, 19.8, 50.1, 20.0)

    print("Fetching data from OpenStreetMap...")
    osm_data = fetch_osm_data(bbox)

    print("Creating the graph...")
    graph = osm_to_graph(osm_data)

    print("Finding the nearest nodes...")
    node_a = nearest_node(graph, city_a[0], city_a[1])
    node_b = nearest_node(graph, city_b[0], city_b[1])

    print("Calculating the shortest path...")
    shortest_path = dijkstra(graph, node_a, node_b)

    if shortest_path is None:
        print("No path found.")
    else:
        route_nodes = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path]

        total_distance_km = calculate_total_distance(route_nodes)

        if not os.path.exists('docs'):
            os.makedirs('docs')

        map_object = create_map(route_nodes, city_a, city_b, total_distance_km)
        map_object.save("docs/shortest_path_map.html")

        print(f"Map generated. Total distance: {total_distance_km:.2f} km")
        print("Saved as: docs/shortest_path_map.html")

if __name__ == "__main__":
    main()
