FROM golang:1.23-alpine AS builder
# Install necessary tools
RUN apk add --no-cache git gcc musl-dev
WORKDIR /app

# Copy source code and build the Go binary
COPY . /app
RUN go mod download
RUN go build ./cmd/katana

FROM alpine:3.20.3
# Install necessary tools and Python packages
RUN apk add --no-cache bind-tools ca-certificates chromium python3 py3-pip

# Set up virtual environment and install Python dependencies
RUN python3 -m venv /home/.venv && \
    /home/.venv/bin/pip install --no-cache-dir elasticsearch pymongo

# Copy the Go binary from the builder stage
COPY --from=builder /app/katana /usr/local/bin/

# Copy source files (if necessary)
COPY /src/ /home/

# Update PATH to use the virtual environment
ENV PATH="/home/.venv/bin:$PATH"

# Set entrypoint (optional, currently empty)
ENTRYPOINT []
