from flask_cli import with_appcontext

from dojson.contrib.marc21.utils import create_record, split_stream
from scoap3.dojson.hep.model import hep
from invenio_records import Record
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from scoap3.modules.pidstore.minters import scoap3_recid_minter
from flask import url_for

import click
import sys

@click.group()
def loadrecords():
    """Migration commands."""


@loadrecords.command()
@click.argument('source', type=click.File('r'), default=sys.stdin)
@with_appcontext
def loadrecords(source):
    """Load records migration dump."""
    click.echo('Loading dump...')

    recs = [hep.do(create_record(data)) for data in split_stream(source)]

    import ipdb
    for i, obj in enumerate(recs, start=1):
        print("Creating record {}/{}".format(i,len(recs)))
        obj['$schema'] = url_for('invenio_jsonschemas.get_schema', schema_path="hep.json")
        del obj['self']
        record = Record.create(obj, id_=None)
        print record

        # Create persistent identifier.
        pid = scoap3_recid_minter(str(record.id), record)

        # Commit any changes to record
        record.commit()

        # Commit to DB before indexing
        db.session.commit()

        # Index record
        indexer = RecordIndexer()
        indexer.index_by_id(pid.object_uuid)
