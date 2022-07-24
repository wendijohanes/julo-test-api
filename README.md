Mini Wallet Exercise

https://documenter.getpostman.com/view/8411283/SVfMSqA3?version=latest

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

Now you can make curl request:
