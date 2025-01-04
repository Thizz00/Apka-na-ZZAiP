## Opis

Aplikacja służy do obliczania najkrótszej trasy między dwoma punktami na podstawie danych z OpenStreetMap (OSM) uzywając algorytmu Dijkstry oraz wizualizacji tej trasy na interaktywnej mapie.


## Jak to działa?

1. Pobieranie danych z OpenStreetMap (OSM) dla określonego obszaru (obszar definiowany przez współrzędne graniczne: bbox) np. dla Krakowa jest to:
    * min_lat = 50.0: Minimalna szerokość geograficzna (południowa granica pola)
    * min_lon = 19.8: Minimalna długość geograficzna (zachodnia granica pola)
    * max_lat = 50.1: Maksymalna szerokość geograficzna (północna granica pudełka)
    * max_lon = 20.0: Maksymalna długość geograficzna (wschodnia granica pola)
2. Przekształcanie danych z OpenStreetMap (OSM) w strukturę grafu (używając biblioteki NetworkX).
3. Przeszukiwanie wszystkich węzłów w grafie i obliczanie odległości między współrzędnymi wejściowymi a współrzędnymi każdego węzła. Zwraca węzeł, którego odległość do podanych współrzędnych jest najmniejsza.
4. Obliczanie najkrótszej ścieżki między dwoma węzłami w grafie za pomocą algorytmu Dijkstry.
5. Tworzenie interaktywnej mapy, na której wizualizowana jest najkrótsza trasa.

![App Screenshot](/docs/ss_new.png)

## Wyniki testów

Wszystkie testy zakończyły się pomyślnie. Przeprowadzono 3 testy, które trwały łącznie 4 minuty i 50 sekund.

![App Screenshot](/docs/test.png)
 
 
Szczegóły testów:

1.	Kraków: Trasa z Wawelu do Bagrów 
* Oczekiwany zakres odległości: 3.0 - 3.5 km
* Test zakończony sukcesem
2.	Gdańsk: Trasa z Długiego Targu do Westerplatte 
* Oczekiwany zakres odległości: 9.0 - 10.0 km
* Test zakończony sukcesem
3.	Wrocław: Trasa z Przejścia Garncarskiego do Hali Stulecia 
* Oczekiwany zakres odległości: 3.5 - 4.0 km
* Test zakończony sukcesem

Wnioski:

1.	Algorytm poprawnie wyznacza trasy dla różnych miast i różnych odległości.
2.	Obliczone odległości mieszczą się w oczekiwanych zakresach dla każdego miasta.
3.	Testy potwierdzają, że funkcje fetch_osm_data, osm_to_graph, nearest_node, dijkstra i calculate_total_distance działają prawidłowo w różnych scenariuszach.


## Instalacja

Pobieranie projektu:

```bash
 git clone https://github.com/Thizz00/Projekt-ZZAiP-Algorytm-Dijkstry.git
```
Instalowanie bibliotek:

```bash
 pip install -r requirements.txt
```

Inicjacja testów:

```bash
 pytest tests.py
```

Inicjacja aplikacji lokalnie:

```bash
 python app_new.py
```
