#!/bin/sh

while getopts abc:d: opt
do 
    case $opt in
        a)  
            .venv/Scripts/python src/bot.py
            ;;
        b)
            python3 src/bot.py
            ;;
        c)
            nouhup python3 src/bot.py
            ;;
        d)
            scp -i "C:\\Users\\Ennui\\.ssh\\aws\\key.pem\\" -r ./$OPTARG ec2-35-76-110-141.ap-northeast-1.compute.amazonaws.com:/home/ubuntu/
            ;;
        *)
            echo "Usage: $0 [-a] [-b] [-c]" 1>&2
            exit 1
            ;;
    esac
done

exit 0
