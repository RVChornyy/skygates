![Logo of the project](https://github.com/RVChornyy/skygates/blob/develop/LOGO.jpg)
# Skygates

Django project for passengers flights reservations and managing the flight service configurations.

## Installing / Getting started

Python3 must be allready installed

```shell
git clone https://github.com/RVChornyy/skygates.git
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_data.json
```
You can create admin account:
```
python manage.py createsuperuser

```
Or use login: Rost
       password: "Vjqghj'rn_2021"

![link for diagram] (https://dbdiagram.io/d/655f9ef23be14957879dec3b)
![](https://github.com/RVChornyy/skygates/blob/develop/diagram.png) 
![link to website] (https://skygates.onrender.com/)
