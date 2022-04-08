# Here is Running Instruction of Techwondoe Assignment Round 2


# Assignment Description : 

The assignment is to write a simple  API in Python that provides CRUD operations on JSON files.

- Functional Requirements
    - API should validate a JWT token before allowing access to the caller.
    - The JSON files should be stored on an S3 bucket. Following is the schema of JSON - 

- Assignment Round 2.png
    - API Resources to be exposed -
    - Create file - To create a new JSON file on an S3  bucket. UUID should be used to name a new file.
    - Get file - To read the contents of an existing JSON file.
    - Update file - To update the content of an existing JSON file. 
    - Delete File  - To delete a JSON file from the s3 bucket.

- Non Functional requirements:
    - Unit tests using moto or similar library to mock AWS services
    - Lint and prettier configurations
    - Dockerise the application
    - Readme file on how to deploy and run the service. 
    - Add a checklist of the above items on ReadMe and check all the items before submitting the assignment.


# Running Instruction : 

How to Run the App : 

    docker build --tag techwondoe-assignment .
    docker run -d -p 5000:5000 techwondoe-assignment

Checklist : 

- [x] Added jwt Authentication and Verification, Login and Signup
- [x] Create file from s3 API
- [x] Get file from s3 API
- [x] Update file from s3 API
- [x] Delete file from s3 API
- [ ] Unit tests using moto or similar library to mock AWS services
- [ ] Lint and prettier configurations
- [x] Dockerise the application
- [x] Created Readme file
