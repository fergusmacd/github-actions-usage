FROM python:3-slim AS builder



# We are installing a dependency here directly into our app source dir


RUN adduser myuser
USER myuser
ADD . /app
#RUN chown -R myuser:myuser /app
WORKDIR /app
RUN python -m pip install --upgrade pip
#COPY --chown=myuser:myuser requirements.txt requirements.txt
#RUN pip install --user -r requirements.txt


RUN pip install --user -r ./python/requirements.txt

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian11
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
# strictly speaking not necessary but makes it easier if working out what is happening
# Useful when running locally
ENV INPUT_ORGANISATION=
ENV INPUT_GITHUBAPIKEY=
CMD ["/app/python/main.py"]
