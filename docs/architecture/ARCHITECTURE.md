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

The docker daemon runs on the background to supply continuous containers
to the backend/frontend/ML

We use CD to launch a new version of the code when we made approved chang-
es to production.

This project will grow to a cloud enviorment, the IaC will be the main idea
for this objective.

- Terraform: Build the main infra to deploy the main server
- We don't use kubernetes yet

### Comunication between the docker and exterior:

- The open port for comunication between the frontend interface and backend is: 8080
- The open port for comunication between the data stream interface and backend is: 8001

### Comunication between internal sockets:

- The open port for comunication between the backend and the predictive model is: 80002
- The open port for comunication between database and backend is: 3306
- The open port for comunication between the backend and the contextual model is: 80003

## MACHINE LEARNING

### Predictive model
We already train a predictive model for vital signs monitoring. This model
have an adaptative feature. It doesn't work with only trained data (that is 
another learnign that we include) but with a delta change variable, we try
to predict the next vital sign from a patron learning of the model.

Delta is the coefficent of change in the time, we want to delta stay on 
certain range, when the coefficent arrise, something it's wrong

The model gives the next JSON output:


```JSON
{
  "astronaut_id": "astro-1", "timestamp": 912.0, "model_version": "gru-v1",
  "status": "ok",                       // or "warming_up"
  "horizon_s": 120, "sample_rate_hz": 1.0,
  "baseline": {"hr": 65.0, "spo2": 98.0, ...},  // personal baseline, from the first 120 s
  "delta": {
    "per_vital": {"hr": {"window": .., "observed": .., "session": ..,
                         "danger_window": .., "danger_observed": .., "confidence": .., ...}},
    "shock_index_delta": .., "shock_index_observed": .., "confidence": ..
  },
  "zone": {
    "overall": "normal|watch|alert", "level": 0|1|2,
    "per_vital": {"hr": "watch", ...}, "shock_index": "normal",
    "reasons": [{"vital": "hr", "metric": "window_delta", "zone": "watch", "score": 0.17, "threshold": 0.157}],
    "low_confidence": false,
    "recommended_source": "ml"          // or "deterministic", meaning "trust NEWS2 instead"
  },
  "forecast": {"hr": {"p10": [...120], "p50": [...], "p90": [...]}, ...}
}
```

### Contextual model (Future feature)

This model will recieve the full context data on the pipeline, it's our last step
on the pipeline.
It uses the context given from the predictive model and the triage from the backend
to deduce from a categorize learning,  if this alert it's a false positive, an error
or is a real emergency.


## BACKEND
The backend works as a messenger:

- Comunicate the interested parts (API)
- Send the streaming data to the ML predictive model.
- Receive the alerts from the predective model and classificate on a triage
- Pass the classfication to the Contextual model.
- Comunicates to the sql base for the medical expedient and pass to the predictive 

We built the first monolithic app (Backend + Frontend) as a single docker container.
The backend uses the API to get the streaming data from the astronaut and pass it to
the ML predictive model, via API.

Then the backend listen for the alerts on the model side and when an alert gets through
the interface using defaults variables of clasification do the triage functions.

When the data gets triaged, we add the info to a JSON full context (Json response from
the predictive model + classfication from the backend) and that's the data that the second
model uses to decided the truth of the alert. This comunications parts from the API between
the clasificator code and the classification model.

Finally, the full pipeline transform the data for the frontend comunication.