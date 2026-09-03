# Docker Homework

## Task: Hello World Applications

For this task, I created and ran six simple Hello World web applications using Docker.

The applications are:

- Node.js
- Python
- Java
- Apache
- React
- Nginx

Each application has its own folder and Dockerfile.

---

## 1. Node.js Application

Folder:

```text
nodejs-app/
```

The Node.js application uses a simple HTTP server and displays:

```text
Hello World from Node.js!
```

### Dockerfile

```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY package.json .
COPY app.js .

EXPOSE 3000

CMD ["npm", "start"]
```

### Build and Run

```bash
docker build -t nodejs-app .
docker run -d -p 3000:3000 --name nodejs-container nodejs-app
```

### Verification

The application was opened in the browser at:

```text
http://localhost:3000
```

The Hello World message was displayed successfully.

---

## 2. Python Application

Folder:

```text
python-app/
```

The Python application uses Python's built-in HTTP server and displays:

```text
Hello World from Python!
```

### Dockerfile

```dockerfile
FROM python:3.12-alpine

WORKDIR /app

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
```

### Build and Run

```bash
docker build -t python-app .
docker run -d -p 8000:8000 --name python-container python-app
```

### Verification

The application was opened in the browser at:

```text
http://localhost:8000
```

The Hello World message was displayed successfully.

---

## 3. Java Application

Folder:

```text
java-app/
```

The Java application uses a simple HTTP server and displays:

```text
Hello World from Java!
```

### Dockerfile

```dockerfile
FROM eclipse-temurin:21-jdk-alpine

WORKDIR /app

COPY HelloWorld.java .

RUN javac HelloWorld.java

EXPOSE 8080

CMD ["java", "HelloWorld"]
```

### Build and Run

```bash
docker build -t java-app .
docker run -d -p 8080:8080 --name java-container java-app
```

### Verification

The application was opened in the browser at:

```text
http://localhost:8080
```

The Hello World message was displayed successfully.

---

## 4. Apache Web Server

Folder:

```text
Apache-app/
```

For this application, I used Apache HTTP Server to serve a simple HTML page.

The page displays:

```text
Hello World from Apache!
```

### Dockerfile

```dockerfile
FROM httpd:2.4-alpine

COPY index.html /usr/local/apache2/htdocs/

EXPOSE 80
```

### Build and Run

```bash
docker build -t apache-app .
docker run -d -p 8081:80 --name apache-container apache-app
```

### Verification

The application was opened in the browser at:

```text
http://localhost:8081
```

The Hello World message was displayed successfully.

---

## 5. React Application

Folder:

```text
React-app/
```

I created a basic React application using Vite. The application displays:

```text
Hello World from React!
```

For Docker, the React application is built using Node.js and the generated files are served using Nginx.

### Dockerfile

```dockerfile
FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
```

### Build and Run

```bash
docker build -t react-app .
docker run -d -p 8082:80 --name react-container react-app
```

### Verification

The application was opened in the browser at:

```text
http://localhost:8082
```

The Hello World message was displayed successfully.

---

## 6. Nginx Application

Folder:

```text
nginx-app/
```

For this application, I used Nginx to serve a simple HTML page.

The page displays:

```text
Hello World from Nginx!
```

### Dockerfile

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

### Build and Run

```bash
docker build -t nginx-app .
docker run -d -p 8083:80 --name nginx-container nginx-app
```

### Verification

The application was opened in the browser at:

```text
http://localhost:8083
```

The Hello World message was displayed successfully.

---

## Docker Containers Verification

After running all the applications, I checked the running containers using:

```bash
docker ps
```

All six containers were running successfully.

| Application | Container | Port |
|---|---|---:|
| Node.js | `nodejs-container` | 3000 |
| Python | `python-container` | 8000 |
| Java | `java-container` | 8080 |
| Apache | `apache-container` | 8081 |
| React | `react-container` | 8082 |
| Nginx | `nginx-container` | 8083 |

## Folder Structure

```text
devOps/
├── Apache-app/
├── React-app/
├── java-app/
├── nginx-app/
├── nodejs-app/
└── python-app/
```

Each application contains its application code and a `Dockerfile`.

## What I Learned

Through this task, I learned how to create Dockerfiles, build Docker images, run containers, map ports, and verify web applications through the browser. I also got to see how different technologies like Node.js, Python, Java, Apache, React and Nginx can be run using Docker.