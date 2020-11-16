FROM circleci/python:3.6.8

COPY webapp/requirements*.txt /opt/bh/webapp/

WORKDIR /opt/bh

ARG GIT_TOKEN
ARG PIP_REQUIREMENTS

# install Python modules needed by the Python app
RUN sudo pip install --upgrade pip
RUN pip install --no-warn-script-location -r /opt/bh/webapp/$PIP_REQUIREMENTS --user

COPY . /opt/bh/

# install node (for tests)
RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo bash
# and install node
RUN sudo apt-get install nodejs
# confirm that it was successful
RUN node -v
# npm installs automatically
RUN npm -v

# Install FE dependencies
WORKDIR /opt/bh/frontend
USER root
RUN npm install
RUN npm install gulp

# tell the port number the container should expose
EXPOSE 8200

# finish up
USER circleci
WORKDIR /opt/bh
ENV PYTHONPATH=$PYTHONPATH:/opt/bh/webapp/src/
