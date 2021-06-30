FROM capturethesignal/gnuradio-mini:pybombs-3.7-py2
LABEL maintainer=federico@maggi.cc

ENV VOLUME=/root
ENV BOMB=/bomb

VOLUME ${VOLUME}
VOLUME ${BOMB}
WORKDIR /root
COPY ./ /root
COPY ./bomb /bomb
RUN chmod +x build-deps.sh ep.sh && \
    ./build-deps.sh

CMD [ "./ep.sh" ]
