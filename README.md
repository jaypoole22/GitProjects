# Financial Tracker Project (AWS)
This project showcases a personal cloud project I did using AWS. The primary focus of this project was to include as many AWS services as possible to create a financial tracking application. I used a CI/CD pipeline on the frontend of the application. The majority of the frontend coding for this project was based on a template, allowing the implementation of cloud services to remain the main focus.
## Services
AWS Lambda, API Gateway, AWS Amplify, CloudWatch, DynamoDB, and IAM were the key services used in this project. Below, I  have included the architectural diagram used to create this app.
<p align= "center"> <img width="800" height="800" alt="image" src="https://github.com/user-attachments/assets/744f4fe8-f7da-4edd-92f3-22c1d2394413" /> <p>
 AWS Amplify (CI/CD Deployment)
 API Gateway (Routing & integration)
 DynamoDB (NoSQL storage for expenses and budgets)
 AWS Lambda (Data processing & analysis)
 Lambda Function URL (Directly called from frontend)
 CloudWatch (Optional monitoring/logging)
 IAM
 Every service in this project serves a key purpose. AWS Amplify is for creating the CI/CD pipeline between the frontend code in GitHub and Amplify hosting. AWS backend 
