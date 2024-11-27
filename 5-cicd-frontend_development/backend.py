#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from flask import Flask


app = Flask(__name__)

@app.route("/cat_get")
def hello_world():
    return 'https://as1.ftcdn.net/v2/jpg/02/39/85/02/1000_F_239850263_MJxcynTmX7HFBVvSC1eT635cB7HNElWR.jpg'

if __name__ == '__main__':
    app.run(debug=True, host='::', port='3001')

