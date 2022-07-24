Mini Wallet Exercise

https://documenter.getpostman.com/view/8411283/SVfMSqA3?version=latest

This test is built using Django 4 & Django REST Framework.
How to install and run this program: (on UNIX based OS, Linux or BSDs)
1. **git clone https://github.com/wendijohanes/julo-test-api**
2. create virtual environment (python >= 3.6) & activate virtual environment
3. Make sure these packages are installed in python env:

   **pip install Django**
  
   **pip install django-rest-framework**
  
   **pip install django_cleanup**
  
   **pip install Markdown**
  
   **pip install django-filter**
  
   **pip install django-oauth-toolkit** (My system needs rust compiler to install this package)
  
  
 4. Check error syntax & depedencies before running: **./manage.py check**
 5. Migrate database using sqlite (or other database): **./manage.py migrate**
 6. Run server as localhost: **./manage.py runserver**

Now you can make curl request: (default localhost port 8000, so use http://127.0.0.1:8000)

**Init New User & Wallet**

*curl --location --request POST http://127.0.0.1:8000/api/v1/init --form 'customer_xid="ea0212d3-abd6-406f-8c67-868e814a2436"'*

**Enable Wallet**

*curl --location --request POST http://127.0.0.1:8000/api/v1/wallet --header 'Authorization: Token 6b3f7dc70abe8aed3e56658b86fa508b472bf238'*

**View Balance Wallet**

*curl --location --request GET http://127.0.0.1:8000/api/v1/wallet --header 'Authorization: Token 6b3f7dc70abe8aed3e56658b86fa508b472bf238'*

**Deposit**
* curl --location --request POST 'http://localhost/api/v1/wallet/deposits' --header 'Authorization: Token 6b3f7dc70abe8aed3e56658b86fa508b472bf238' --form 'amount="100000"' --form 'reference_id="50535246-dcb2-4929-8cc9-004ea06f5241"' *
