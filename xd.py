import pandas as pd
import os
import json
import math

# Inicializar el diccionario de datos
data = {
    "N": [],
    "TP": ['Cliente', 'Depósito'],
    "V": [],
    "TV": ['Gasolina/Gas', 'EV', 'Dron'],
    "CV": ['Terrestre', 'Aereo'],
    "CategoriaTipoVehiculo": {
        'Gasolina/Gas': 'Terrestre',
        'EV': 'Terrestre',
        'Dron': 'Aereo',
    },

    "CostoCarga": None,
    "CostoDescarga": None,
    "VelocidadCarga": None,
    "VelocidadDescarga": None,

    "TipoNodo": {},
    "UbicacionNodo": {},
    "DemandaEnvio": {},
    "CapacidadDeposito": {},

    "TipoVehiculo": {},
    "CapacidadVehiculo": {},
    "RangoVehiculo": {},
    "TarifaFleteTipoVehiculo": {},
    "TarifaHorariaTipoVehiculo": {},
    "MantenimientoTipoVehiculo": {},
    "CostoRecargaTipoVehiculo": {},
    "TiempoRecargaTipoVehiculo": {},
    "VelocidadTipoVehiculo": {},
    "EficienciaTipoVehiculo": {},

    "d": None
}

# Diccionarios para mapear IDs sin prefijo a IDs con prefijo
node_id_map = {}
vehicle_id_map = {}

def read_clients(data, client_csv_paths):
    for path in client_csv_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Client CSV file not found: {path}")
        df = pd.read_csv(path)
        required_columns = ['ClientID', 'Longitude', 'Latitude', 'Product']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Client CSV missing required columns: {required_columns}")
        for index, row in df.iterrows():
            client_id_raw = row['ClientID']
            # Convertir a entero si es float con valor entero
            if isinstance(client_id_raw, float) and client_id_raw.is_integer():
                client_id_raw = int(client_id_raw)
            client_id_raw = str(client_id_raw)
            client_id = f"c{client_id_raw}"
            if client_id in data['N']:
                raise ValueError(f"Duplicate ClientID found: {client_id}")
            data['N'].append(client_id)
            data['TipoNodo'][client_id] = 'Cliente'
            product = row['Product']
            if product < 0:
                raise ValueError(f"Product demand must be >= 0 for ClientID {client_id}")
            data['DemandaEnvio'][client_id] = float(product)
            longitude = row['Longitude']
            latitude = row['Latitude']
            if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
                raise ValueError(f"Invalid coordinates for ClientID {client_id}")
            data['UbicacionNodo'][client_id] = (latitude, longitude)
            # Agregar al mapeo
            node_id_map[str(client_id_raw)] = client_id

def read_depots(data, depot_csv_paths):
    for path in depot_csv_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Depot CSV file not found: {path}")
        df = pd.read_csv(path)
        required_columns = ['DepotID', 'Longitude', 'Latitude']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Depot CSV missing required columns: {required_columns}")
        for index, row in df.iterrows():
            depot_id_raw = row['DepotID']
            # Convertir a entero si es float con valor entero
            if isinstance(depot_id_raw, float) and depot_id_raw.is_integer():
                depot_id_raw = int(depot_id_raw)
            depot_id_raw = str(depot_id_raw)
            depot_id = f"d{depot_id_raw}"
            if depot_id in data['N']:
                raise ValueError(f"Duplicate DepotID found: {depot_id}")
            data['N'].append(depot_id)
            data['TipoNodo'][depot_id] = 'Depósito'
            longitude = row['Longitude']
            latitude = row['Latitude']
            if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
                raise ValueError(f"Invalid coordinates for DepotID {depot_id}")
            data['UbicacionNodo'][depot_id] = (latitude, longitude)
            # Agregar al mapeo
            node_id_map[str(depot_id_raw)] = depot_id


def read_vehicles(data, vehicle_csv_paths):
    vehicle_id = 1
    for path in vehicle_csv_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Vehicle CSV file not found: {path}")
        df = pd.read_csv(path)
        required_columns = ['VehicleType', 'Capacity', 'Range']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Vehicle CSV missing required columns: {required_columns}")
        for index, row in df.iterrows():
            vehicle_type_raw = row['VehicleType']
            if vehicle_type_raw == 'Gas Car':
                vehicle_type = 'Gasolina/Gas'
            elif vehicle_type_raw == 'EV':
                vehicle_type = 'EV'
            elif vehicle_type_raw == 'drone':
                vehicle_type = 'Dron'
            else:
                raise ValueError(f"Invalid VehicleType: {vehicle_type_raw}")
            capacity = row['Capacity']
            if capacity < 0:
                raise ValueError(f"Capacity must be >= 0 for VehicleID {vehicle_id}")
            range_ = row['Range']
            if range_ < 0:
                raise ValueError(f"Range must be >= 0 for VehicleID {vehicle_id}")
            vehicle_id_str = "v" + str(vehicle_id)
            data['V'].append(vehicle_id_str)
            data['TipoVehiculo'][vehicle_id_str] = vehicle_type
            data['CapacidadVehiculo'][vehicle_id_str] = capacity
            data['RangoVehiculo'][vehicle_id_str] = range_
            vehicle_id += 1

def is_float_with_zero_decimals(s):
    try:
        num = float(s)
        return num.is_integer()
    except ValueError:
        return False

def read_depot_capacities(data, depot_capacity_csv_paths):
    for path in depot_capacity_csv_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Depot Capacity CSV file not found: {path}")
        df = pd.read_csv(path)
        required_columns = ['DepotID']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Depot Capacity CSV missing required columns: {required_columns}")
        for index, row in df.iterrows():
            depot_id = str(row['DepotID'].item())
            depot_id = "d" + (str(int(float(depot_id))) if is_float_with_zero_decimals(depot_id) else depot_id)
            if depot_id not in data['N'] or data['TipoNodo'].get(depot_id) != 'Depósito':
                raise ValueError(f"DepotID {depot_id} not found among depots.")
            product = 0
            for p in ["Product-Type-A","Product-Type-B","Product-Type-C", "Product"]:
                product += row.get(p, 0)
            if product < 0:
                raise ValueError(f"Product capacity must be >= 0 for DepotID {depot_id}")
            product = float(product.item())
            data['CapacidadDeposito'][depot_id] = product

def read_loading_products(data, loading_products_csv_paths):
    loading_cost_set = False
    unloading_cost_set = False
    loading_speed_set = False
    unloading_speed_set = False

    for path in loading_products_csv_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Loading Products CSV file not found: {path}")
        df = pd.read_csv(path)
        required_columns = ['Activity', 'Cost [COP/min]', 'Loading Speed [kg/min]']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Loading Products CSV missing required columns: {required_columns}")
        if len(df) < 1 or len(df) > 2:
            raise ValueError("Loading Products CSV must have 1 or 2 rows.")
        for index, row in df.iterrows():
            activity = row['Activity']
            cost = row['Cost [COP/min]']
            speed = row['Loading Speed [kg/min]']
            if cost < 0 or speed < 0:
                raise ValueError("Cost and Speed must be >= 0.")
            if activity == 'Loading/Unloading':
                if loading_cost_set or unloading_cost_set:
                    raise ValueError("Duplicate Loading/Unloading activity.")
                data['CostoCarga'] = cost
                data['CostoDescarga'] = cost
                data['VelocidadCarga'] = speed
                data['VelocidadDescarga'] = speed
                loading_cost_set = unloading_cost_set = True
                loading_speed_set = unloading_speed_set = True
            elif activity == 'Loading':
                if loading_cost_set:
                    raise ValueError("Duplicate Loading activity.")
                data['CostoCarga'] = cost
                data['VelocidadCarga'] = speed
                loading_cost_set = True
                loading_speed_set = True
            elif activity == 'Unloading':
                if unloading_cost_set:
                    raise ValueError("Duplicate Unloading activity.")
                data['CostoDescarga'] = cost
                data['VelocidadDescarga'] = speed
                unloading_cost_set = True
                unloading_speed_set = True
            else:
                raise ValueError(f"Invalid Activity type: {activity}")
    if not (loading_cost_set and unloading_cost_set and loading_speed_set and unloading_speed_set):
        raise ValueError("Incomplete loading/unloading data.")

def read_vehicle_types(data, vehicle_types_csv_paths):
    vehicle_types_set = set()
    for path in vehicle_types_csv_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Vehicle Types CSV file not found: {path}")
        df = pd.read_csv(path)
        required_columns = ['Vehicle', 'Freight Rate [COP/km]', 'Time Rate [COP/min]',
                            'Daily Maintenance [COP/day]', 'Recharge/Fuel Cost [COP/(gal or kWh)]',
                            'Recharge/Fuel Time [min/10 percent charge]', 'Avg. Speed [km/h]',
                            'Gas Efficiency [km/gal]', 'Electricity Efficency [kWh/km]']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Vehicle Types CSV missing required columns: {required_columns}")
        if len(df) != 3:
            raise ValueError("Vehicle Types CSV must have exactly 3 rows.")
        for index, row in df.iterrows():
            vehicle_raw = row['Vehicle']
            if vehicle_raw == 'Gas Car':
                vehicle = 'Gasolina/Gas'
            elif vehicle_raw == 'Drone':
                vehicle = 'Dron'
            elif vehicle_raw == 'Solar EV':
                vehicle = 'EV'
            else:
                raise ValueError(f"Invalid Vehicle type: {vehicle_raw}")
            if vehicle in vehicle_types_set:
                raise ValueError(f"Duplicate Vehicle type: {vehicle}")
            vehicle_types_set.add(vehicle)
            freight_rate = row['Freight Rate [COP/km]']
            time_rate = row['Time Rate [COP/min]']
            maintenance = row['Daily Maintenance [COP/day]']
            recharge_cost = row['Recharge/Fuel Cost [COP/(gal or kWh)]']
            recharge_time = row['Recharge/Fuel Time [min/10 percent charge]']
            avg_speed = row['Avg. Speed [km/h]']
            gas_efficiency = row['Gas Efficiency [km/gal]']
            electricity_efficiency = row['Electricity Efficency [kWh/km]']

            if freight_rate < 0 or time_rate < 0 or maintenance < 0:
                raise ValueError(f"Rates and maintenance must be >= 0 for Vehicle {vehicle}")
            data['TarifaFleteTipoVehiculo'][vehicle] = freight_rate
            data['TarifaHorariaTipoVehiculo'][vehicle] = time_rate
            data['MantenimientoTipoVehiculo'][vehicle] = maintenance

            if vehicle == 'EV':
                # Ignore recharge_cost and recharge_time if empty
                if pd.notnull(recharge_cost):
                    raise ValueError("Recharge/Fuel Cost should be empty for EV.")
                if pd.notnull(recharge_time):
                    raise ValueError("Recharge/Fuel Time should be empty for EV.")
                if electricity_efficiency <= 0:
                    raise ValueError("Electricity Efficiency must be > 0 for EV.")
                data['CostoRecargaTipoVehiculo'][vehicle] = 0
                data['TiempoRecargaTipoVehiculo'][vehicle] = 0
                data['EficienciaTipoVehiculo'][vehicle] = electricity_efficiency
            elif vehicle == 'Dron':
                if recharge_cost < 0 or recharge_time < 0:
                    raise ValueError(f"Recharge Cost and Time must be >= 0 for Vehicle {vehicle}")
                if electricity_efficiency <= 0:
                    raise ValueError("Electricity Efficiency must be > 0 for Dron.")
                data['CostoRecargaTipoVehiculo'][vehicle] = recharge_cost
                data['TiempoRecargaTipoVehiculo'][vehicle] = recharge_time
                data['EficienciaTipoVehiculo'][vehicle] = electricity_efficiency
            elif vehicle == 'Gasolina/Gas':
                if recharge_cost < 0 or recharge_time < 0:
                    raise ValueError(f"Fuel Cost and Time must be >= 0 for Vehicle {vehicle}")
                if gas_efficiency <= 0:
                    raise ValueError("Gas Efficiency must be > 0 for Gasolina/Gas.")
                data['CostoRecargaTipoVehiculo'][vehicle] = recharge_cost
                data['TiempoRecargaTipoVehiculo'][vehicle] = recharge_time
                data['EficienciaTipoVehiculo'][vehicle] = gas_efficiency
            else:
                raise ValueError(f"Unknown vehicle type: {vehicle}")

            if avg_speed <= 0:
                raise ValueError(f"Avg. Speed must be > 0 for Vehicle {vehicle}")
            data['VelocidadTipoVehiculo'][vehicle] = avg_speed

# Las demás funciones de lectura se mantienen igual...

def haversine(coord1, coord2):
    """Calcula la distancia Haversine entre dos coordenadas geográficas."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Radio de la Tierra en kilómetros
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def compute_distance_matrix(data):
    nodes = data['N']
    node_coords = {node: data['UbicacionNodo'][node] for node in nodes}

    # Calcular distancias para vehículos terrestres y aéreos
    for cv in data['CV']:
        for i in nodes:
            for j in nodes:
                coord_i = node_coords[i]
                coord_j = node_coords[j]
                distance = haversine(coord_i, coord_j)
                data['d'][cv][i][j] = distance

def get_base_case_paths(base_case):
    # Rutas predefinidas para casos base
    base_case_paths = {
        '1': {
            'clients': ['C:\\Users\\cdcp2\\Desktop\\MOS\\proyecto_e2\\case_1_base\\Clients.csv'],
            'vehicles': ['C:\\Users\\cdcp2\\Desktop\\MOS\\proyecto_e2\\case_1_base\\Vehicles.csv'],
            'depots': ['C:\\Users\\cdcp2\\Desktop\\MOS\\proyecto_e2\\case_1_base\\Depots.csv'],
            'depot_capacities': [],
            'loading_products': ['C:\\Users\\cdcp2\\Desktop\\MOS\\proyecto_e2\\loading_costs.csv'],
            'vehicle_types': ['C:\\Users\\cdcp2\\Desktop\\MOS\\proyecto_e2\\vehicles_data.csv']
        },
        # Agrega más casos base según sea necesario
    }
    return base_case_paths[base_case]

# Cargar datos
base_case = '1'  # Puedes cambiar al caso que desees
paths = get_base_case_paths(base_case)

# Leer y procesar archivos CSV
read_clients(data, paths['clients'])
read_vehicles(data, paths['vehicles'])
read_depots(data, paths['depots'])

if paths['depot_capacities']:
    read_depot_capacities(data, paths['depot_capacities'])
else:
    # Establecer capacidad infinita para todos los depósitos
    for depot_id in data['N']:
        if data['TipoNodo'][depot_id] == 'Depósito':
            data['CapacidadDeposito'][depot_id] = float('inf')

read_loading_products(data, paths['loading_products'])
read_vehicle_types(data, paths['vehicle_types'])

# Crear matriz de distancias
data["d"] = {cv: {i: {j: 0 for j in data["N"]} for i in data["N"]} for cv in data["CV"]}

# Calcular la matriz de distancias
compute_distance_matrix(data)

# Lista de archivos JSON de salida
json_files = [
    "C:\\Users\\cdcp2\\Desktop\\MOS\\proyecto_e2\\output1.json",
    "C:\\Users\\cdcp2\\Desktop\\MOS\\proyecto_e2\\output2.json",
    "C:\\Users\\cdcp2\\Desktop\\MOS\\proyecto_e2\\output3.json",
    "C:\\Users\\cdcp2\\Desktop\\MOS\\proyecto_e2\\output4.json"
]

def parse_key_r(key_str):
    """Parsea una clave de cadena y mapea los IDs sin prefijo a IDs con prefijo."""
    key_str = key_str.strip('()')
    parts = key_str.split(', ')
    i_raw = parts[0].strip("'\"")
    j_raw = parts[1].strip("'\"")
    v_raw = parts[2].strip("'\"")

    # Mapear los IDs de nodos
    i = node_id_map.get(i_raw, i_raw)
    j = node_id_map.get(j_raw, j_raw)
    # Mapear el ID del vehículo
    v = vehicle_id_map.get(v_raw, v_raw)

    return (i, j, v)

def reconstruct_route(edges):
    """Reconstruye la ruta completa a partir de los arcos."""
    # Construir el diccionario de adyacencia
    adjacency = {}
    for i, j in edges:
        adjacency[i] = j

    # Encontrar el nodo inicial (suponemos que es un depósito)
    start_nodes = set(adjacency.keys()) - set(adjacency.values())
    if start_nodes:
        start_node = start_nodes.pop()
    else:
        start_node = edges[0][0]  # Fallback si no se encuentra el inicio

    route = [start_node]
    next_node = adjacency.get(start_node)
    visited = set(route)
    while next_node and next_node != start_node and next_node not in visited:
        route.append(next_node)
        visited.add(next_node)
        next_node = adjacency.get(next_node)

    return route

def process_json_file(json_path, data):
    """Procesa un archivo JSON para extraer rutas y calcular costos."""
    with open(json_path, 'r') as file:
        json_data = json.load(file)

    # Extraer la matriz 'r' (asignaciones de rutas)
    r_matrix = json_data['r']
    # Convertir claves de cadena a tuplas
    r_matrix = {parse_key_r(key): value for key, value in r_matrix.items()}

    # Construir rutas para cada vehículo
    vehicle_routes = {}
    for (i, j, v), value in r_matrix.items():
        if value == 1:
            if v not in vehicle_routes:
                vehicle_routes[v] = []
            vehicle_routes[v].append((i, j))

    # Reconstruir la ruta completa para cada vehículo
    vehicle_full_routes = {}
    for v, edges in vehicle_routes.items():
        route = reconstruct_route(edges)
        vehicle_full_routes[v] = route

    # Obtener parámetros de vehículos y nodos
    vehicle_params = data['TipoVehiculo']
    vehicle_speeds = data['VelocidadTipoVehiculo']
    vehicle_efficiencies = data['EficienciaTipoVehiculo']
    vehicle_maintenance = data['MantenimientoTipoVehiculo']
    vehicle_freight_rates = data['TarifaFleteTipoVehiculo']
    vehicle_time_rates = data['TarifaHorariaTipoVehiculo']
    vehicle_recharge_costs = data['CostoRecargaTipoVehiculo']

    node_coordinates = data['UbicacionNodo']

    # Calcular costos para cada vehículo
    cost_breakdown = []
    for v in data['V']:
        vehicle_type = vehicle_params[v]
        params = {
            'TarifaDistancia': vehicle_freight_rates[vehicle_type],
            'Velocidad': vehicle_speeds[vehicle_type],
            'Eficiencia': vehicle_efficiencies[vehicle_type],
            'CostoRecarga': vehicle_recharge_costs[vehicle_type],
            'Mantenimiento': vehicle_maintenance[vehicle_type],
            'TarifaTiempo': vehicle_time_rates[vehicle_type]
        }

        route = vehicle_full_routes.get(v, [])
        if route:
            # Calcular distancia total
            total_distance = 0
            for idx in range(len(route) - 1):
                node_i = route[idx]
                node_j = route[idx + 1]
                if node_i not in node_coordinates:
                    raise KeyError(f"Nodo {node_i} no encontrado en node_coordinates")
                if node_j not in node_coordinates:
                    raise KeyError(f"Nodo {node_j} no encontrado en node_coordinates")
                coord_i = node_coordinates[node_i]
                coord_j = node_coordinates[node_j]
                dist = haversine(coord_i, coord_j)
                total_distance += dist

            # Calcular costos
            costo_distancia = total_distance * params['TarifaDistancia']
            tiempo_viaje = total_distance / params['Velocidad'] * 60  # Convertir a minutos
            costo_tiempo = tiempo_viaje * params['TarifaTiempo']
            consumo = total_distance / params['Eficiencia']
            costo_recarga = consumo * params['CostoRecarga']
            costo_mantenimiento = params['Mantenimiento']
            costo_total = costo_distancia + costo_tiempo + costo_recarga + costo_mantenimiento
        else:
            # Vehículo no utilizado
            total_distance = 0
            costo_distancia = 0
            tiempo_viaje = 0
            costo_tiempo = 0
            consumo = 0
            costo_recarga = 0
            costo_mantenimiento = params['Mantenimiento']
            costo_total = costo_mantenimiento

        # Agregar al desglose de costos
        cost_breakdown.append({
            'Vehículo': v,
            'Tipo': vehicle_type,
            'Distancia (km)': round(total_distance, 2),
            'Costo Distancia (COP)': round(costo_distancia, 2),
            'Tiempo de Viaje (min)': round(tiempo_viaje, 2),
            'Costo Tiempo (COP)': round(costo_tiempo, 2),
            'Consumo (gal o kWh)': round(consumo, 2),
            'Costo Recarga (COP)': round(costo_recarga, 2),
            'Costo Mantenimiento (COP)': round(costo_mantenimiento, 2),
            'Costo Total (COP)': round(costo_total, 2)
        })

    return cost_breakdown

# Procesar cada archivo JSON y recopilar los desgloses de costos
all_costs = []
for json_file in json_files:
    if os.path.exists(json_file):
        costs = process_json_file(json_file, data)
        all_costs.extend(costs)
    else:
        print(f"File {json_file} not found.")

# Convertir a DataFrame para mejor presentación
df_costs = pd.DataFrame(all_costs)
print(df_costs)

# Guardar en CSV si es necesario
df_costs.to_csv('cost_breakdown.csv', index=False)
