# first stage
FROM python:3.10 
COPY test/requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

WORKDIR /code

COPY ./src .

# update PATH environment variable
ENV PATH=/root/.local:$PATH

CMD [ "pytest", "test/" ]