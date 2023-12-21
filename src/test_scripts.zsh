if [[ $input == "test" ]]; then
    screen -dmS server # to create a screen
    screen -r server
    python3 server/src/main.py # to run the server
    # python3 server/src/main.py # to run the server
    ctrl+a+d # to detach from the screen
    python3 client/src/main.py # to run the client
    screen -r server # to reattach to the screen
    ctrl+c # to stop the server
    ctrl+d # to exit the screen
fi