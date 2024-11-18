## Opis

Aplikacja, która oblicza i wizualizuje najkrótszą trasę samochodową pomiędzy dwoma punktami w mieście.

![App Screenshot](/docs/ss.png)

## Jak to działa?

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
 python app.py
```
