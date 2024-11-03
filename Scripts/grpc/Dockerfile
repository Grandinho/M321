FROM python:3.9-slim

WORKDIR /app

# Install required packages
RUN apt-get update && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install grpcio grpcio-tools pymongo

# Copy proto file
COPY api.proto .

# Generate Python files from proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. api.proto

# Copy server implementation
COPY server.py .
COPY shield_generator.py .

# Expose the gRPC port
EXPOSE 2102

CMD ["python", "server.py"]