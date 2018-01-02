import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from datetime import datetime
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model


class Article(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4())
    source_url = columns.Text(primary_key=True, index=False, required=True)
    imported_at = columns.DateTime()
    description = columns.Text(required=True)
    author = columns.Text(required=False, index=True)
   # keywords = columns.List(value_type=columns.Text, index=True)


if __name__ == "__main__":
    connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)
    sync_table(Article)
    art = Article.create(source_url="http://vg.no",
                         imported_at=datetime.now(),
                         description="A test article",
                         author="Mr Roboto",
                         keywords=["test", "roboto", "kjeks", "smør"]
                         )

    print(Article.objects.count())