FROM python:3.8

RUN apt-get update && \
	apt-get install -y && \
	useradd -m --shell /bin/bash --no-user-group user && \
	chmod g+w /etc/passwd && \
	echo "user	ALL=(ALL)	NOPASSWD:	ALL" >> /etc/sudoers && \
	# Prevent apt-get cache from being persisted to this layer.
	rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1 \
	POETRY_VERSION=1.1.13

RUN pip install "poetry==$POETRY_VERSION"
# Disable virtual environments
RUN poetry config virtualenvs.create false

# Set the working directory for all the subsequent Dockerfile instructions.
WORKDIR /SentimentalBB

# Copy the environment definition file and install the environment
COPY pyproject.toml poetry.lock ./
RUN poetry install

# Pass the git commit hash
ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}


# Copy the content of the repository to the Docker.
COPY . .

# Configure the kernel for Jupyter
RUN python -m ipykernel install --sys-prefix
# Make the default shell bash (vs "sh") for a better Jupyter terminal UX
ENV SHELL=/bin/bash

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

USER user
