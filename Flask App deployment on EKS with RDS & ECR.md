Here is a **complete, well-structured document** for your setup workflow. It includes explanations and all required commands for setting up an EC2 instance, EKS cluster, RDS, Docker, Git, Flask app deployment, and Kubernetes integration.

---

# 🚀 Full Deployment Guide: Flask App on EKS with RDS & ECR

## ✅ Prerequisites

* AWS CLI configured with permissions to create EKS, EC2, RDS, and ECR resources
* IAM role with the necessary permissions (EC2InstanceProfile, EKS permissions, AmazonRDSFullAccess, etc.)
* AWS region used: `ap-south-1`

---

## 📘 Step 1: Create RDS Database (MySQL)

### 1.1. Create RDS Instance

You can create it from the AWS Console or CLI. Choose:

* Engine: MySQL
* DB Name: `my_product`
* Master Username: `admin`
* Master Password: `adminadmin`
* Public Access: **Yes** (for testing; **No** in production)
* Security Group: Add inbound rule for port `3306` from your EC2 IP

### 1.2. Open MySQL Workbench

* Create a new connection using your RDS endpoint, username, and password.
* Open the connection.

### 1.3. Create Database and Table

Use the following SQL script to initialize the database and insert a sample product:

```sql
CREATE DATABASE my_product;
USE my_product;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(255)
);

INSERT INTO products (name, description, price, image_url)
VALUES (
    'Example Product',
    'This is a sample description for the example product.',
    49.99,
    'https://img.autocarindia.com/Features/Hycross%20feature.jpg?w=700&c=1'
);
```

---

## 💥 Step 2: Prepare EC2 Linux Server

### 2.1. Launch EC2 Instance

* Choose Amazon Linux 2 or Ubuntu.
* Attach IAM role with the following permissions:

  * `AmazonEC2ContainerRegistryFullAccess`
  * `AmazonEKSWorkerNodePolicy`
  * `AmazonRDSFullAccess`

### 2.2. Install Docker

```bash
sudo yum update -y   # For Amazon Linux
sudo yum install docker -y
sudo service docker start
sudo usermod -aG docker ec2-user
sudo chmod 666 /var/run/docker.sock
```

Or for Ubuntu:

```bash
sudo apt update -y
sudo apt install docker.io -y
sudo usermod -aG docker ubuntu
sudo chmod 666 /var/run/docker.sock
```

Logout and log back in, or use `newgrp docker` to apply group changes.

### 2.3. Install Git

```bash
sudo yum install git -y  # Amazon Linux
# or
sudo apt install git -y  # Ubuntu
```

### 2.4. Install kubectl

```bash
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin
kubectl version --short --client
```

### 2.5. Install eksctl

```bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

---

## ☨️ Step 3: Create EKS Cluster

```bash
eksctl create cluster --name naresh \
  --region ap-south-1 \
  --node-type t2.small \
  --nodes 2 \
  --managed
```

> This may take 10–15 minutes to provision the control plane and nodes.

---

## 🐙 Step 4: Clone Flask App Repository

```bash
git clone https://github.com/ashrafgate/PythonFlaskProjecteCoomerece.git
cd PythonFlaskProjecteCoomerece/flask_ecommerce_app_Dynamic
```

---

## ✏️ Step 5: Update Flask App and Kubernetes Files

### 5.1. Modify `app.py`

Update the database connection logic using environment variables:

```python
DB_HOST = os.environ.get("DB_HOST", "your-rds-endpoint")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "adminadmin")
DB_NAME = os.environ.get("DB_NAME", "my_product")
```

### 5.2. Modify `deployment.yaml`

Update the image URI and environment variables:

```yaml
containers:
  - name: flask-container
    image: <account_id>.dkr.ecr.ap-south-1.amazonaws.com/flask-ecommerce:latest
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

---

## 🐳 Step 6: Create ECR Repository and Push Docker Image

### 6.1. Create ECR Repository

```bash
aws ecr create-repository --repository-name flask-ecommerce
```

### 6.2. Build and Push Docker Image

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin <account_id>.dkr.ecr.ap-south-1.amazonaws.com

docker build -t flask-ecommerce .
docker tag flask-ecommerce:latest <account_id>.dkr.ecr.ap-south-1.amazonaws.com/flask-ecommerce:latest
docker push <account_id>.dkr.ecr.ap-south-1.amazonaws.com/flask-ecommerce:latest
```

---

## 📦 Step 7: Deploy Application to EKS

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### Check Kubernetes Resources

```bash
kubectl get nodes
kubectl get pods
kubectl get deployments
kubectl get services
```

---

## 🌐 Step 8: Access the Application

```bash
kubectl get svc
```

* Copy the `EXTERNAL-IP` of the LoadBalancer service
* Paste it into your browser to access the Flask web application

---

## 🧹 Optional: Cleanup Resources

```bash
kubectl delete service <service-name>
kubectl delete deployment <deployment-name>
```

---

## ✅ Summary of Tools Used

| Tool        | Purpose                               |
| ----------- | ------------------------------------- |
| **Docker**  | Containerizing Flask app              |
| **Git**     | Cloning project repository            |
| **kubectl** | Managing Kubernetes resources         |
| **eksctl**  | Creating and managing EKS clusters    |
| **ECR**     | Hosting and pulling container images  |
| **RDS**     | Backend MySQL database                |
| **EKS**     | Hosting scalable Kubernetes workloads |

---
