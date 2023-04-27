import os
import subprocess

def create_executable(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    pyinstaller_cmd = ['python', '/home/g321/.local/lib/python3.9/site-packages/PyInstaller/__main__.py', script_path]
    subprocess.run(pyinstaller_cmd)

# Replace 'tflite_inference.py' with the name of your script
create_executable('tflite_inference.py')
