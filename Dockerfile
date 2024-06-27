FROM alpine

WORKDIR /repos
RUN apk update \
    && apk add gcc g++ make cmake python3-dev py3-pip git curl wget swig libffi-dev libdrm-dev openssl-dev \
    pulseaudio-dev alsa-lib-dev ffmpeg-dev libxcb-dev mesa-dev autoconf automake libtool bison unzip \
    && pip install pybind11[global] \
    && mkdir -p /repos \
    && cd /repos \
    && git clone --depth 1 https://github.com/cmusphinx/sphinxbase.git \
    && cd sphinxbase \
    && ./autogen.sh \
    && make -j$(nproc) \
    && make install \
    && cd /repos \
    && git clone --depth 1 --branch last-pre-1.0 https://github.com/cmusphinx/pocketsphinx.git \
    && cd pocketsphinx \
    && ./autogen.sh \
    && make -j$(nproc) \
    && make install \
    && cd /repos \
    && git clone --depth 1 https://github.com/sc0ty/subsync.git \
    && cd subsync \
    && cp subsync/config.py.template subsync/config.py \
    && export CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
    && pip install --no-binary :all: "cryptography<3.5" \
    && pip install . \
    && mkdir -p /work/resources/libs \
    && ldd build/lib*cpython*/gizmo*.so | grep -o '/[^ ]*' | xargs -I '{}' cp -n '{}' /work/resources/libs \
    && rm -rf /work/resources/libs/ld*.so* \
    && cp subsync/key.pub /work/resources/ \
    && git clone https://github.com/ztancankiri/subtitle-extractor.git \
    && cd subtitle-extractor \
    && mkdir build && cd build \
    && cmake .. \
    && make -j$(nproc) \
    && make install \
    && ldd subextractor.*.so | grep -o '/[^ ]*' | xargs -I '{}' cp -n '{}' /work/resources/libs \
    && rm -rf /work/resources/libs/ld*.so* \ 
    && cd / && rm -rf /repos

WORKDIR /work

# COPY make.sh .
# COPY engine.spec .
# COPY requirements.txt .
# COPY src/*.py src/
# RUN chmod +x make.sh && ./make.sh && mv /work/dist/main /engine && rm -rf /work

# FROM alpine

# WORKDIR /app
# COPY --from=subsync /engine .