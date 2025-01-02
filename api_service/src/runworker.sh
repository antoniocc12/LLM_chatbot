#!/bin/bash

APP_NAME=""
JOB_TYPE=""
LOG_LEVEL="INFO"
CONCURRENCY=1
VALIDATION="false"

function validate_job_type() {
    case "${JOB_TYPE}" in
        process_dataset);;
        "")
            echo "Job type(-j) argument is required."
            exit_with_usage_info;;
        *)
            echo "Invalid value for JOB_TYPE: ${JOB_TYPE}."
            exit_with_usage_info;;
    esac
}

function validate_log_level() {
    case "${LOG_LEVEL}" in
        DEBUG);;
        INFO);;
        WARNING);;
        ERROR);;
        CRITICAL);;
        *)
            echo "Invalid value for LOG_LEVEL: ${LOG_LEVEL}."
            exit_with_usage_info;;
    esac
}

function set_app_name() {
    if [ "${JOB_TYPE}" == "process_dataset" ];
        then
            APP_NAME="jobs.process_dataset.process_dataset.celery"
    fi
}

function exit_with_usage_info {
    echo "Usage: $0 -j <process_dataset> [-l <DEBUG|INFO|WARNING|ERROR|CRITICAL>] [-c <type:int>]"
    echo "		-j : Job type of the worker. Options are <training|eda|dataset-upload>. This filed is mandatory."
    echo "		-l : Log level of worker. Options are <DEBUG|INFO|WARNING|ERROR|CRITICAL>. This value is optional. Default: INFO."
    echo "		-c : Concurrency. Value should be an integer number. This value is optional. Default: 1."

    exit 0;
}

while getopts j:l:c: flag;
    do
        case "${flag}" in
            j) JOB_TYPE=${OPTARG};;
            l) LOG_LEVEL=${OPTARG};;
            c) CONCURRENCY=${OPTARG};;
            *) exit_with_usage_info;;
        esac
    done

validate_job_type
validate_log_level
set_app_name

echo "Running celery job..."
echo "    Worker: ${JOB_TYPE}_worker@%h"
echo "    LogLevel: ${LOG_LEVEL}"
echo "    Queue: ${JOB_TYPE}_queue"
echo "    Concurrency: ${CONCURRENCY}"
celery -A ${APP_NAME} worker -n "${JOB_TYPE}_worker@%h" --loglevel="${LOG_LEVEL}" -Q "${JOB_TYPE}_queue" --concurrency="${CONCURRENCY}"
