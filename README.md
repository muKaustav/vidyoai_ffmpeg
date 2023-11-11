<h1 align="center">Vidyo.ai Backend Task 🧭</h1>

## 📚 | Problem Statement

- Task is to create a Python web service using FastAPI and PostgreSQL for video processing.
- This service should provide two main functionalities: **audio extraction** and **video watermarking**.
- In addition, you are expected to design and develop an efficient architecture that can handle multiple requests concurrently.

<br/>

## 🚀 | APIs (Run and Test)

_**Note:**_ Authentication is not implemented since it was not mentioned in the problem statement. But I have made the user creation flow nevertheless, and JWT authentication can be implemented easily.

### User

- **POST** `/user` : Create a new user.

```yml
FormData:
  - name
  - email
```

- **GET** `/user` : Get user details by user id.

### Video & Audio

- **POST** `/video/watermark` : Takes a video file and a watermark image as input, applies the watermark, stores the video in AWS S3, updates PostgreSQL the processed file and its details.

```yml
Query Params:
  - x_offset=10 (default)
  - y_offset=10 (default)

FormData:
  - files:
      - video.mp4
      - watermark.png
  - email
```

- **POST** `/audio/extract` : Takes a video file as input, extracts audio and stores the audio file in AWS S3, updates PostgreSQL with processed details.

```yml
FormData:
  - file: video.mp4
  - email
```

- **GET** `/video/watermark/{unique_id}` : Get video details and processsed video URL by unique video id.
- **GET** `/audio/extract/{unique_id}` : Get audio details and processsed audio URL by unique audio id.

### TEST APIs

```yml
1. POST http://localhost:4000/user
FormData:
  - name: <name>
  - email: <email>

2. GET http://localhost:4000/user

3. POST http://localhost:4000/video/watermark?x_offset=10&y_offset=10
Query Params:
  - x_offset=10
  - y_offset=10
FormData:
  - files:
      - <video.mp4>
      - <watermark.png>
  - email: <email>

Response: will return status code, and unique_id

4. POST http://localhost:4000/audio/extract
FormData:
  - file: <video.mp4>
  - email: <email>

Response: will return status code, and unique_id

5. GET http://localhost:4000/video/watermark/<unique_id>

6. GET http://localhost:4000/audio/extract/<unique_id>
```

  <br/>

## 🌐 | Test Project

- Install Docker Desktop, and clone this repository.
- Create .env file in the root directory. (Since this is a private repository, I have mentioned the credentials in the .env.example file, for your testing purposes. Please copy the contents of .env.example to .env)
- Change HOST_IP in .env to your host IP address.
- Run `docker-compose up --build --scale fastapi-web=3` to build the docker images, and start the containers, with 3 instances of **fastapi-web** running. This will demonstrate the load balancing capabilities of the application.
- Run `docker-compose down` to stop the containers.

<br/>

## 💻 | Architecture

### What I have implemented:

<p align = center>
    <img alt="Project Logo" src="https://raw.githubusercontent.com/muKaustav/vidyoai_ffmpeg/main/assets/implemented_arch.jpeg?token=GHSAT0AAAAAACGUZWEROTQOX6IPJUWPZDWKZKPZJNQ" target="_blank" />
</p>

- **FastAPI** is used to create the web service.
- **PostgreSQL** is used to store the user, video and audio task details.
- **AWS S3** is used to store the processed video and audio files.
- **Docker** is used to containerize the applications. Also using docker for ffmpeg environment. Containers can be scaled up and down, depending on the load.
- **Nginx** is used as a reverse proxy server, to load balance the requests between N instances of **fastapi-web**.
- Have created a distributed task queue using **RabbitMQ** and **Celery**. The Celery workers can be scaled up and down, depending on the load.

### What I can implement to improve the architecture:

<p align = center>
    <img alt="Project Logo" src="https://raw.githubusercontent.com/muKaustav/vidyoai_ffmpeg/main/assets/efficient_arch.jpeg?token=GHSAT0AAAAAACGUZWEQSALXK4CWSWC6MRB4ZKPZUHQ" target="_blank" />
</p>

- **Redis** can be used as a distributed cache, to store the task results. This will reduce the load on the database.
- **Kubernetes** can be used to orchestrate the containers. This will help in scaling the containers, and also in monitoring the containers.
- **AWS API Gateway** can be used to create a REST API, which will trigger the Celery tasks. This will help in decoupling the web service from the task queue, essentially opting for a microservice architecture.
- **AWS Elastic Load Balancer** can be used to load balance the requests between the N instances of **fastapi-web**.
- **PostgreSQL** can be replaced with **AWS RDS**. This will help in scaling the database, and also in monitoring the database.
- **FFMPEG** logic can be further improved upon by using more efficient codecs, and also by using GPU acceleration. Or we can use a cloud service like AWS Elastic Transcoder.

  <br/>

## 🧑🏽 | Author

**Kaustav Mukhopadhyay**

- Linkedin: [@kaustavmukhopadhyay](https://www.linkedin.com/in/kaustavmukhopadhyay/)
- Github: [@muKaustav](https://github.com/muKaustav)

<br/>

---
