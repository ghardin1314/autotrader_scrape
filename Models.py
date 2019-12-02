# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 15:23:54 2019

@author: Garrett
"""


from config import db

class Make(db.Model):
    __tablename__ = "make"
    make_id = db.Column(db.Integer, primary_key=True)
    make_name = db.Column(db.String(32))
    make_value = db.Column(db.String(32))
    xodels = db.relationship(
            'Xodel',
            backref='make',
            cascade='all, delete, delete-orphan',
            single_parent=True
            )

class Xodel(db.Model):
    __tablename__ = "xodel"
    xodel_id = db.Column(db.Integer, primary_key=True)
    make_id = db.Column(db.Integer, db.ForeignKey('make.make_id'))
    xodel_name = db.Column(db.String(32))
    xodel_value = db.Column(db.String(32))
    trims = db.relationship(
            'Trim',
            backref='xodel',
            cascade='all, delete, delete-orphan',
            single_parent=True
            )

class Trim(db.Model):
    __tablename__ = "trim"
    trim_id = db.Column(db.Integer, primary_key=True)
    xodel_id = db.Column(db.Integer, db.ForeignKey('xodel.xodel_id'))
    trim_name = db.Column(db.String(32))
    trim_value = db.Column(db.String(32))
