FROM ghcr.io/graalvm/graalvm-ce:java17-21.3.0 as sigbuilder
ENV GRAALVM_HOME=/opt/graalvm-ce-java17-21.3.0/ 
SHELL ["/usr/bin/bash", "-c"]
WORKDIR /app
RUN microdnf install -y git zlib-devel && rm -rf /var/cache/yum
RUN gu install native-image
RUN git clone --branch upstream https://github.com/forestcontact/signal-cli
WORKDIR /app/signal-cli
RUN git pull origin forest-v2.10.5
RUN git log -1 --pretty=%B | tee commit-msg
RUN ./gradlew nativeCompile

FROM ubuntu:hirsute as libbuilder
WORKDIR /app
RUN ln --symbolic --force --no-dereference /usr/share/zoneinfo/EST && echo "EST" > /etc/timezone
RUN apt update
RUN DEBIAN_FRONTEND="noninteractive" apt install -yy python3.9 python3.9-venv pipenv
RUN python3.9 -m venv /app/venv
COPY Pipfile.lock Pipfile /app/
RUN VIRTUAL_ENV=/app/venv pipenv install 

FROM ubuntu:hirsute
WORKDIR /app
RUN mkdir -p /app/data
RUN apt-get update
RUN apt-get install -y python3.9 wget libfuse2 kmod
RUN apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/
COPY --from=sigbuilder /app/signal-cli/build/native/nativeCompile/signal-cli /app/signal-cli/commit-msg /app/signal-cli/build.gradle.kts  /app/
# for signal-cli's unpacking of native deps
COPY --from=sigbuilder /lib64/libz.so.1 /lib64
COPY --from=libbuilder /app/venv/lib/python3.9/site-packages /app/
COPY ./mc_util/ /app/mc_util/
COPY ./forest/ /app/forest/
COPY ./signle.py /app/ 
ENTRYPOINT ["/usr/bin/python3.9", "/app/signle.py"]
