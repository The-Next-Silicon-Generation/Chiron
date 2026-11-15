# CONVENTIONS
This document have the whole conventions to build the Chiron app.

## CONSTRAINTS
This file include:
- The conventions we reach from the project development
- This file have the purpouse to give the guidance of what we use and what we don't use.

This file don't include:
- The architectures
- Security
- Previuos Tasks

## 1. API CONVENTION
For the comunication between astronaut and the server we use the API type websocket

This help us to improve the real time streaming data with low latency.

## 2. Programming language.
We use python for the backend. The reason? Because its simplicity and versatility.

For the API we use `fast API`.

On the frontend we use JS with html and CSS

## 3. Deployment
We use docker images for availability.

The compose integrates the high availability.

The repository will use GH actions for the CI/CD

Workflows put's CI as testing phase but CD should be Continuous Delivery not deployment.
