from fastapi import FastAPI
from starlette.responses import StreamingResponse
import subprocess

app = FastAPI()

async def generator(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=False)
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                yield output
    finally:
        process.terminate()


@app.get("/iostats")
async def generate_iostats():
    return StreamingResponse(generator("iostat 5 | jc --iostat-s -u"), media_type="text/plain")

@app.get("/nvidia")
async def generate_nvidia():
    return StreamingResponse(generator("while true; do nvidia-smi -x -q | xmltojson --stdin; sleep 5; done"), media_type="text/plain")

@app.get("/amd")
async def generate_amd():
    return StreamingResponse(generator("while true; do rocm-smi -aPfutbcglM --json; sleep 5; done"), media_type="text/plain")
