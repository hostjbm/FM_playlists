FROM ubuntu:18.04
# Install git
RUN apt-get update && apt-get install -y \
git \
python3 \
python3-pip \
python3-dev \
libxml2-dev \
libxslt1-dev
RUN git clone https://github.com/hostjbm/FM_playlists.git
RUN pip3 install lxml
WORKDIR /FM_playlists/
RUN mkdir Playlists
CMD bash start_cron.sh && mv Week_* Playlists

# docker build -t fm:0.1 .
# docker run -it --rm -v $PWD:/FM_playlists/Playlists fm:0.1
