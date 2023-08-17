FROM alpine AS mkvtoolnix

WORKDIR /repos

RUN apk update \
    && apk add gcc g++ linux-headers make cmake ruby-rake python3-dev autoconf automake libtool lld pkgconfig curl wget git docbook-xsl \
    && cd /repos \
    && git clone --depth 1 https://github.com/gcp/libogg.git \
    && cd libogg \
    && ./autogen.sh \
    && ./configure --enable-static=yes --enable-shared=no \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos \
    && git clone --depth 1 https://github.com/xiph/vorbis.git \
    && cd vorbis \
    && ./autogen.sh \
    && ./configure --enable-static=yes --enable-shared=no --enable-docs=no \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos \
    && git clone --depth 1 https://github.com/madler/zlib.git \
    && cd zlib \
    && ./configure --static \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos \
    && git clone --depth 1 https://github.com/tukaani-project/xz.git \
    && cd xz \
    && mkdir build && cd build \
    && cmake .. -DBUILD_SHARED_LIBS=OFF \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos \
    && git clone --depth 1 https://github.com/GNOME/libxml2.git \
    && cd libxml2 \
    && mkdir build && cd build \
    && cmake .. -DBUILD_SHARED_LIBS=OFF \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos \
    && git clone --depth 1 https://gitlab.gnome.org/GNOME/libxslt.git \
    && cd libxslt \
    && mkdir build && cd build \
    && cmake .. -DBUILD_SHARED_LIBS=OFF \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos \
    && git clone --depth 1 https://github.com/Matroska-Org/libebml.git \
    && cd libebml \
    && mkdir build && cd build \
    && cmake .. -DBUILD_SHARED_LIBS=OFF -DENABLE_WIN32_IO=OFF \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos \
    && git clone --depth 1 https://github.com/Matroska-Org/libmatroska.git \
    && cd libmatroska \
    && mkdir build && cd build \
    && cmake .. -DBUILD_SHARED_LIBS=OFF -DBUILD_EXAMPLES=OFF \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos \
    && git clone --depth 1 https://github.com/xiph/flac.git \
    && cd flac \
    && mkdir build && cd build \
    && cmake .. -DBUILD_SHARED_LIBS=OFF -DBUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF -DCBUILD_DOCS=OFF -DCBUILD_DOCS=OFF -DINSTALL_MANPAGES=OFF \
    && make -j$(($(nproc) + 3)) \
    && make install \ 
    && cd /repos \
    && wget https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.17.tar.gz && tar -xvf libiconv-1.17.tar.gz && rm -rf libiconv-1.17.tar.gz \
    && cd libiconv-1.17 \
    && ./configure --enable-static=yes --enable-shared=no --disable-nls \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos \
    && wget https://gmplib.org/download/gmp/gmp-6.3.0.tar.xz && tar -xvf gmp-6.3.0.tar.xz && rm -rf gmp-6.3.0.tar.xz \
    && cd gmp-6.3.0 \
    && ./configure --enable-shared=no --enable-static=yes \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos  \
    && wget https://download.qt.io/archive/qt/5.15/5.15.10/single/qt-everywhere-opensource-src-5.15.10.tar.xz \ 
    && tar -xvf qt-everywhere-opensource-src-5.15.10.tar.xz && rm -rf qt-everywhere-opensource-src-5.15.10.tar.xz \
    && cd qt-everywhere-src-5.15.10 \
    && ./configure --prefix=/usr/local -static -release -opensource -confirm-license -no-icu -no-pch -no-opengl -skip qtwebengine -nomake tests -nomake examples -DBUILD_SHARED_LIBS=OFF \
    && make -j$(($(nproc) + 3)) \
    && make install \
    && cd /repos \
    && wget https://boostorg.jfrog.io/artifactory/main/release/1.82.0/source/boost_1_82_0.tar.gz \
    && tar -xvf boost_1_82_0.tar.gz && rm -rf boost_1_82_0.tar.gz \
    && cd boost_1_82_0 \
    && ./bootstrap.sh --prefix=/usr/local --with-libraries=all \
    && ./b2 -j $(nproc) link=static install \
    && rm -rf /repos \
    && mkdir -p /repos \
    && cd /repos \
    && git clone --depth 1 https://gitlab.com/mbunkus/mkvtoolnix.git \
    && cd mkvtoolnix \
    && git submodule update --init --recursive \
    && ./autogen.sh \
    && ./configure --enable-qt6=no --enable-update-check=no --enable-static=yes --enable-static-qt=yes --enable-gui=no \
    && rake \
    && mv src/mkvextract / && mv src/mkvinfo / && mv src/mkvmerge / && mv src/mkvpropedit / \
    && rm -rf repos

FROM alpine AS subsync

WORKDIR /work/resources/tools
COPY --from=mkvtoolnix /mkvextract .
COPY --from=mkvtoolnix /mkvinfo .

WORKDIR /work
COPY make.sh .
COPY requirements.txt .

WORKDIR /work/src
COPY src/*.py .

WORKDIR /repos

RUN apk update \
    && apk add gcc g++ make python3-dev py3-pip git curl wget swig libffi-dev libdrm-dev openssl-dev \
    pulseaudio-dev alsa-lib-dev ffmpeg-dev libxcb-dev mesa-dev autoconf automake libtool bison unzip \
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
    && cd / && rm -rf /repos \
    && cd /work && chmod +x make.sh && ./make.sh \
    && mv /work/dist/main /engine \
    && rm -rf /work

FROM alpine

WORKDIR /app
COPY --from=subsync /engine .