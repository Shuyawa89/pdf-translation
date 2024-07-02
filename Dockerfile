# Dockerfile
FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-devel

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-venv \
    git \
    cmake \
    ninja-build \
    && apt-get clean

# Install Python packages
COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt

# Install detectron2
RUN pip install 'git+https://github.com/facebookresearch/detectron2.git'

# Copy the application code
COPY . .

# Set the entrypoint and default command
ENTRYPOINT ["python3"]
CMD ["main.py"]
