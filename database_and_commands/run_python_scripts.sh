#!/bin/bash

# Open each script in a new tab of xfce4-terminal
xfce4-terminal \
    --tab --title="DB Connect" -e "bash -c 'python3 db_connect.py; exec bash'" \
    --tab --title="Read from DB" -e "bash -c 'python3 read_from_db.py; exec bash'" \
    --tab --title="Light Command" -e "bash -c 'python3 read_light_send_command.py; exec bash'" \
    --tab --title="Store Light Data" -e "bash -c 'python3 recieve_and_store_light_data.py; exec bash'"

