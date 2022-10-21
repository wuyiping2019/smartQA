#!/bin/sh

ps -ef | grep server_sim | grep -v grep | cut -c 9-15 | xargs kill -9
ps -ef | grep server_ner | grep -v grep | cut -c 9-15 | xargs kill -9
ps -ef | grep server_query | grep -v grep | cut -c 9-15 | xargs kill -9