## **Intro**
00:00 useful resources  
🔗 [meetup.com/aws-ontario-virtual-user-group/](http://meetup.com/aws-ontario-virtual-user-group/)  
🔗 [cantrill.io](http://cantrill.io/)  
🔗 [learn.cantrill.io/p/docker-fundamentals](http://learn.cantrill.io/p/docker-fundamentals)  
🔗 WeCloudData  
🔗 AWS  
4:55 Guest instructors & our Community hero 😊  
  
## **Class notices**  
7:30 Spend consideration  
🔗 [gitpod.io/user/billing](http://gitpod.io/user/billing)  
🔗 aws --> billing  
9:10 Homework  
  
## 🐳**Docker  Hands-on**  
**Setup**  
10:34 Instructions on Github  
🔗 Hands-on project source: [https://github.com/omenking/aws-bootcamp-cruddur-2023/tree/main](https://github.com/omenking/aws-bootcamp-cruddur-2023/tree/main)  
12:07 Launch GitPod (from your main branch)  
13:17 Hands-on start  

### **Discussion**  
**📝 Why containerise?** 
For portability: share the end configuration and end environment with others  
🎙 14:30 Guest instructors' insights  
👆🏻 Edith: containers are extremely handy for rigorous/repetitive testing tasks  
👆🏻 James: for simplicity - when app is shared across a large group of people, it simplifies the painful process of installing or compiling the missing or lacking requirements and modules (for example, node, npm, python).   
🔗 17:52 Real-world application: [Linuxserver.io](http://linuxserver.io/)    
🔗 23:25 [jfrog.com](http://jfrog.com/)  
 
### 🐳Docker  
24:30 Hands-on starts  

### Backend   
25:28 🐳Dockerfile  
26:05 Docker extension  
28:15 Docker hub  
30:14 Docker Image - scratch  
30:39 Docker Image - python  
🔗 [https://github.com/docker-library/python/blob/master/3.10/slim-buster/Dockerfile](https://github.com/docker-library/python/blob/master/3.10/slim-buster/Dockerfile)  
37:23 🐳Dockerfile explanation  
38:00 WORKDIR  
40:40 COPY  
57:28 Difference between CMD & RUN  
- 🎙 RUN = apt install h-top (becomes the component of the container image)  
- 🎙 CMD = what runs after the image has been built, inside the container.   

58:55 Set environmental variables    

- `export FRONTEND_URL="*"`  
- `export BACKEND_URL="*"`  
- Link: url + /api/activities/home  

1:04:18 Set EVN variables & Build container  

```docker
# Unset ENV variables
unset BAKCEND_URL
env | grep BACKEND
env | grep FRONTEND
FRONTEND_URL=*
unset FRONTEND_URL
env | grep FRONTEND
```
1:08:48 Difference bewteen Host OS & Guest OS  
1:12:13 Build container `**docker build** -t backend-flask ./backend-flask`  
1:19:40 Run container `**docker run** --rm -p 4567:4567 -it backend-flask`  
1:22:54 Set ENV & run docker container `FRONTEND_URL="*" BACKEND_URL="*" docker run --rm -p 4567:4567 -it backend-flask` (WILL FAIL)  
1:25:08 Troubleshooting - check the logs inside a docker container  
- A useful tip: how to access shell inside the container.  

![Attach Shell](https://github.com/mariachiinajar/aws-bootcamp-cruddur-2023/blob/submissions/journal/resources/week01%20Live%20stream%20-%20attach%20shell.png)

1:29:20 Solution - Set ENV variables and run the container again.
- What Doesn’t work
    `docker run --rm -p 4567:4567 -it backend-flask -e FRONTEND_URL="*" -e BACKEND_URL="*"`
    `docker run --rm -p 4567:4567 -it backend-flask -e FRONTEND_URL='*' -e BACKEND_URL='*'`
- What Works
    `docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' **backend-flask**`
- Always put the <container_name> at the end of the command.
1:41:58 Stop the container
    `docker run <image>`: when the container stops, it will be an exited state, but it’s still there for future reuse. 
    `docker run --rm <image>` : the tag `--rm` will destroy the container when it’s stopped. So it’s gone for good.
1:43:30 Containerise frontend
    `npm i`
1:45:20 Run`docker-compose`
1:49:58 `docker compose -f "docker-compose.yml" up -d --build`
- Applies updates, even to compose containers that are already running.
1:51:22 🎙Insights on `docker-compose`🐳🐳🐳🐳
- Try to learn the following well:
    - Getting into the machine
    - Knowing how to read the logs
    - Debugging Docker commands,`ENV` variables
🎙 James: starts straight with docker-compose to build an app — even he’s got only one container!

**Closing**  
1:58:50 Homework notice

<br>

## Resources

🔗 Week 1 learning material - [omenking/aws-bootcamp-cruddur-2023](https://github.com/omenking/aws-bootcamp-cruddur-2023/tree/main)

🔗 [Linuxserver.io](http://linuxserver.io/)

🔗 [jfrog.com](http://jfrog.com/)  

🔗 [github.com/docker-library/python/blob/master/3.10/slim-buster/Dockerfile](https://github.com/docker-library/python/blob/master/3.10/slim-buster/Dockerfile)  

### **Sponsors**

🔗 [meetup.com/aws-ontario-virtual-user-group/](http://meetup.com/aws-ontario-virtual-user-group/)  
🔗 [cantrill.io](http://cantrill.io/)  
🔗 [learn.cantrill.io/p/docker-fundamentals](http://learn.cantrill.io/p/docker-fundamentals)  
🔗 WeCloudData  
🔗 AWS  