<div align="center">
  <p align="center"><h1>pipe_pocket</h1></p>
</div>
<div align="center">

  <a href="">![GitHub issues](https://img.shields.io/github/issues/Besix2/pipe_pocket)</a>
  <a href="">![GitHub last commit](https://img.shields.io/github/last-commit/Besix2/pipe_pocket)</a>
  <a href="">![GitHub Repo stars](https://img.shields.io/github/stars/Besix2/pipe_pocket?color=gree)</a>

</div>

## Description

This application synchronizes pocket items with notion databases. It synchronizes the name, Url and tags to notion.

## Usage

### 1. Go to [pocket](https://getpocket.com/developer/apps/) and create a new application. Enter the following settings:
       Permissions: retrieve
       Apllication-Type: Windows-Desktop
### 2. Copy the token
### 3. Git clone the project and install requirements using:
       pip install requirements.txt
### 4. Start the authenticator.py script
### 5. Enter your consumer token
### 6. Open the link thats get printed to the terminal and authorize the application. When this is finsihed head back to the terminal and press enter.
### 7. Copy the resulting access token.
### 8. Go to [pipedream](https://pipedream.com/workflows) and create a new workflow. The trigger is "pocket new item added" and the reaction is python code.
![Screenshot 2023-05-06 141621](https://user-images.githubusercontent.com/92743858/236623571-0f59c75e-4755-4b0d-8280-c7d5251417d5.png)
### 9. Copy the code from pipedreeam_python.py into the python module and change the consumer and access key.
        [...]
        def get_tags():#extract tags from pocket api call because pipedreams call doesn't return tags because of detailType not being "complete"
        consumer_key = "your-consumer-key"
        access_token = "your-access-token"
        [...]
### 10. Go to notion and click on the 3 dots in the upper right corner than connections und connect to pipedream.
### 11. The last step before deploying is to create four databases one for reddit, one for instagram, one for youtube and one for articles.
### 11.1 The Databases need to have 3 properties Title, Url and Tags. In the end they should look like this:
![Screenshot 2023-05-06 143434](https://user-images.githubusercontent.com/92743858/236624476-7a3e36b1-ebb8-4455-bfb8-cf3921b72d9e.png)
### 12. Copy the database Id's by clicking on "share link to database". The database id is the first number sequence. Copy these Ids in their fields.
        [...]
        def db_id_set(extracted_url):#set database id depending on type of saved content
          if "insta" in extracted_url:
            db_id = "your insta database-id"
          elif "reddit" in extracted_url:
            db_id = "your reddit database-id"
          elif "youtube" in extracted_url:
            db_id = "your youtube database-id"
          else:
            db_id = "your article database-id"
        [...]
### 12.1 For example in this link:
         "https://www.notion.so/a1b023b304144b528159465200597a58?v=2974d30753f84a1bad901d34412844"
         
         "a1b023b304144b528159465200597a58" is the Id.
### 13. Test and deploy your Workflow.

Thats it now your Pocket is connected to notion.


