# GaoDuckCreativity
National University of Kaohsiung Student Creativity Competition Management System  
為國立高雄大學為鼓勵學生創新、創意、創業而舉辦的第 12 屆「激發學生創意競賽」設計的電子化的競賽管理系統


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

# Report

[Report](./DB_Report_Final_for_pubilc.pdf)
