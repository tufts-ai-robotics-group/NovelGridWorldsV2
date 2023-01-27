FROM ubuntu:20.04
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install python3 python3-pip -y
RUN apt-get install openjdk-8-jre ant -y

COPY ade ade
RUN apt-get install bison flex -y
RUN cd ade/com/action/planner/ffplanner/Metric-FF-v2.1 && make clean && make
RUN cd ade && ant

COPY NovelGridWorldsV2 NovelGridWorldsV2
COPY NovelGridWorldsV2/examples/docker/run_experiment.sh /
RUN pip3 install wheel
RUN cd NovelGridWorldsV2 && pip3 install .

COPY polycraft_tufts/rl_agent/rapid_learn_diarc rapid_learn_diarc
RUN rm -rf rapid_learn_diarc/policies/*.npz && rm -rf rapid_learn_diarc/policies/*.json
RUN cd rapid_learn_diarc && pip install -r requirements.txt

ENV SDL_VIDEODRIVER="dummy"
ENTRYPOINT [ "/run_experiment.sh" ]
