FROM python:3.12.7 AS base
WORKDIR /app/main
SHELL ["/bin/bash", "-c"]

# install deps
# FROM base AS deps
COPY ./requirements.txt .
RUN python3 -m venv ./.hp
RUN source ./.hp/bin/activate
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

FROM base AS runner
# EXPOSE 3001
RUN useradd app
RUN chown app /home/app 
USER app
RUN source ./.hp/bin/activate
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "80"]
