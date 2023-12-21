import os
import subprocess
import json

def scan_code(target):
    if os.path.isfile(target):
        scan_file(target)
    elif os.path.isdir(target):
        scan_directory(target)
    else:
        print(f"El objetivo '{target}' no es un archivo ni un directorio válido.")

def scan_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Scanning: {file_path}")
                scan_file(file_path)

def scan_file(file_path):
    try:
        result = subprocess.check_output(
            ["bandit", "-r", "-f", "json", file_path],
            universal_newlines=True,
            stderr=subprocess.STDOUT,
        )
        handle_bandit_results(result, file_path)
    except subprocess.CalledProcessError as e:
        print(e.output)

def handle_bandit_results(result, file_path):
    try:
        issues = json.loads(result)
        if not issues:
            print(f"No se encontraron vulnerabilidades en: {file_path}")
            return

        print("\nVulnerabilities found:")
        for issue in issues:
            print("--------------------")
            print(f"Severity: {issue['issue_severity']}")
            print(f"ID: {issue['test_id']}")
            print(f"Description: {issue['issue_text']}")
            print(f"File: {file_path}")
            print(f"Line: {issue['line_number']}")
            print(f"Code snippet:\n{issue['code']}")
            print("--------------------")

        # Agrega aquí la lógica para manejar las vulnerabilidades encontradas
        # por ejemplo, enviar alertas, registrar en una base de datos, etc.

        print("\nDetails:")
        print("Consider reviewing and addressing these vulnerabilities.")
    except json.JSONDecodeError:
        print(f"No se encontraron vulnerabilidades en: {file_path}")

if __name__ == "__main__":
    user_target = input("Ingrese el nombre de archivo o directorio a escanear: ").strip()
    scan_code(user_target)
