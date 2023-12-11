#!/bin/bash
##############################

shopt -s xpg_echo

##############################
# SET DEFAULT VARIABLES
HOST=$HOSTNAME
SHORT_DATE=`date '+%Y-%m-%d'`
TIME=`date '+%H%M'`
SCRIPT_TYPE=`basename $0 | cut -d '.' -f1`
filenametime1=$(date +"%m%d%Y%H%M%S")
filenametime2=$(date +"%Y-%m-%d %H:%M:%S")

##############################
# SET VARIABLES
export PYTHON_SCRIPT_NAME=$(cat config.toml | grep 'py_script' | awk -F"=" '{print $2}' | tr -d '"')
export SCRIPTS_FOLDER=$(pwd)
export LOGDIR=$SCRIPTS_FOLDER/log
export SHELL_SCRIPT_NAME='run'
export LOG_FILE=${LOGDIR}/${SHELL_SCRIPT_NAME}_${filenametime1}.log

echo $SCRIPTS_FOLDER
echo $PYTHON_SCRIPT_NAME
echo $
#############################
# GO TO SCRIPT FOLDER AND RUN
cd ${SCRIPTS_FOLDER}

##############################
# SET LOG RULES
exec > >(tee ${LOG_FILE}) 2>&1
##############################
# RUN SCRIPT
source venv/bin/activate

echo "Start Python script"
python3 ${SCRIPTS_FOLDER}/${PYTHON_SCRIPT_NAME}

RC1=$?
if [ ${RC1 -ne 0 } ]; then
    echo "PYTHON RUNNING FAILED"
    echo "[ERROR:] RETURN CODE: ${RC1}"
    echo "[ERROR:] REFER TO THE LOG FOR THE REASON FOR THE FAILURE"
    exit 1
fi

echo "PROGRAM SUCCEEDED"
exit 0

deactivate