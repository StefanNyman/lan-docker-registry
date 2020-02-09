#!/usr/bin/env python3

import yaml
import sys
from typing import List

config_filename = 'config.yml'
compose_filename = 'docker-compose.yml'
redis_filename = 'redis.conf'
registry_config_filename = 'registry-config.yml'


def read_redis_config(filename: str) -> List[str]:
    """Read Redis configuration into a list of lines."""
    try:
        with open(filename) as f:
            return [line.strip() for line in f.readlines()]
    except OSError:
        print(f"Error reading {filename}, exiting now.", file=sys.stderr)
        sys.exit(1)


def generate_redis_config(filename: str, config: dict, out_file: str) -> None:
    """Inserts values to appropriate places in redis config"""
    lines = read_redis_config(filename)
    for index in range(len(lines)):
        if lines[index].startswith('bind'):
            lines[index] = f"bind {config['redis']['ip']}"
        elif lines[index].startswith('masterauth'):
            lines[index] = f"masterauth {config['redis']['password']}"
        elif lines[index].startswith('requirepass'):
            lines[index] = f"requirepass {config['redis']['password']}"
    write_file(out_file, '\n'.join(lines))


def read_yaml(filename: str) -> dict:
    """Read a yaml file to a native python dict."""
    try:
        with open(filename) as f:
            return yaml.safe_load(f)
    except OSError as e:
        print(f"Error reading {filename}, exiting now.", file=sys.stderr)
        print(e)
        sys.exit(1)


def write_file(filename: str, content: str):
    """Write string to the given file"""
    try:
        with open(filename, 'w') as f:
            f.write(content)
    except OSError as e:
        print(f"Error writing {filename}, exiting now.", file=sys.stderr)
        print(e)
        sys.exit(1)


def generate_registry_config(filename: str, config: dict, out_file: str) -> None:
    """Generate docker registry config."""
    registry = read_yaml(filename)
    registry['redis']['password'] = config['redis']['password']
    write_file(out_file, yaml.safe_dump(registry))


def generate_docker_compose(filename: str, config: dict, out_file: str) -> None:
    """Generate docker-compose.yml"""
    compose = read_yaml(filename)
    compose['services']['registry']['networks']['registry']['ipv4_address'] = config['registry']['ip']
    compose['services']['redis']['networks']['registry']['ipv4_address'] = config['redis']['ip']
    compose['networks']['registry']['ipam']['config'][0]['subnet'] = config['compose']['subnet']
    write_file(out_file, yaml.safe_dump(compose))


def clean():
    """Clean previously generated config files"""
    from os import remove
    remove(compose_filename)
    remove(redis_filename)
    remove(registry_config_filename)


def generate():
    """Generate config files from templates and config."""
    config = read_yaml(config_filename)
    generate_docker_compose(
        f"template/{compose_filename}", config, compose_filename)
    generate_registry_config(
        f"template/{config_filename}", config, registry_config_filename)
    generate_redis_config(f"template/{redis_filename}", config, redis_filename)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'clean':
            clean()
        else:
            print(f"""Usage: {sys.argv[0]} [COMMAND]
Commands:
    generate  Generate config files.
    help      Show this help message.
    clean     Clean previously generated config files.""")
    else:
        generate()


main()
