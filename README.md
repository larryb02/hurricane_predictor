# hurricane_predictor

Determine the probability of a hurricane on a specific date, at a given location

# How it works
A user will select a location and a date. This input will get sent to NVIDIA StormCast in order to create a prediction on certain weather conditions in that area on that day. This data will get sent to an LLM to determine a probability of a storm occurring on that day.
# Structure

## Client Side
Simple web server powered by nextjs. This is what the user will interact with to get predictions.
## Server Side
API to facilitate interactions with StormCast model
# Tools
NVIDIA StormCast - Pretrained Model <br>
Nextjs <br>
FastAPI <br>
OpenAI
