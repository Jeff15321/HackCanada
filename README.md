## How to Run

When first cloning the repo, run the following commands to install the dependencies:

```
pip install -r requirements.txt
npm install
```

to run mongoDB locally, remember to create a .env file with the MONGODB_URI variable.
also go into atlas and add your ip address to the whitelist


to run the server:

```
cd backend
python manage.py runserver
```


to run the frontend:

```
cd frontend
npm run dev
``` 

//currently, all the api are in localhost