FROM ubuntu:20.04
# Install git
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Kyiv
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        git \
        python3 \
        python3-pip \
        python3-dev \
        libxml2-dev \
        libxslt1-dev && \
    apt-get autoremove -y && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/hostjbm/FM_playlists.git
RUN pip3 install lxml
WORKDIR /FM_playlists/
RUN mkdir Playlists
CMD bash start_cron.sh && mv Week_* Playlists

# docker build -t fm:0.1 .
# docker run -it --rm -v $PWD:/FM_playlists/Playlists fm:0.1


