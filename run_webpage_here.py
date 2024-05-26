import subprocess
import time
import os

script_name = "webpage.py"
venv_path = "venv"

while True:
    # Run the script
    print(f"Running {script_name}...")
    activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
    activate_cmd = f"{activate_script} && python {script_name}"
    process = subprocess.Popen(activate_cmd, shell=True)

    # Wait for 10 seconds
    time.sleep(10)

    # Terminate the script process
    print("Terminating the script...")
    process.terminate()

    # Wait for the process to terminate
    process.wait()
