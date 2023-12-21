# distributed_cloud

Distributed_Cloud is a transportable server system which aims to provide file sharing
and distributed computing to a personal environment.

<h1> Build </h1>
To build, from the github /src directory, 
<h3>Generating all RPC build files</h3>
`./build_scripts build_all`

<h3>Generating client build files</h3>
`./build_scripts build_client`

<h3>Generating server build files</h3>
`./build_scripts build_server`

<h1>Run</h1>
<h3>Running the server</h3>
python3 src/server/src/main.py

<h3>Running the client</h3>
python3 src/client/src/main.py
