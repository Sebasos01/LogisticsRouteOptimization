# Organización de Archivos y Carpetas

- **Docs/**:
  - Contiene el modelo y el informe de resultados.
  
- **informes/**:
  - Contiene todos los reportes y rutas generadas para los 4 casos de estudio.
  
- **solution.ipynb**:
  - Notebook principal con todo el código del modelo, desde la carga de datos hasta la resolución del problema.
  
- **Geneticos.ipynb**:
  - Contiene el código del bono de algoritmos genéticos para abordar el problema desde un enfoque evolutivo.

# Documentación del Código

Este código implementa un modelo de ruteo de vehículos, incluyendo la preparación de datos, cálculo de distancias, formulación y resolución de un modelo de optimización, y la posterior generación de reportes y mapas de las rutas obtenidas.

## Estructura General

1. **Funciones de Utilidad para la Matriz de Costos:**
   - `haversine(coord1, coord2)`: Calcula la distancia en kilómetros entre dos puntos dados por coordenadas (latitud, longitud) utilizando la fórmula de Haversine.
   - `compute_distance_matrix(data)`: Prepara las coordenadas, llama a la API de OSRM para obtener distancias terrestres y calcula las distancias para vehículos aéreos (drones) con la función Haversine.

2. **Función para Resolver el Modelo de Ruteo de Vehículos:**
   - `solve_vehicle_routing_problem(data)`: Construye y resuelve el modelo de optimización de ruteo de vehículos utilizando Pyomo. Incluye:
     - Definición de conjuntos y parámetros (nodos, vehículos, tipos de vehículos, etc.).
     - Variables de decisión (asignación de clientes a vehículos, arcos utilizados, asignación de depósitos, etc.).
     - Restricciones del modelo (flujo, capacidad, asignación de depósitos, eliminación de subciclos, etc.).
     - Función objetivo para minimizar costos (carga/descarga, distancia, tiempo, recarga y mantenimiento).
     - Llamada al solver (Gurobi u otro) y devolución de la solución en forma de diccionario.

3. **Función para Visualizar Rutas:**
   - `print_vehicle_routes(solution, data)`: Imprime en consola las rutas de cada vehículo según la solución obtenida.

4. **Funciones de Utilidad para Cargar Datos:**
   - Varias funciones (`read_clients`, `read_vehicles`, `read_depots`, etc.) que cargan y validan datos desde archivos CSV para clientes, vehículos, depósitos, capacidades, costos de carga/descarga y tipos de vehículos.
   
5. **Generación de Reportes:**
   - `generate_reports(solution, data)`: A partir de la solución, genera archivos CSV y TXT con las rutas, el valor de la función objetivo y un informe de costos operativos.

6. **Visualización con Mapas:**
   - Código adicional para generar un mapa interactivo con Folium que muestre nodos y rutas resultantes.

## Flujo de Trabajo del Código

1. Se cargan datos desde archivos CSV (ya sea seleccionando un caso base o ingresando rutas manualmente).
2. Se calculan las distancias entre nodos.
3. Se construye y resuelve el modelo de optimización de ruteo de vehículos.
4. Se genera un archivo JSON con la solución.
5. Se imprimen las rutas y se generan reportes adicionales (CSV con rutas, TXT con el valor objetivo, TXT con informe de costos).
6. Se visualiza la solución sobre un mapa interactivo usando Folium.

