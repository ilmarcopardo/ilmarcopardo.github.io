from scholarly import scholarly

author = scholarly.search_author_id('1XGhMwgAAAAJ')
author = scholarly.fill(author, sections=['publications'])
pubs = author.get('publications', [])

if pubs:
    print(pubs[0]['bib'])
