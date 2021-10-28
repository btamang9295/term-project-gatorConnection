# Credentials Folder

## The purpose of this folder is to store all credentials needed to log into your server and databases. This is important for many reasons. But the two most important reasons is
    1. Grading , servers and databases will be logged into to check code and functionality of application. Not changes will be unless directed and coordinated with the team.
    2. Help. If a class TA or class CTO needs to help a team with an issue, this folder will help facilitate this giving the TA or CTO all needed info AND instructions for logging into your team's server. 


# Below is a list of items required. Missing items will causes points to be deducted from multiple milestone submissions.


1. Server/Website URL: ec2-13-57-42-22.us-west-1.compute.amazonaws.com
2. SSH username: ubuntu
3. SSH password or key: main_ubuntu_CSC648Team05_key_pair.pem (key uploaded in credentials folder)
4. Database URL or IP and port used: ubuntu-csc648team05db.clbwe7zwx6so.us-west-1.rds.amazonaws.com    
5. Database username: CSC648Team05
6. Database password: CSC05GinyuForce!!
7. Database name(only a test database in here now): CSC648_test_database
8. Instructions on how to use the above information.

To connect to mysql database click on + icon in mysql workbench, then fillout according to the below:

1. Connection Name: whatever you want
2. Connection Method: Standard TCP/Ip over SSH
3. ssh hostname: ec2-13-57-42-22.us-west-1.compute.amazonaws.com
4. ssh username: ubuntu
5. (we dont need ssh password)
6. keyfile(store in vault): wherever main_ubuntu_CSC648Team05_key_pair.pem file is located (pem file is uploaded in crednetials folder) 
7. MySQL hostname: ubuntu-csc648team05db.clbwe7zwx6so.us-west-1.rds.amazonaws.com
8. MySQL Server port: 3306
9. Username: CSC648Team05
10. Password(store in vault): CSC05GinyuForce!!

(img will be provided here for reference called succesful connection main database)

How to connect to ec2 instance on cloud shown below(example photo shown called succesful ssh i):

If on windows 10, go to where Linux subsystem is and make sure the key file is located in there, you will know if you are there if your address starts with ~

For example:

alectenefrancia@DESKTOP-5KD2T48:~$

Then do ls to make sure the key is in there:

alectenefrancia@DESKTOP-5KD2T48:~$ ls

main_ubuntu_CSC648Team05_key_pair.pem

Then do:

ssh -i "main_ubuntu_CSC648Team05_key_pair.pem" ubuntu@ec2-13-57-42-22.us-west-1.compute.amazonaws.com 

if it does not work, then do:

sudo ssh -i "main_ubuntu_CSC648Team05_key_pair.pem" ubuntu@ec2-13-57-42-22.us-west-1.compute.amazonaws.com -l ubuntu

it will prompt you for your linux password, enter that

once it works, you should see:

ubuntu@ip-172-31-19-158 




# Most important things to Remember
## These values need to kept update to date throughout the semester. <br>
## <strong>Failure to do so will result it points be deducted from milestone submissions.</strong><br>
## You may store the most of the above in this README.md file. DO NOT Store the SSH key or any keys in this README.md file.
