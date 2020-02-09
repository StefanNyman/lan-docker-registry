#!/usr/bin/env python3

import yaml
import sys


def read_yaml(filename: str) -> dict:
    try:
        with open(filename) as f:
            return yaml.safe_load(f)
    except OSError:
        print(f"Error reading {filename}, exiting now.", file=sys.stderr)
        sys.exit(1)


def generate_registry_config(filename: str, config: dict) -> None:
    pass


def generate_redis_config(filename: str, config: dict) -> None:
    pass


def generate_docker_compose(filename: str, config: dict) -> None:
    pass


config_filename = 'config.yml'
compose_filename = 'docker-compose.yml'
redis_filename = 'redis.conf'

config = read_yaml(config_filename)
registry_config = read_yaml(f'template/{config_filename}')
