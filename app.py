import osmnx as ox
import folium
import heapq
from geopy.distance import geodesic
import os

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
            node1_coords = (graph.nodes[current_node]['y'], graph.nodes[current_node]['x'])
            node2_coords = (graph.nodes[neighbor]['y'], graph.nodes[neighbor]['x'])
            weight = geodesic(node1_coords, node2_coords).meters

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
    city_a = (50.0560141, 19.9308824)  # Wawel
    city_b = (50.0433374, 19.9640778)  # Bagry

    place_name = "Kraków, Poland"
    graph = ox.graph_from_place(place_name, network_type='drive')

    node_a = ox.distance.nearest_nodes(graph, X=city_a[1], Y=city_a[0])
    node_b = ox.distance.nearest_nodes(graph, X=city_b[1], Y=city_b[0])

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

        print(f"Map generated with total distance: {total_distance_km:.2f} km")

if __name__ == "__main__":
    main()
