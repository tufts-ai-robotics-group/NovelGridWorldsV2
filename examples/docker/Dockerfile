FROM ubuntu:20.04
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install --no-install-recommends \
            python3 python3-pip \
            openjdk-8-jdk-headless ant openjdk-11-jre-headless- \
            gcc libc6-dev make wget bison flex -y && \
    rm -rf /var/lib/apt/lists/*

COPY ade ade
RUN cd ade/com/action/planner/ffplanner && \
    wget https://fai.cs.uni-saarland.de/hoffmann/ff/Metric-FF-v2.1.tgz && \
    tar -xvzf Metric-FF-v2.1.tgz && \
    cd Metric-FF-v2.1 && \
    make clean && make && \
    apt-get autoremove wget gcc make -y
RUN cd ade && ant clean && ant

COPY NovelGridWorldsV2 NovelGridWorldsV2
COPY NovelGridWorldsV2/examples/docker/run_experiment.sh /
RUN cd NovelGridWorldsV2 && pip3 install .

COPY polycraft_tufts/rl_agent/rapid_learn_diarc rapid_learn_diarc
RUN rm -rf rapid_learn_diarc/policies/*.npz && rm -rf rapid_learn_diarc/policies/*.json
RUN cd rapid_learn_diarc && pip3 install -r requirements.txt

ENV SDL_VIDEODRIVER="dummy"
ENTRYPOINT [ "/run_experiment.sh" ]
