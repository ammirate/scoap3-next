# -*- coding: utf-8 -*-
#
# This file is part of SCOAP3 Repository.
# Copyright (C) 2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Admin views for managing API registrations."""

from flask import flash
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import macro
from invenio_db import db

from .models import Compliance


class ComplianceView(ModelView):
    """View for managing Compliance results."""

    can_edit = False
    can_delete = False
    can_create = False
    can_view_details = True
    column_default_sort = ('created', True)

    column_list = ('publisher', 'created', 'updated', 'doi', 'arxiv', 'accepted', 'results')
    column_formatters = {
        'results': macro('render_results'),
        'doi': macro('render_doi'),
        'arxiv': macro('render_arxiv'),
    }
    column_labels = {
        'results': 'Problems',
        'arxiv': 'Arxiv number',
    }
    column_sortable_list = ()

    list_template = 'scoap3_compliance/admin/list.html'
    details_template = 'scoap3_compliance/admin/details.html'

    def action_base(self, ids, action):
        """Calls given function for all id separately.
        @:return count of successful actions
        """
        count = 0
        for id in ids:
            id, _ = id.split(',')
            if action(id):
                count += 1

        db.session.commit()
        return count

    @action('accept', 'Accept', 'Are you sure you want to mark all selected record as accepted?')
    def action_accept(self, ids):
        count = self.action_base(ids, Compliance.accept)
        if count > 0:
            flash('%d compliance record(s) were successfully accepted.' % count, 'success')

    @action('reject', 'Reject', 'Are you sure you want to mark all selected record as rejected?')
    def action_reject(self, ids):
        count = self.action_base(ids, Compliance.reject)
        if count > 0:
            flash('%d compliance record(s) were successfully rejected.' % count, 'success')


compliance_adminview = {
    'model': Compliance,
    'modelview': ComplianceView,
    'category': 'Compliance',
}

__all__ = (
    'compliance_adminview',
)