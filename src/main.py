import os
import json
import time
import urllib.request
import prometheus_client
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server

def test_url(url):
    try:
        urllib.request.urlopen(url, timeout=1)
    except urllib.error.HTTPError as e:
        print('Dockerhub endpoint is not reachable.')
        time.sleep(3)
        test_url(url)
    except urllib.error.URLError as e:
        print('Dockerhub endpoint is not reachable.')
        time.sleep(3)
        test_url(url)
    print('URL is OK.')

def main():
    organization = os.getenv('DOCKERHUB_ORGANIZATION', default='camunda').lower()
    port = int(os.getenv('APP_PORT', default=2113))



    class RandomNumberCollector(object):
        def __init__(self):
            pass

        def collect(self):
            dockerhub_url = 'https://hub.docker.com/v2/repositories/' + organization + '/?page_size=25&page=1'
            test_url(dockerhub_url)
            with urllib.request.urlopen(dockerhub_url) as url:
                data = json.load(url)
            img_list = data["results"]
            keys = ['name', 'pull_count']
            gauge = GaugeMetricFamily("docker_image_pulls", "The total number of Docker image pulls",
                                      labels=["image", "organization"])
            for i in range(0, len(img_list)):
                img_d = img_list[i]
                values = [img_d[key] for key in keys]
                gauge.add_metric([values[0], organization], values[1])
            yield gauge

    start_http_server(port)
    prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
    prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
    prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)
    REGISTRY.register(RandomNumberCollector())

    while True:
        time.sleep(5)


if __name__ == '__main__':
    main()

