import os
import subprocess
import sys

def build():
    print("Iniciando compilación de la aplicación A-P-R-C-H con PyInstaller...")

    # Definir rutas principales
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entry_point = os.path.join(project_root, "src", "main.py")
    
    # Determinar el ejecutable de PyInstaller dentro del entorno virtual
    if sys.platform == "win32":
        pyinstaller_bin = os.path.join(project_root, ".venv", "Scripts", "pyinstaller.exe")
    else:
        pyinstaller_bin = os.path.join(project_root, ".venv", "bin", "pyinstaller")
        
    # Verificar si PyInstaller existe en el entorno virtual
    if not os.path.exists(pyinstaller_bin):
        print(f"Error: No se encontró PyInstaller en el entorno virtual: {pyinstaller_bin}")
        print("Por favor instala pyinstaller usando: pip install pyinstaller")
        sys.exit(1)

    # Configuración de PyInstaller
    cmd = [
        pyinstaller_bin,
        "--noconfirm",
        "--windowed",
        "--name=A-P-R-C-H",
        f"--paths={project_root}",
        f"--add-data={os.path.join(project_root, 'data')}{os.path.pathsep}data",
        entry_point
    ]

    print(f"Ejecutando comando: {' '.join(cmd)}")
    
    # Ejecutar la compilación
    try:
        subprocess.run(cmd, check=True, cwd=project_root)
        print("\n¡Compilación completada exitosamente!")
        print(f"Encontrarás el instalador/ejecutable en la carpeta: {os.path.join(project_root, 'dist', 'A-P-R-C-H')}")
    except subprocess.CalledProcessError as e:
        print(f"\nError durante la compilación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
