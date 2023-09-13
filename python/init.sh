docker build -t  my-chat-app . -f bonus.dockerfile 
docker run -p 5000:5000 --cpus "2.0" --memory "1g" my-chat-app
