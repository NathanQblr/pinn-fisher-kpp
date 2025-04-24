#!/bin/bash
docker build -t pinn-fisher-kpp:dev -f docker/Dockerfile .
docker run --rm pinn-fisher-kpp:dev
