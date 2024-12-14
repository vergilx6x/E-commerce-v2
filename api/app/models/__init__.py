#!/usr/bin/python3
"""
initialize the models package
"""


from api.app.engine.db_engine import DBStorage

storage = DBStorage()
storage.reload()