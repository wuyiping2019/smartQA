#!/bin/sh
nohup python server_ner.py >> server_ner_log.log 2>&1 &
nohup python server_sim.py 8081 >> server_sim_8081_log.log 2>&1 &
nohup python server_sim.py 8082 >> server_sim_8082_log.log 2>&1 &
nohup python server_sim.py 8083 >> server_sim_8083_log.log 2>&1 &
nohup python server_sim.py 8084 >> server_sim_8084_log.log 2>&1 &
nohup python server_query.py >> server_query_log.log 2>&1 &