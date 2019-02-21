#!/bin/bash

if [ $1 == "pot" ];then
    pybabel extract -F ./stalls/babel.cfg -o ./stalls/messages.pot ./stalls
fi

if [ $1 == "init" ];then
    pybabel init -i ./stalls/messages.pot -d ./stalls/translations -l $2
fi

if [ $1 == "build" ];then
    pybabel compile -d ./stalls/translations
fi

if [ $1 == "update" ];then
    pybabel update -i ./stalls/messages.pot -d ./stalls/translations
fi
