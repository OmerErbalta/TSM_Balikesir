import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QLabel, \
    QPushButton, QFormLayout, QMessageBox

import folium
import json
import random
from shapely.geometry import Point, Polygon

from arabaMesafe import calculate_distance_car
from genetikAlgoritmaPMX import genetic_algorithm_for_coordinates
from mesafeHesaplaKusUcusu import calculate_distances, haversine

def generate_random_point_in_polygon(polygon, num_points=1):
    minx, miny, maxx, maxy = polygon.bounds
    random_points = []

    for _ in range(num_points):
        while True:
            random_point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if polygon.contains(random_point):
                random_points.append((random_point.y, random_point.x))
                break

    return random_points
class SecondWindow(QWidget):
    def __init__(self, best_order, random_locations, polygon_coordinates_list):
        super().__init__()

        self.setWindowTitle('Yeni Sayfa')
        self.best_order = best_order
        self.random_locations = random_locations
        self.polygon_coordinates_list = polygon_coordinates_list

        self.init_ui()

    def show_popup_on_load(self,bird,car):
        popup_message = f"Bird Flight Distance {bird} km Car Distance: {car} km"
        QMessageBox.information(self, "Distances", popup_message, QMessageBox.Ok)

    def init_ui(self):
        random_locations = self.random_locations
        best_order = self.best_order
        with open('balıkesir2.geojson','r',encoding='utf-8') as file:
            geojson_data = json.load(file)
        borderList = []
        for feature in geojson_data.get("features", []):
            if feature.get("geometry", {}).get("type") == "Polygon":
                borderList.append(feature["geometry"]["coordinates"][0])

        # Eğer Polygon koordinatları bulunduysa rastgele konumlar üret
        if borderList:
            # Tüm poligonları birleştir
            combined_polygon = Polygon([point for polygon in borderList for point in polygon])

        polygon_coordinates_list = self.polygon_coordinates_list
        order_coordinates = [random_locations[i] for i in best_order]

        result_map = folium.Map(location=[order_coordinates[0][0], order_coordinates[0][1]], zoom_start=9)
        reversed_coordinates = [list(reversed(coord)) for coord in combined_polygon.exterior.coords]
        folium.Polygon(locations=reversed_coordinates, color='blue', fill=True, fill_color='lightblue',
                       fill_opacity=0.5).add_to(result_map)
        for i, location in enumerate(order_coordinates):
            folium.Marker(location=[location[0], location[1]],
                          popup=f'{location}  <br> Number: {i + 1}',
                          icon=folium.Icon(color='green', prefix='fa', icon='location', icon_color='white')).add_to(
                result_map)

        for i in range(len(order_coordinates) - 1):
            line_coordinates = [order_coordinates[i], order_coordinates[i + 1]]
            folium.PolyLine(locations=line_coordinates, color='green').add_to(result_map)

        total_car_distance = 0
        for i in range(len(random_locations) - 1):
            if i < len(random_locations):
                carMesafe = calculate_distance_car(random_locations[i], random_locations[i + 1])
                print(carMesafe)
                total_car_distance += carMesafe
        print(total_car_distance)
        bird_flight_distances, total_bird_flight_distance = calculate_distances(order_coordinates, "km")
        inner_v_layout_result = QVBoxLayout(self)

        html_code_result = result_map.get_root().render()
        webview_result = QWebEngineView()
        webview_result.setHtml(html_code_result)
        inner_v_layout_result.addWidget(webview_result)
        btn_use_data = QPushButton("Distances")
        btn_use_data.clicked.connect(lambda:self.show_popup_on_load(total_bird_flight_distance,total_car_distance) )
        inner_v_layout_result.addWidget(btn_use_data)



class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def button_clicked(self,random_locations,polygon_coordinates_list):

        values = [line_edit.text() for line_edit in self.input_lineedits]
        print("Input Values:", values)
        best_order = self.run_genetic_algorithm(self.random_locations, values)
        self.new_window = SecondWindow(best_order, self.random_locations, self.polygon_coordinates_list)
        self.new_window.show()

    def run_genetic_algorithm(self, random_locations, values):
        return genetic_algorithm_for_coordinates("distances.json", pop_size=int(values[3]),
                                                 generations=int(values[0]),
                                                 elite_percent=float(values[4]),
                                                 crossover_rate=float(values[1]),
                                                 mutation_rate=float(values[2]))

    def generate_random_locations(self):
        with open('balikesir_boundary.geojson', 'r', encoding='utf-8') as file:
            geojson_data = json.load(file)

        polygon_coordinates_list = []
        for feature in geojson_data.get("features", []):
            if feature.get("geometry", {}).get("type") == "Polygon":
                polygon_coordinates_list.append(feature["geometry"]["coordinates"][0])

        if polygon_coordinates_list:
            combined_polygon = Polygon([point for polygon in polygon_coordinates_list for point in polygon])

            random_locations = generate_random_point_in_polygon(combined_polygon, num_points=20)
            distances_json = {}
            for i, location in enumerate(random_locations):
                distance_json = {}
                for j, location in enumerate(random_locations):
                    if i != j:
                        key = f'location_to {j}'
                        distance_json[key] = haversine(random_locations[i], random_locations[j], 'km')
                distances_json[f'location {i}'] = distance_json
            with open('distances.json', 'w') as json_file:
                json.dump(distances_json, json_file, indent=2)
            return random_locations, polygon_coordinates_list
        else:
            print("No Polygon geometry found in the GeoJSON file.")
            return []
    def init_ui(self):
        self.setWindowTitle('Shortest Distance Calculation')
        self.setGeometry(100, 100, 1200, 600)
        self.setWindowIcon(QIcon('icon.png'))
        self.random_locations,self.polygon_coordinates_list = self.generate_random_locations()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.h_layout_result = QHBoxLayout(central_widget)

        v_layout_left = QVBoxLayout()

        input_labels = ["Generations:", "Crossover Rate:", "Mutation Rate:", "Population Size", "Elite Child Rate"]
        self.input_lineedits = [QLineEdit() for _ in range(5)]

        form_layout = QFormLayout()
        for label, line_edit in zip(input_labels, self.input_lineedits):
            form_layout.addRow(label, line_edit)

        v_layout_left.addLayout(form_layout)
        with open('balıkesir2.geojson', 'r', encoding='utf-8') as file:
            geojson_data2 = json.load(file)
        borderList = []
        for feature in geojson_data2.get("features", []):
            if feature.get("geometry", {}).get("type") == "Polygon":
                borderList.append(feature["geometry"]["coordinates"][0])

        # Eğer Polygon koordinatları bulunduysa rastgele konumlar üret
        if borderList:
            # Tüm poligonları birleştir
            combined_polygon = Polygon([point for polygon in borderList for point in polygon])
        self.h_layout_result.addLayout(v_layout_left)
        mymap1 = folium.Map(location=[self.random_locations[0][0], self.random_locations[0][1]], zoom_start=9)
        reversed_coordinates = [list(reversed(coord)) for coord in combined_polygon.exterior.coords]
        folium.Polygon(locations=reversed_coordinates, color='blue', fill=True, fill_color='lightblue',
                       fill_opacity=0.5).add_to(mymap1)
        for i, location in enumerate(self.random_locations):
            folium.Marker(location=[location[0], location[1]],
                          popup=f'{location}  <br> Numara: {i + 1}',
                          icon=folium.Icon(color='orange', prefix='fa', icon='location', icon_color='white')).add_to(mymap1)

        for i in range(len(self.random_locations) - 1):
            line_coordinates = [self.random_locations[i], self.random_locations[i + 1]]
            folium.PolyLine(locations=line_coordinates, color='red').add_to(mymap1)

        # HTML kodunu al
        html_code1 = mymap1.get_root().render()

        # İlk webview1 eklendi
        webview1 = QWebEngineView()
        webview1.setHtml(html_code1)

        btn_use_data = QPushButton("Create Map")
        btn_use_data.clicked.connect(lambda: self.button_clicked(self.random_locations,self.polygon_coordinates_list))
        v_layout_left.addWidget(btn_use_data)
        v_layout_left.addWidget(webview1)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapWindow()
    sys.exit(app.exec_())
