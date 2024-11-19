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


## Jak to działa - stara apka?

1. Użytkownik podaje współrzędne geograficzne (szerokość i długość geograficzną) dla punktu początkowego i końcowego.
2. Apka oblicza punkty na mapie, które znajdują się najbliżej zadanych współrzędnych geograficznych użytkownika.
3. Za pomocą algorytmu Dijkstry program znajduje najkrótszą drogę między tymi dwoma punktami.
4. Następnie generowana jest mapa z wyświetleniem trasy, punktów początkowego i końcowego oraz legendą pokazującą całkowitą odległość w kilometrach.
5. Na końcu mapa jest zapisywana w pliku HTML w folderze docs.


## Instalacja

Pobieranie projektu:

```bash
 git clone https://github.com/Thizz00/Apka-na-ZZAiP.git
```
Instalowanie bibliotek:

```bash
 pip install -r requirements.txt
```
Odpalanie projektu lokalnie:

```bash
 python app_new.py
```
