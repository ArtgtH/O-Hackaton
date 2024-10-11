FROM golang:1.22.2-alpine AS builder

WORKDIR /build

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o backend app/main.go

FROM alpine:latest

COPY --from=builder ["/build/backend", "/"]

ENTRYPOINT ["/backend"]