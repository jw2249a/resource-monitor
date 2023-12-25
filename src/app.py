from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import subprocess

app = FastAPI()

def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Command failed with error: {error.strip()}")
    return json.loads(output.strip())

@app.get("/iostats", response_class=JSONResponse)
def generate_iostats():
    return execute_command("iostat -h -o JSON")

@app.get("/nvidia", response_class=JSONResponse)
def generate_nvidia():
    return execute_command("nvidia-smi -x -q | xmltojson --stdin")

@app.get("/amd", response_class=JSONResponse)
def generate_amd():
    return execute_command("rocm-smi -aPfutbcglM --json")
