# Infrastructure Engineer Coding Challenge - Solution

This is a solution of a coding challenge for a DevOps Infrastructure Engineer task I recently did.

## How the application works
This application uses a custom collector with a gauge type metric. All standard collectors are disabled for the sake of readability.
The application accepts environment variables, such as APP_PORT or DOCKERHUB_ORGANIZATION which defaults as following if not provided :
- APP_PORT = 2113
- DOCKERHUB_ORGANIZATION = camunda

For every request, the application will check the availability of hub.docker.com. If not accessible within 1s (timeout), it will repeat the test every 3s. If the URL is healthy, it will scrape the information and provide the output with the application name and the organization name as labels in the form as below :

```
# HELP docker_image_pulls The total number of Docker image pulls
# TYPE docker_image_pulls gauge
docker_image_pulls{image="camunda-bpm-platform",organization="camunda"} 6.2366922e+07
docker_image_pulls{image="zeebe",organization="camunda"} 7.772069e+06
docker_image_pulls{image="zeebe-operator",organization="camunda"} 304.0
docker_image_pulls{image="zeebe-simple-monitor",organization="camunda"} 256850.0
docker_image_pulls{image="operate",organization="camunda"} 3.286514e+06
docker_image_pulls{image="zeebe-http-worker",organization="camunda"} 67430.0
docker_image_pulls{image="zeeqs",organization="camunda"} 112448.0
docker_image_pulls{image="zeebe-script-worker",organization="camunda"} 2427.0
docker_image_pulls{image="zeebe-dmn-worker",organization="camunda"} 87.0
...
```


## How to use dockerized app

### Build docker image
While in the root directory of the project, run :

```docker build -t camunda_test:<tag> .```

Using tag is preferred, so you know what version you are going to run later.

### Run docker image
The following command will tun the container on the localhost port 80 :

```docker run -p 80:2113 -e DOCKERHUB_ORGANIZATION='mysql' camunda_test:1.0```

The DOCKERHUB_ORGANIZATION variable is optional and defaults to 'camunda' if not provided.

To access Prometheus metrics, you should navigate to http://localhost/metrics (if you left the port mapping as in the provided example).

## How to run the application in K8s

The ```k8s-resources/app.yml``` defines the Deployment and Service kinds for K8s use-case. By default, the environment variables are not provided, however you can pass them this way :
```
...
    spec:
      containers:
      - env:
        - name: APP_PORT
          value: "2113"
        - name: DOCKERHUB_ORGANIZATION
          value: "camunda"
...
```
To access it from your local environment, you might want to use kube-proxy : ```kubectl port-forward svc/camunda-app 2113:2113```.
Then you should navigate to http://localhost:2113/metrics 
(in case if you are using custom ports, the kube-proxy command and the URL should be adjusted accordingly).


