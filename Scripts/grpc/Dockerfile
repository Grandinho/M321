# Golang Build Stage
FROM golang:1.21 AS builder

WORKDIR /app

# Install protoc und gRPC tools
RUN apt-get update && apt-get install -y protobuf-compiler
RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
RUN go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Kopiere Proto-Datei
COPY api.proto .

# Generiere Go-Code aus Proto-Datei
RUN protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    api.proto

# Kopiere und baue den Go-Code
COPY go.mod  ./
RUN go mod download

COPY *.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o analyzer-alpha

# Final Stage
FROM alpine:3.18

WORKDIR /app
COPY --from=builder /app/analyzer-alpha .

EXPOSE 2102
CMD ["./analyzer-alpha"]