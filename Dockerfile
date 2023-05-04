FROM python:3-slim AS builder
ADD ./python/requirements.txt /app/python/requirements.txt
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN python -m pip install --upgrade pip
RUN pip install --target=/app -r ./python/requirements.txt

ADD . /app
# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian11
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/python/main.py"]
