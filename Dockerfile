# Use phusion/baseimage as base image. To make your builds reproducible, make
# sure you lock down to a specific version, not to `latest`!
# See https://github.com/phusion/baseimage-docker/blob/master/Changelog.md for
# a list of version numbers.
FROM phusion/baseimage:0.9.22

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

RUN apt-get update
RUN apt-get -y install python3-pip

RUN pip3 install --upgrade pip
ADD ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY . /usr/local/automation_tests
WORKDIR /usr/local/automation_tests
ENV PATH="/usr/local/automation_tests:${PATH}"
ENV PYTHONPATH="/usr/local/automation_tests:${PYTHONPATH}"

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
