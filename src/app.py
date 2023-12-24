from flask import Flask, Response, stream_with_context
import subprocess
import time
app = Flask(__name__)


def generate_iostats():
    return generator("iostat 5 | jc --iostat-s -u")

def generate_nvidia():
    return generator("while true; do nvidia-smi -x -q | xmltojson --stdin; sleep 5; done")

def generate_amd():
    return generator("while true; do rocm-smi -aPfutbcglM --json; sleep 5; done")

routes = [
    ('/iostats', generate_iostats),
    ('/nvidia', generate_nvidia),
    ('/amd', generate_amd)
]

def generator(command):
    # Start the sar subprocess
    _process = subprocess.Popen(command,
                                shell=True, \
                                stdout=subprocess.PIPE,\
                                universal_newlines=False)

    try:
        while True:
            output = _process.stdout.readline()
            if output == '' and _process.poll() is not None:
                break
            if output:
                yield output
            else:
                time.sleep(0.1)
    except GeneratorExit:
        # Client disconnected; clean up
        _process.terminate()
        try:
            _process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            _process.kill()


for route, view_func in routes:
    view_func = app.route(route)(view_func)


if __name__ == '__main__':
    app.run(debug=True, threaded=True,host='0.0.0.0')
