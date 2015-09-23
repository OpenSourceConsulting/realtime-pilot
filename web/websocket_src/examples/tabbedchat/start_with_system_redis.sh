#!/bin/sh


# Setting up signal handlers
# All this code is needed to do not leave dangling children
killchildren() {
    if [ "x$(jobs)" == "x" ]; then
        exit 0
    fi
    trap killchildren 0 1 2 3 15
    kill $(jobs -p) 2> /dev/null
}
trap killchildren 0 1 2 3 15

mkdir ./run 2> /dev/null

zerogw -c zerogw.yaml &
python3 -m tabbedchat \
    --auth-connect "ipc://./run/auth.sock" \
    --chat-connect "ipc://./run/chat.sock" \
    --output-connect "ipc://./run/output.sock" \
    --log-file "./run/python.log" \
    &

echo "========================================================================"
echo "You can now browse:"
echo "    http://localhost:8000/"
echo "(although it can take few seconds to start up redis and python)"
echo "NOTE: we have put all the sockets and logs in ./run dir"
echo "WARNING: this script clobbers system redis with it's own data"
echo "========================================================================"

while ! wait; do true; done;
