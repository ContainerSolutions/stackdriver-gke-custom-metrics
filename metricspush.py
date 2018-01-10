from google.cloud import monitoring
from kubernetes import client, config
import requests
import os
import time


metadata_header = {'Metadata-Flavor': 'Google'}


def instance_id():
    # Get the instance_id from the GCP metadata API
    r = requests.get("http://metadata.google.internal./computeMetadata/v1/instance/id", headers=metadata_header)
    return r.text


def zone():
    # Get the zone from the GCP metadata API
    r = requests.get("http://metadata.google.internal./computeMetadata/v1/instance/zone", headers=metadata_header)
    parts = r.text.split('/')
    return parts[len(parts) - 1]


def cluster_name():
    # Get the cluster name from an environment variable. This will be set from the ConfigMap cluster-metadata (see: clustermetadata.yaml)
    # This is just a custom solution, as there is no API to determine this value from a running Pod.
    return os.environ['CLUSTER_NAME'] # cannot be determined from metadata


def container_name():
    # The container name is passed in from the yaml file as an environment variable.
    return os.environ['CONTAINER_NAME'] # cannot be determined from metadata (HOSTNAME is Pod ID)


def namespace_id():
    # Get namespace_id from the Kubernetes API server. The Pod has to have the proper permissions to access this information
    # if you have enabled RBAC on your cluster.
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    return v1.list_namespace().items[0].metadata.uid


def pod_uid():
    # The UID of the Pod is passed in as an environment variable using the Kubernetes Downward API (see: metricspod.yaml)
    return os.environ['POD_UID']


print("instance_id:", instance_id())
print("zone: ", zone())
print("namespace_id:", namespace_id())
print("pod_uid:", pod_uid())
print("container_name:", container_name())
print("cluster_name:", cluster_name())

sdclient = monitoring.Client()
resource = sdclient.resource(
    'gke_container',
    labels={
        'cluster_name': cluster_name(),
        'container_name': container_name(),
        'instance_id': instance_id(),
        'namespace_id': namespace_id(),
        'pod_id': pod_uid(),
        'zone': zone(),
    }
)

metric = sdclient.metric(
    type_='custom.googleapis.com/my_container_metric',
    labels={
    }
)

while True:
    print("pushing metric")
    sdclient.write_point(metric, resource, 3.14)
    time.sleep(60)