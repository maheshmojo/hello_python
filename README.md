Kubernetes Intergration:

kubectl create secret docker-registry dockerhub-secret \
>   --docker-username=maheshmojo \
>   --docker-password=<Token-API>


>> vi service-account.yaml 
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dockerhub-sa
  namespace: default  # Change this if you're using a different namespace
secrets:
  - name: dockerhub-secret

>> kubectl apply -f deployment.yaml
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
To convert the setup for using a Docker Hub service account into a Helm chart, you'll need to create a directory structure for the Helm chart and define templates for the Kubernetes resources. Here's how you can do it step by step.

Step 1: Create the Helm Chart Structure
Run the following command to create a new Helm chart:

bash
Copy code
helm create my-app-chart
This will create a directory named my-app-chart with the following structure:

perl
Copy code
my-app-chart/
├── charts/
├── templates/
│   ├── deployment.yaml
│   ├── serviceaccount.yaml
│   ├── secret.yaml
│   └── ...
├── values.yaml
└── Chart.yaml
Step 2: Define the Values in values.yaml
Edit the values.yaml file to include your Docker Hub credentials and other necessary configurations:

yaml
Copy code
image:
  repository: <your-dockerhub-username>/<your-image>
  tag: latest

dockerhub:
  username: <your-dockerhub-username>
  password: <your-access-token>
  email: <your-email>

serviceAccount:
  name: dockerhub-sa
Step 3: Create the Secret Template
Create a secret.yaml file in the templates directory to define the Docker registry secret:

templates/secret.yaml:

yaml
Copy code
apiVersion: v1
kind: Secret
metadata:
  name: dockerhub-secret
  annotations:
    kubernetes.io/dockerconfigjson: "true"
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: {{ .Values.dockerhub.username | b64enc }}:{{ .Values.dockerhub.password | b64enc }} | toJson | b64enc
Step 4: Create the Service Account Template
Create a serviceaccount.yaml file to define the service account:

templates/serviceaccount.yaml:

yaml
Copy code
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ .Values.serviceAccount.name }}
  namespace: {{ .Release.Namespace }}
secrets:
  - name: dockerhub-secret
Step 5: Create the Deployment Template
Edit the existing deployment.yaml file to use the service account and image configuration from the values.yaml:

templates/deployment.yaml:

yaml
Copy code
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      serviceAccountName: {{ .Values.serviceAccount.name }}
      containers:
      - name: my-container
        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
        ports:
        - containerPort: 5000
Step 6: Update the Chart.yaml
Edit the Chart.yaml file to define your chart’s metadata:

yaml
Copy code
apiVersion: v2
name: my-app-chart
description: A Helm chart for deploying a Flask app with Docker Hub authentication
version: 0.1.0
Step 7: Install the Helm Chart
Now that you have defined your Helm chart, you can install it:

bash
Copy code
helm install my-app my-app-chart --set dockerhub.username=<your-dockerhub-username> --set dockerhub.password=<your-access-token> --set dockerhub.email=<your-email>
Summary
You have created a Helm chart that defines a Kubernetes deployment, service account, and Docker registry secret. This chart allows you to deploy your application to a Kubernetes cluster while securely pulling images from Docker Hub using service account credentials.

Important Note
For security reasons, consider using Helm secrets or a more secure method to handle sensitive data such as passwords. Using plain text in the values.yaml is not recommended for production environments.
