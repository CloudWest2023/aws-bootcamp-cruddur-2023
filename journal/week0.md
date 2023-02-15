# Week 0 — Billing and Architecture

## $${\color{white}Team:\color{blue}Cloud \space West}$$ 
## $${\color{white}Team \space Members:\color{blue}Mani \space Raj \space \space \space allan-hsu \space \space \space mariachiinajar \space \space \space HemaKar \space \space \space HK}$$ 
## $${\space \color{blue}Harneet \space Kaur \space \space \space Ultra \space Man \space \space \space Arunmano \space \space \space Maayaa-06 \space \space \space UltraBoostDevil}$$ 


 ## Team To Do Checklist:
   
| TASK | COMPLETED |
|  --- |    ---    |
| Watched Live - Streamed Video | :heavy_check_mark: |
| Watched Chirag's - Spend Considerations   | -- |
| Watched Ashish's - Security Considerations | -- |
| Recreate Conceptual Diagram in Lucid Charts or on a Napkin | -- |
| Recreate Logical Architectual Diagram in Lucid Charts | -- |
| Create an Admin User | -- |
| Use CloudShell | -- |
| Generate AWS Credentials | -- |
| Installed AWS CLI | -- |
| Create a Billing Alarm | -- |
| Create a Budget | -- |

## Current AWS Organizations Structure

![Organization Structure](../_docs/assets/organization-structure.png)

1. `cruddur-dev` account contains IAM role `iamdeveloper` with just enough permissions for development.
2. Only ccounts under **DEV OU** are permitted to assume `iamdeveloper` role for access to AWS resources, otherwise permissions are very limited.
