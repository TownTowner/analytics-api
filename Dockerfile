# https://codingforentrepreneurs.com/blog/deploy-fastapi-to-railway-with-this-dockerfile
# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN pip install uv && uv venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install os dependencies for our mini vm
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code

# Copy the requirements file into the container
# COPY requirements.txt /tmp/requirements.txt

# copy the project code into the container's working directory
COPY ./src /code

# Install the Python project requirements
COPY pyproject.toml /code/
RUN uv pip install -e .

# database isn't available during build
# run any other commands that do not need the database
# such as:
# RUN python manage.py collectstatic --noinput

COPY ./boot/docker-run.sh /opt/docker-run.sh

# make the bash script executable
RUN chmod +x /opt/docker-run.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the FastAPI project via the runtime script
# when the container starts
CMD ["/opt/docker-run.sh"]