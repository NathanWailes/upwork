import os
from whoosh.index import create_in
from whoosh.fields import Schema, STORED, TEXT
from whoosh.qparser import QueryParser

mongodb_search_index_schema = Schema(mongodb_id=STORED,
                                     content=TEXT(stored=True))

directory_to_store_index_in = "search_index"
if not os.path.exists(directory_to_store_index_in):
    os.makedirs(directory_to_store_index_in)

index = create_in(directory_to_store_index_in, mongodb_search_index_schema)

writer = index.writer()

writer.add_document(mongodb_id=u"First document",
                    content=u"This is the first document we've added!")

writer.add_document(mongodb_id=u"Second document",
                    content=u"The second one is even more interesting!")
writer.commit()

# Now query
with index.searcher() as searcher:
    query = QueryParser("content", index.schema).parse("first")
    results = searcher.search(query)
    print(results[0])
