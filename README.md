<h1 align="center">Vidyo.ai Backend Task 🧭</h1>

## 📚 | Problem Statement

- Task is to create a Python web service using FastAPI and PostgreSQL for video processing.
- This service should provide two main functionalities: **audio extraction** and **video watermarking**.
- In addition, you are expected to design and develop an efficient architecture that can handle multiple requests concurrently.

<br/>

## 🚀 | APIs

### User

- **POST** `/user` : Create a new user.
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

  <br/>

## 🌐 | Test Project

- Install Docker Desktop, and clone this repository.
- Create .env file in the root directory. (Since this is a private repository, I have mentioned the credentials in the .env.example file, for your testing purposes. Please copy the contents of .env.example to .env)
- Change HOST_IP in .env to your host IP address.
- Run `docker-compose up --build --scale fastapi-web=3` to build the docker images, and start the containers, with 3 instances of **fastapi-web** running. This will demonstrate the load balancing capabilities of the application.
- Run `docker-compose down` to stop the containers.

<br/>

## 💻 | Architecture

- ![](./assets/architecture.png)

<br/>

## 🧑🏽 | Author

**Kaustav Mukhopadhyay**

- Linkedin: [@kaustavmukhopadhyay](https://www.linkedin.com/in/kaustavmukhopadhyay/)
- Github: [@muKaustav](https://github.com/muKaustav)

<br/>

---
