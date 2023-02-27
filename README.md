This is a project implemented in the tutorial from freecodecamp. You can find the video link below,
* [video link](https://www.youtube.com/watch?v=hmkF77F9TLw)


Before building the docker images, please run the following commands on k8s.
* eval $(minikube docker-env)
* docker build --no-cache . --tag <service_name>:latest
* minikube start
* minikube tunnel
