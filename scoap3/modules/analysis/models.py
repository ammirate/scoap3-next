# -*- coding: utf-8 -*-
#
# This file is part of SCOAP3 Repository.
# Copyright (C) 2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Database models for access module."""

from __future__ import absolute_import, print_function

from datetime import datetime
from invenio_db import db
from sqlalchemy import UniqueConstraint


class Gdp(db.Model):

    __tablename__ = 'analysis_gdp'

    __table_args__ = (UniqueConstraint(
        'name',
        name='analysis_gdp_unique'),
    )

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    """Primary key. It allows the other fields to be nullable."""

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    name = db.Column(db.String(150), nullable=False)

    value1 = db.Column(db.Integer, default=0, nullable=False, server_default='0')
    value2 = db.Column(db.Integer, default=0, nullable=False, server_default='0')
    value3 = db.Column(db.Integer, default=0, nullable=False, server_default='0')
    value4 = db.Column(db.Integer, default=0, nullable=False, server_default='0')