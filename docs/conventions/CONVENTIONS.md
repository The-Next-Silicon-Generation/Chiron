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

## 4. Progress and tasks

The two folders works together, the task folders its where the to do list are.
The progress is what we agree about certain topics (ex; the API give us error for x problem use y instead)

This two have the next format:

- For every task the format is: tasks/TASK 0xx Name
- And in progress the associated task have the same name: progress/TASK 0xx Name

## 5. Triage

For the triage the levels are:

- "Rangos normales": Normal ranges
- "Vigilancia": Warning ranges
- "Atención inmediata": Critics ranges