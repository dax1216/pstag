# PST.AG Car Search
## Getting Started
```bash
gh repo fork --clone=true https://github.com/dax1216/pstag.git
mkvirtualenv -p ~/.pyenv/versions/3.12.2/bin/python pstag-py3.12.2
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata cars.json
./manage.py createsuperuser
./manage.py runserver
```
## More instructions
* Make sure to create a copy of .env-sample and rename to .env
* Change values in .env to match your local environment