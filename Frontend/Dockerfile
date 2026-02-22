FROM ubuntu:22.04

# Ostavljamo prazno, Docker će koristiti tvoju kućnu mrežu automatski

# 1. Instalacija zavisnosti
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    libjpeg-dev \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# 2. Kloniranje i build
RUN git clone https://github.com/jacksonliam/mjpg-streamer.git /tmp/mjpg-streamer
WORKDIR /tmp/mjpg-streamer/mjpg-streamer-experimental
RUN make && make install

EXPOSE 8080

ENTRYPOINT ["mjpg_streamer"]
CMD ["-i", "input_uvc.so", "-o", "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www"]