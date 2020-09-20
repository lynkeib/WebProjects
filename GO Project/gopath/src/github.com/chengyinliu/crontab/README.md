Project Stack Intro:
- Frontend
    - Bootstrap
    - jQuery

- Backend
    - Language: GO
    - Database: MongoDB
    - Server: Nginx

- Highlights:
    - High availability
    - Partition tolerance 
    - etcd based status management
    
- Problems for traditional crontab
    - Tasks schedule would be terminated if the machine malfunctioning. 
    - Need human force to migrate tasks if one single machine running out of resources by having too many tasks
    - Need go to the machine to check and config cron

- How we solve?
<img src="img/Solution Framework.png"/>