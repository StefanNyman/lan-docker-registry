# Local Network Docker Registry

This project attempts to simplify creating a docker pull through cache for local environments.

## Configuration

- If necessary, edit `config.yml` file.

## Installation

- Run `make.py` file to generate proper config files from templates in template dir.
- Run `docker-compose up -d` to start the registry server.
- Add contents of `daemon.json` file to the __client__ docker daemon configuration.

### Notes

- HTTPS is __not__ supported since this deployment isn't intended to be exposed to the internet.  
  If you wish to deploy to somewhere that's exposed to the internet, see [Docker Documentation](https://docs.docker.com/registry/deploying/#run-an-externally-accessible-registry)

- For local domain name, consider using a zeroconf solution, see [Arch Wiki](https://wiki.archlinux.org/index.php/Avahi) for details.
