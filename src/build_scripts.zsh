if [ "$1" = "build_client" ]; then
    cd client/
    zsh generate_proto.zsh
    cd ..
fi
if [ "$1" = "build_server" ]; then
    cd server/
    zsh generate_proto.zsh
    cd ..
fi
if [ "$1" = "build_all" ]; then
    cd client/
    zsh generate_proto.zsh
    cd ..
    cd server/
    zsh generate_proto.zsh
    cd ..
fi