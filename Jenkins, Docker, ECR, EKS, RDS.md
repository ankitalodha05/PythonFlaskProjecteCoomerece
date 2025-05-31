

---

# 📘 **End-to-End CI/CD Pipeline for Flask App on AWS using Jenkins, Docker, ECR, EKS, RDS**

---

## 🧱 **Architecture Overview**

* **Flask App** hosted in **Amazon EKS**
* **MySQL (RDS)** as the database
* Dockerized and pushed to **Amazon ECR**
* CI/CD pipeline using **Jenkins**
* Deployment via `kubectl` using `deployment.yaml`

---

## 🔧 Prerequisites

1. ✅ Jenkins Master + Agent (slave) setup
2. ✅ Jenkins slave node with:

   * Docker installed
   * AWS CLI installed
   * IAM permissions for ECR and EKS
3. ✅ Flask application in a GitHub repository
4. ✅ EKS Cluster created (`naresh` in our example)
5. ✅ RDS MySQL database created
6. ✅ ECR repository created (`flask-ecommerce`)

---

## 🛠 Step-by-Step Instructions

---

### ✅ 1. **Install & Configure Jenkins Agent (slave2)**

On `slave2`:

```bash
sudo yum update -y  # or apt update for Ubuntu
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker

sudo usermod -aG docker ubuntu
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock
```

> Reboot or restart Jenkins agent to apply group changes.

---

### ✅ 2. **Create ECR Repo**

```bash
aws ecr create-repository --repository-name flask-ecommerce --region ap-south-1
```

---

### ✅ 3. **Prepare `deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
  labels:
    app: flask-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-container
          image: 160885291806.dkr.ecr.ap-south-1.amazonaws.com/flask-ecommerce:latest
          ports:
            - containerPort: 5000
          env:
            - name: DB_HOST
              value: "your-rds-endpoint"
            - name: DB_USER
              value: "admin"
            - name: DB_PASSWORD
              value: "adminadmin"
            - name: DB_NAME
              value: "my_product"
```

> Save this as `deployment.yaml` in your Flask project repo.

Also create a `service.yaml` if you want to expose the service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  type: LoadBalancer
  selector:
    app: flask-app
  ports:
    - port: 80
      targetPort: 5000
```

---

### ✅ 4. **Jenkins Pipeline Script**

Create a **pipeline job** in Jenkins and use this script:

```groovy
pipeline {
    agent none

    environment {
        ECR_URI = '160885291806.dkr.ecr.ap-south-1.amazonaws.com/flask-ecommerce'
        IMAGE_TAG = 'latest'
        CLUSTER_NAME = 'naresh'
        REGION = 'ap-south-1'
    }

    stages {
        stage('Git Clone') {
            agent { label 'slave2' }
            steps {
                dir('flask_ecommerce_app_Dynamic') {
                    git branch: 'main', url: 'https://github.com/ankitalodha05/PythonFlaskProjecteCoomerece.git'
                }
            }
        }

        stage('Docker Build & Push') {
            agent { label 'slave2' }
            steps {
                dir('flask_ecommerce_app_Dynamic/flask_ecommerce_app_Dynamic') {
                    script {
                        sh '''
                            echo "Login to ECR..."
                            aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_URI

                            echo "Build Docker image..."
                            docker build -t flask-ecommerce .

                            echo "Tag image for ECR..."
                            docker tag flask-ecommerce:$IMAGE_TAG $ECR_URI:$IMAGE_TAG

                            echo "Push image to ECR..."
                            docker push $ECR_URI:$IMAGE_TAG
                        '''
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            agent { label 'slave2' }
            steps {
                dir('flask_ecommerce_app_Dynamic/flask_ecommerce_app_Dynamic') {
                    script {
                        sh '''
                            echo "Update kubeconfig for EKS..."
                            aws eks update-kubeconfig --name $CLUSTER_NAME --region $REGION

                            echo "Deploying to EKS..."
                            kubectl apply -f deployment.yaml
                            kubectl apply -f service.yaml
                        '''
                    }
                }
            }
        }
    }
}
```

---

### ✅ 5. **IAM Permissions for Jenkins Node**

Attach a role to the `slave2` EC2 instance (or use IAM credentials) with these policies:

* `AmazonEC2ContainerRegistryFullAccess`
* `AmazonEKSClusterPolicy`
* `AmazonEKSWorkerNodePolicy`
* `AmazonEKS_CNI_Policy`

---

### ✅ 6. **Run the Jenkins Job**

* Jenkins will:

  * Clone your repo
  * Build and push Docker image to ECR
  * Deploy to EKS using `kubectl`

---

## 📊 Example Outputs

* ECR push: `Pushed flask-ecommerce:latest`
* EKS: `deployment.apps/flask-app created`
* Load Balancer URL from `kubectl get svc`

---

## 🔐 Security Tips

* Use AWS Secrets Manager for DB credentials instead of plaintext.
* Use a private ECR repo.
* Configure RBAC on EKS.

---

Let me know if you'd like this exported as a PDF or formatted into a Markdown `.md` or `.docx` file.
