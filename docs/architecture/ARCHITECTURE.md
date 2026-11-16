# ARCHITECTURE
How chiron works, how it interacts with the data, which tech stack we use, 
how the apps deploys at infra level.

## CHIRON
Chiron its a health solutions provided to astronauts who lives on the 
space station.

It gives to the personal inside of the ship, the capability to measure
they vital signs and alert if an annomaly it's detected.

## INFRASTRUCTURE
We use an architecture of microservices for comunication between ship,
models and monolithic apps.

- The full software runs on a Ubuntu 26.04 host.

- The host runs the docker images for the software.

- Docker image for service

- Docker compose route the whole images

We use `Github Actions Container Register` for the container images and
an a CI github actions to uploads the images from the repository.

The docker daemon runs on the 