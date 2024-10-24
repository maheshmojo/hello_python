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
