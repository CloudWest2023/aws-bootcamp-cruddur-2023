# Week 0 — Billing and Architecture

## $${\color{white}Team:\color{blue}Cloud \space West}$$ 
## $${\color{white}Team \space Members:\color{blue}Mani \space Raj \space \space \space allan-hsu \space \space \space mariachiinajar \space \space \space HemaKar \space \space \space HK}$$ 
## $${\space \color{blue}Harneet \space Kaur \space \space \space Ultra \space Man \space \space \space Maayaa-06 \space \space \space UltraBoostDevil}$$ 


 ## Team To Do Checklist:
   
| TASK | COMPLETED |
|  --- |    ---    |
| Watched Live - Streamed Video | :heavy_check_mark: |
| Watched Chirag's - Spend Considerations   | :heavy_check_mark: |
| Watched Ashish's - Security Considerations | :heavy_check_mark: |
| Recreate Conceptual Diagram in Lucid Charts or on a Napkin | :heavy_check_mark: |
| Recreate Logical Architectual Diagram in Lucid Charts | :heavy_check_mark: |
| Create an Admin User | :heavy_check_mark: |
| Use CloudShell | :heavy_check_mark: |
| Generate AWS Credentials | :heavy_check_mark: |
| Installed AWS CLI | :heavy_check_mark: |
| Create a Billing Alarm | :heavy_check_mark: |
| Create a Budget | :heavy_check_mark: |

## Current AWS Organizations Structure

![Organization Structure](../_docs/assets/organization-structure.png)

1. `cruddur-dev` account contains IAM role `iamdeveloper` with just enough permissions for development.
2. Only ccounts under **DEV OU** are permitted to assume `iamdeveloper` role for access to AWS resources, otherwise permissions are very limited.


## Architecture Diagrams

HemaKar (Hemalakshmi Kannan): [Conceptual and Logical Diagrams](https://lucid.app/lucidchart/d1407ad3-3f3d-4015-a3b1-36adbcfb8061/edit?viewport_loc=-1038%2C-358%2C2520%2C1612%2C0_0&invitationId=inv_7919566f-49fa-4510-8171-ea7c72ce9235)

k3kmani (Mani Raj):

allan-hsu (Allan Hsu): [Conceptual and Logical Diagrams](https://lucid.app/lucidchart/f7e59b81-605f-4131-af03-1657c3f03f6e/edit?invitationId=inv_fcbe1868-1e2e-4e80-a987-ff61c0c6f463)

mariachiinajar (Goeun Gil): [Conceptual Diagram](https://lucid.app/lucidchart/3a9760e3-df75-438a-b0e6-158e641871ef/edit?viewport_loc=-1863%2C-11885%2C7168%2C3412%2C0_0&invitationId=inv_38e40548-c558-46e2-aa36-f3e51ba96d6a) and [Logical Diagram](https://lucid.app/lucidchart/011e0247-49dc-4d1e-8a40-b6b116f8d571/edit?viewport_loc=-2120%2C-1667%2C3903%2C1858%2C0_0&invitationId=inv_5c09fd58-3214-41f2-88ac-bdf85d63413b)

ultraman-labs (Tony Quintanilla): [Conceptual Diagrams](https://lucid.app/lucidchart/invitations/accept/inv_bb3d008f-13c4-4567-a2d5-ea2dfe5556bb) and [Logical Diagrams ](https://lucid.app/lucidchart/d1ab9877-6c23-4cfe-a972-45be0f5d3757/edit?viewport_loc=-137%2C-357%2C1872%2C910%2C0_0&invitationId=inv_119312fa-3f6b-4505-af42-5ad2b6b5165b)

maayaa06 (Sharon Sekyere):

Harneetk21 (Harneet Kaur):
