# How to get started using the development API

You can use virtual env [recommended]. Make sure you're also using `python3`.

```bash
cd backend
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python app.py
```

or if you don't mind doing things globally:

```
cd backend
pip3 install -r requirements.txt
python3 app.py
```

<<<<<<< HEAD
## Frontend

The frontend can initially be used without the dev server; it provides some sample data
for initial testing and usage. Once you get going though you'll need to change the url
to match the url of the backend API.

```bash
cd frontend
# install helper scripts
npm install

# start the dev server on first available port.. likely 8080
npm start
```

See Frontend README for more details.
=======

>>>>>>> d39c30229b3ac1feb90923d0bbc292a917a0ab7b
