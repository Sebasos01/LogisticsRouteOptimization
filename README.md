# Optimización de Rutas con Restricciones Complejas 🚛📊

¡Bienvenido/a al repositorio de **Optimización de Rutas con Restricciones Complejas**! Este proyecto presenta un enfoque innovador y eficiente para resolver problemas de asignación y optimización de rutas utilizando vehículos terrestres, eléctricos y drones. La solución fue diseñada y desarrollada como parte del proyecto "Seneca Libre" y está fundamentada en análisis cuantitativo, visualizaciones y un enfoque práctico en la reducción de costos operativos.

> **Autores:**  
> - Carlos Casadiego - [cdcp2](https://github.com/cdcp2)
> - Sebastián Ospino - [Sebasos01](https://github.com/Sebasos01)

---

## 🧩 **Descripción del Proyecto**

Este proyecto aborda problemas de optimización de rutas en escenarios diversos, incorporando restricciones realistas como:

- **Capacidades mixtas** de vehículos y centros de distribución.
- **Minimización de costos** operativos (carga, distancia, recarga, mantenimiento, etc.).
- **Gestión de oferta** bajo restricciones de capacidad.
- **Manejo de múltiples productos** con demandas heterogéneas.

Los resultados son ilustrados con rutas optimizadas y desgloses detallados de costos, respaldados por visualizaciones gráficas.

**Escenarios Analizados:**

1. **Escenario Base:** Optimización inicial con restricciones estándar.
2. **Evaluación por Costos:** Reducción de costos totales con alta densidad de clientes.
3. **Gestión de Oferta:** Inclusión de restricciones en la capacidad de centros de distribución.
4. **Manejo de Múltiples Productos:** Complejidad añadida con demandas mixtas y productos heterogéneos.

---

## 📊 **Visualizaciones y Resultados**

Cada escenario incluye:

- **Descripción de parámetros:** Clientes, vehículos, demanda y restricciones específicas.
- **Rutas generadas:** Optimización detallada para cada vehículo.
- **Desglose de costos:** Impacto de cada componente en el costo total.
- **Visualización gráfica:** Mapas de rutas generados para facilitar la comprensión.

### Ejemplo de Visualización 📌
**Ruta generada para el Caso 1:**
![Ruta Caso 1](Docs/ruta_caso1.png)

---

## 🚀 **Características Clave**

- **Adaptabilidad:** El modelo ajusta rutas según restricciones complejas y objetivos personalizados.
- **Eficiencia:** Reducción de costos operativos manteniendo cumplimiento de restricciones.
- **Escalabilidad:** Diseño flexible para incorporar nuevas restricciones o escenarios a futuro.
- **Visualización:** Imágenes y tablas claras para interpretación rápida de resultados.

---

## 📂 **Estructura del Repositorio**

- **Docs/**:
  - Contiene el modelo y el informe de resultados.
  
- **informes/**:
  - Contiene todos los reportes y rutas generadas para los 4 casos de estudio.
  
- **solution.ipynb**:
  - Notebook principal con todo el código del modelo, desde la carga de datos hasta la resolución del problema.
  
- **Geneticos.ipynb**:
  - Contiene el código del bono de algoritmos genéticos para abordar el problema desde un enfoque evolutivo.
---

## 🏆 **Conclusiones**

- La solución propuesta muestra **eficiencia y adaptabilidad** en la asignación de rutas bajo restricciones complejas.
- El desglose detallado de costos permite identificar áreas clave de optimización.
- La integración de múltiples restricciones, como la capacidad de los centros y productos mixtos, demuestra la **flexibilidad del modelo** para resolver problemas reales.

---

## 📖 Documentación general

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

---

## 🛠️ Flujo de Trabajo del Código

1. Se cargan datos desde archivos CSV (ya sea seleccionando un caso base o ingresando rutas manualmente).
2. Se calculan las distancias entre nodos.
3. Se construye y resuelve el modelo de optimización de ruteo de vehículos.
4. Se genera un archivo JSON con la solución.
5. Se imprimen las rutas y se generan reportes adicionales (CSV con rutas, TXT con el valor objetivo, TXT con informe de costos).
6. Se visualiza la solución sobre un mapa interactivo usando Folium.

