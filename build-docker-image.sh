#!/bin/bash
docker build \
    --squash \
    -t registry.gitlab.com/alex4401/arkse-mobile-extraction:$1 \
    -f docker/Dockerfile \
    .