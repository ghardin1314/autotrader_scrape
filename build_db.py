# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 15:47:20 2019

@author: Garrett
"""
import os
from config import db
from Models import Make, Xodel, Trim
import sqlite3 as lite

MAKES = [
    {
      'name': 'Acura',
      'value': 'ACURA',
      'models': [
        {
            'name': 'CL',
            'value': 'ACUCL',
            'trims': [
                {
                    'name': 'Type-S',
                    'value': 'ACUCL|Type-S',
                    'details': [{'name': 'isSeries', 'value': False}]
                }
            ]
        },
        {
            'name': 'Integra',
            'value': 'INTEG',
            'trims': [
                {
                    'name': 'GS',
                    'value': 'INTEG|GS',
                    'details': [{'name': 'isSeries', 'value': False}]
                },
                {
                    'name': 'GS-R',
                    'value': 'INTEG|GS-R',
                    'details': [{'name': 'isSeries', 'value': False}]
                }
            ]
        }]
    },
    {
      'name': 'Alfa Romeo',
      'value': 'ALFA',
      'models': [
        {
            'name': '164',
            'value': 'ALFA164',
            'trims': [
                {
                    'name': 'L',
                    'value': 'ALFA164|L',
                    'details': [{'name': 'isSeries', 'value': False}]},
                {
                    'name': 'LS',
                    'value': 'ALFA164|LS',
                    'details': [{'name': 'isSeries', 'value': False}]}
                    ]
        }]
    }]

# breakpoint()


if os.path.exists("models.db"):
    os.remove('models.db')

db.create_all()


for make in MAKES:

    # breakpoint()
    name = make.get('name')
    value = make.get('value')
    m = Make(make_name = name, make_value = value)

    for model in make.get('models'):
        ma = m.xodels
        xa = Xodel(xodel_name = model.get('name'), xodel_value = model.get('value'))
        ma.append(xa)

        for trim in model.get('trims'):
            tr = xa.trims
            tr.append(Trim(trim_name = trim.get('name'), trim_value = trim.get('value')))

    db.session.add(m)

db.session.commit()

conn = lite.connect('models.db')
cur = conn.cursor()

with conn:
    cur.execute("SELECT * FROM make")
    print(cur.fetchall())

    cur.execute("SELECT * FROM xodel")
    print(cur.fetchall())

    cur.execute("SELECT * FROM trim")
    print(cur.fetchall())









