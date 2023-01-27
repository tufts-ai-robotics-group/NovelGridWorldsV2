#!/bin/bash
# runs multiple components at the same time.

RL="no_rl"
CONFIG_FILE="pre_novelty_diarc.json"
RUN_NAME="default"
EPISODES=50
NUM_RUNS=10


while [[ $# -gt 0 ]]; do
  case $1 in
    -c|--config-file)
      CONFIG_FILE="$2"
      shift # past argument
      shift # past value
      ;;
    -r|--run_name)
      RUN_NAME="$2"
      shift # past argument
      shift # past value
      ;;
    --episodes)
      EPISODES="$2"
      shift # past argument
      shift # past value
      ;;
    --num_runs)
      NUM_RUNS="$2"
      shift # past argument
      shift # past value
      ;;
    --rl|--rl_on)
      RL="rl"
      shift # past argument
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

ORIGINAL_DIR=$(pwd)

for i in $(seq 1 $NUM_RUNS); do
    echo "Starting run $i of $NUM_RUNS"
    cd $ORIGINAL_DIR/NovelGridWorldsV2/examples
    python3 polycraft.py $CONFIG_FILE --exp_name $RUN_NAME_$RL --episodes $EPISODES --num_runs $NUM_RUNS &
    NGW_CMD_PID=$!
    sleep 5

    RL_PID=0
    if [[ $RL == "rl" ]]; then
        cd $ORIGINAL_DIR/polycraft_tufts/rl_agent/rapid_learn_diarc
        python3 rapid_learn.py &
        RL_PID=$!
        
        cd $ORIGINAL_DIR/ade && sleep 5
        ant launch -Dmain=com.config.polycraft.PolycraftAgent -Dargs="-gameport 2346 -rl" &
        ADE_PID=$!
    else
        cd $ORIGINAL_DIR/ade && sleep 5
        ant launch -Dmain=com.config.polycraft.PolycraftAgent -Dargs="-gameport 2346" &
        ADE_PID=$!
    fi


    wait $NGW_CMD_PID
    kill -9 $ADE_PID
    if [[ $RL_PID != 0 ]] ; then kill -9 $RL_PID ; fi
    sleep 5
done
exit $?
