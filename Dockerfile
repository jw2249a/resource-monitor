FROM python:3.8-slim

WORKDIR /build

# Install required packages
RUN apt-get update && apt-get install -y sysstat git cmake g++

# Clone rocm-smi and install the package
RUN git clone https://github.com/ROCm/rocm_smi_lib
WORKDIR /build/rocm_smi_lib/build
RUN cmake .. && make -j$(nproc) && make install

# clean cloned directory
RUN rm -r /build

# link executable 
RUN ln -s /opt/rocm/bin/rocm-smi /usr/local/bin/rocm-smi

# create user
WORKDIR /usr/src/app
RUN useradd -m rmanager
USER rmanager

# COPY app.py and requirements
COPY src/ .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install waitress

ENV PATH="$PATH:/home/rmanager/.local/bin/"



# Run app.py when the container launches
CMD ["waitress-serve", "app:app"]
