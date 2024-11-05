# Dockerfile
FROM python:3.8.13

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libosmesa6-dev \
    freeglut3-dev \
    libglfw3-dev \
    libgles2-mesa-dev \
    libosmesa6 \
    cmake

# Set environment variables for OpenGL
ENV PYOPENGL_PLATFORM=osmesa

# Copy the entire AnimatedDrawings directory (which includes setup.py)
COPY . /app

# Install the animated_drawings package
RUN pip install -e .

# Copy the contents of the examples directory (if necessary)
WORKDIR /app/examples

# Install any additional dependencies (Flask, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
