import os
import subprocess


def run():
    current_file_path = os.path.abspath(__file__)
    base_directory = os.path.dirname(current_file_path)
    print(base_directory)
    print(current_file_path)

    utils_dir = os.path.join(base_directory, "utils")
    venv_path = os.path.join(base_directory, ".venv", "Scripts", "activate")
    script_get_all_data_path = os.path.join(
        utils_dir, "script_get_all_data.bat"
    )
    formatter_path = os.path.join(utils_dir, "formatter.py")
    result_geojson_path = os.path.join(utils_dir, "result.geojson")
    target_geojson_path = os.path.join(
        base_directory, "static", "geodata", "result.geojson"
    )

    # Активация виртуального окружения
    activate_command = f"call {venv_path}"
    subprocess.run(activate_command, shell=True, cwd=base_directory)

    # Запуск script_get_all_data.bat
    subprocess.run(script_get_all_data_path, shell=True, cwd=utils_dir)

    # Запуск formatter.py
    python_executable = os.path.join(
        base_directory, ".venv", "Scripts", "python.exe"
    )
    subprocess.run([python_executable, formatter_path], cwd=utils_dir)

    if os.path.exists(result_geojson_path):
        os.replace(result_geojson_path, target_geojson_path)
        print(f"Файл result.geojson успешно перемещен в {target_geojson_path}")
    else:
        print("Файл result.geojson не найден.")

    deactivate_command = "deactivate"
    subprocess.run(deactivate_command, shell=True, cwd=base_directory)


if __name__ == "__main__":
    run()
