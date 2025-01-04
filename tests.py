import pytest
from app_new import fetch_osm_data, osm_to_graph, nearest_node, dijkstra, calculate_total_distance

@pytest.mark.parametrize("start, end, bbox, city, expected_min, expected_max", [
    ((50.0560141, 19.9308824), (50.0433374, 19.9640778), (50.0, 19.8, 50.1, 20.0), "Kraków", 3.0, 3.5), #Wawel - Bagry (Kraków)
    ((54.3484484, 18.6531988), (54.4075833, 18.6711111), (54.3, 18.6, 54.5, 18.8), "Gdańsk", 9.0, 10.0), #Długi targ - Westerplatte (Gdańsk)
    ((51.1101776, 17.0326689), (51.1068553, 17.0774238), (51.0, 16.9, 51.2, 17.1), "Wrocław", 3.5, 4.0) #Przejscie garncarskie - hala stulecia (Wrocław)
])
def test_routing_algorithm(start, end, bbox, city, expected_min, expected_max):
    osm_data = fetch_osm_data(bbox)
    graph = osm_to_graph(osm_data)
    
    start_node = nearest_node(graph, start[0], start[1])
    end_node = nearest_node(graph, end[0], end[1])
    
    path = dijkstra(graph, start_node, end_node)
    
    assert path is not None, f"No path found between the given points in {city}"
    
    route_nodes = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in path]
    distance = calculate_total_distance(route_nodes)
    
    assert distance > 0, f"Distance should be greater than 0 in {city}"
    assert expected_min <= distance <= expected_max, f"Distance {distance:.2f} km is out of expected range [{expected_min}, {expected_max}] km in {city}"
    print(f"Distance for {city} ({start} to {end}): {distance:.2f} km")
