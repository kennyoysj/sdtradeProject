#!/bin/bash

port=5205
threadId=$(netstat -nlp | grep :$port | awk '{print $7}' | awk -F"/" '{ print $1 }');
threadId=${threadId%/*};
echo $threadId
if [ -n "$threadId" ]; then
    kill $threadId
    echo "关闭进程{$threadId}"
fi
source activate ai
nohup python -u ./appBackend.py > socket.log 2>&1 &
echo "启动服务"
