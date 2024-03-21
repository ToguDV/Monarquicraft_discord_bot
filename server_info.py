import os
import yaml


def set_data(key, value, root_dir):
    file_path = f"{root_dir}/data/server_info.yml"
    # Verificar si el archivo ya existe
    check_file = os.path.exists(file_path)
    # Cargar datos actuales si el archivo existe
    if check_file:
        with open(file_path, 'r') as archivo_yml:
            try:
                current_data = yaml.load(archivo_yml, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                print(exc)
                return

        # Combinar datos actuales con los nuevos datos
        current_data[key] = value
    else:
        # Si el archivo no existe, crear un nuevo diccionario y archivo
        f = open(file_path, "x")
        current_data = {key: value}

    # Escribir los datos en el archivo YAML
    with open(file_path, 'w') as archivo_yml:
        yaml.dump(current_data, archivo_yml)


def get_data_yml(root_dir):
    file_path = f"{root_dir}/data/server_info.yml"
    check_file = os.path.exists(file_path)
    if not check_file: return
    with open(file_path, 'r') as archivo_yml:
        data = yaml.load(archivo_yml, Loader=yaml.FullLoader)
        return data
