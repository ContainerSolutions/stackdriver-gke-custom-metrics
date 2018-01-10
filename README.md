# stackdriver-gke-custom-metrics

This example how to push custom metrics from a container running on GKE (Google Kubernetes Engine) to Google Stackdriver. It's an extension for this post on the Container Solutions blog: https://container-solutions.com/monitoring-containers-on-gke-with-google-stackdriver

To push metrics related to a container to the Stackdriver API you have to set the metrics type to `gke_container` and set a bunch of labels so Stackdriver can link the metric to the container correctly. Look at the Python code and the yaml files to see some working code how to get this done. If you just want to run the the container on your cluster follow the instructions below. The container is already built by Docker Hub: https://hub.docker.com/r/containersol/stackdriver-gke-custom-metrics/

1. Go to your Google Cloud console and open Monitoring. If it asks you to enable monitoring for your project say yes. This will enable the Monitoring API.
2. Edit clustermetadata.yaml and set the cluster name to whatever your cluster is named in Google Cloud.
3. Apply the edited clustermetadata.yaml: `kubectl apply -f clustermetadata.yaml`
4. Apply metricspod.yaml to start the pud: `kubectl apply -f metricspod.yaml`
5. Go to the Metrics Explorer in Stackdriver Monitoring and look for the metric `my_container_metric`. After a few minutes of the container running on the cluster the metric should show up.

