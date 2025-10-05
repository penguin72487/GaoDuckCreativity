# GaoDuckCreativity
National University of Kaohsiung Student Creativity Competition Management System

# React + Flask + Pymsql

環境設置
```
conda create -n GaoDuck python=3.12
conda activate GaoDuck

conda install Flask
conda install flask flask-cors

pip install Flask
pip install flask flask-cors
```


# start
```
py run.py
cd react-frontend
npm install
npm start
```


# database connect (server run MySQL 8.0.35)
copy `/api/sql_config.sample.json` to `/api/sql_config.json`

fill in IP, username, password, dbname

