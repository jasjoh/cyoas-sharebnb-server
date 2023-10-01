# Share B&B Server

## What is This?
This repo represents the back-end server for a bootcamp development project focused on building a web application from scratch with only basic requirements. It was developed as part of my Full-Stack Software Engineering curriculum at the Rithm School bootcamp in partnership with a fellow cohort member. 

In this case, we opted to choose React for our front-end in order to gain more experience with that library and Flask for our backend, since we preferred that over Express.js. For the backend we used PostgreSQL as that was the only database we were familiar with. We also leveraged Amazon S3 to support image storage and retrieval.

[Link to front-end repo.](https://github.com/jasjoh/cyoas-sharebnb-client)

## Key Learnings
- The need to explicitly type image uploads sent from React forms alongside JSON data to Flask APIs as multipart form data
- How to provision a new AWS account and S3 instance including IAM and policy management
- How challenging it is as an AWS novice to navigate their documentation as part of the above bullet point
- The challenges of time estimation and planning with working under fixed time constraints

## How to Run
- Run `pip install requirements.txt` to install pre-requisites
- Create a `.env` file with values for the following keys: `S3_BUCKET_NAME`, `AWS_REGION`, `SECRET_KEY`, `DATABASE_URL`
- Create an S3 bucket with appropriate permissions and setup appropriate local AWS environment variables
- Install and run PostgresQL then optionally run the `seed.py` file to initialize your DB and seed initial data
- Run the app via `python app.py` 

## API Design
![API Designs](https://github.com/jasjoh/cyoas-sharebnb-server/blob/main/sharebnb.apis.jpg "API Designs")

