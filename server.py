from kubernetes import client, config
from flask import Flask,request, jsonify
from os import path
import yaml, random, string, json
import sys
import json
import os


# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.BatchV1Api()
v1_c = client.CoreV1Api()
app = Flask(__name__)
# app.run(debug = True)

with open("free-resource-job.yaml", "r") as file:
    free_job = yaml.safe_load(file)

with open("paid-resource-job.yaml", "r") as file:
    paid_job = yaml.safe_load(file)
print("hi")
@app.route('/config', methods=['GET'])
def get_config():
    pods = []
    namespaces = v1_c.list_namespace().items
    for ns in namespaces:
        namespace = ns.metadata.name
        pod_list = v1_c.list_namespaced_pod(namespace=namespace).items
        for pod in pod_list:
            pod_info = {
                "node": pod.spec.node_name,
                "ip": pod.status.pod_ip,
                "namespace": namespace,
                "name": pod.metadata.name,
                "status": pod.status.phase
            }
            pods.append(pod_info)

    # your code here
    
    output = {"pods": pods}
    print(output)
    output = json.dumps(output)

    return output

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    # your code here

    #data = request.data.decode("utf-8")
    #dataset = json.loads(data)["dataset"]

    # Create a job with the feed-forward neural network within the free-service namespace
    os.environ["DATASET"] = "mnist"
    os.environ["TYPE"] = "ff"


    try:
        v1.create_namespaced_job("free-service", free_job)
        return "success", 200
    except Exception as e:
        return str(e), 500


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # Parse request body
    #data = request.data.decode("utf-8")
    #dataset = json.loads(data)["dataset"]

    # Create a job with the convolutional neural network within the default namespace
    os.environ["DATASET"] = "kmnist"
    os.environ["TYPE"] = "cnn"

    v1.create_namespaced_job("default", paid_job)
    return "success", 200


    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)

