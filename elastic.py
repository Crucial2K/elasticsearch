'''
Various elastic queries

'''
from elasticsearch import *
# Importing this library to use the prettyprint function for the json which is returned from elastic
import json

es = Elasticsearch('http://localhost/', port = 9200)

'''
 Search for all documents in the ecommerce index
 The equvialent of:
 GET ecommerce/_search?q=*
'''

'''
res = es.search("ecommerce")
print res
'''

'''
Search for all documents in the product type
The equivalent of 
GET ecommerce/prodcut/_search?q*
res = es.search(index="ecommerce", doc_type="product")
print res
'''

'''
Another way to return everything
res = es.search(index="ecommerce", doc_type="product",
        body={"query": {"match_all": {}}})

print res

'''


'''
Search for "pasta" in the product doc_type in the ecommerce index
Apparently you have to look in the "body" for the data
*I am not sure why this weird grouping of keywords work
res = es.search(index="ecommerce", doc_type="product", body={"query":{"match":{"name":"pasta"}}})
print res
'''

'''
Pretty print the json results
res = es.search(index="ecommerce", doc_type="product", body={"query":{"match":{"name":{"query":"pasta"}}}})
print json.dumps(res, indent=4)
'''

'''
Does this query do the same as that on line 33 and 39?
res = es.search(index="ecommerce", doc_type="product", 
        body={"query":
            {"match":
                {"name": "pasta"
                    }
                }
            })
print json.dumps(res, indent=4)

'''

'''
Return the values from multiple fields
res = es.search(index="ecommerce", doc_type="product", 
        body={"query":
            {"multi_match":
                {"query": "pasta",
                    "fields": ["name", "description"]
                    }
                }
            })
print json.dumps(res, indent=4)
'''

'''
Return the matches for a phrase
res = es.search(index="ecommerce", doc_type="product", 
        body={"query":
            {"match_phrase":
                {"name": "pasta spaghetti"
                    }
                }
            })
print json.dumps(res, indent=4)
'''

'''
Term level queries
Used for exact values - the search terms are not analyzed

res = es.search(index="ecommerce", doc_type="product", 
        body={"query":
            {"term":
                {"status": "active"
                    }
                }
            })
print json.dumps(res, indent=4)

'''

'''
Term level query - multiple values

res = es.search(index="ecommerce", doc_type="product", 
        body={"query":
            {"terms":
                {"status": ["active", "inactive"]
                    }
                }
            })
print json.dumps(res, indent=4)

'''

'''
Range query
res = es.search(index="ecommerce", doc_type="product",
        body={"query": {
            "range": {
                "quantity": {
                    "gte": 1,
                    "lte": 10
                    }
                }
              }   
            }
        )
print json.dumps(res, indent=4)

'''
'''
Compound query - MUST/AND
res = es.search(index="ecommerce", doc_type="product",
        body={"query": {
               "bool": {
                "must": [
                    {"match": {"name": "pasta"}},
                    {"match": {"name": "spaghetti"}}
                    ]
                }
              }   
            }
        )
print json.dumps(res, indent=4)
'''
'''
Must NOT
res = es.search(index="ecommerce", doc_type="product",
        body={"query": {
               "bool": {
                "must": [
                    {"match": {"name": "pasta"}}
                    ],
                    "must_not": [
                        {"match": {"name":"spaghetti"}}
                    ]
                }
              }   
            }
        )
print json.dumps(res, indent=4)

'''
'''
The bool query also has a "should" parameter. When the "should" clause is matched a documents relevancy score is increased otherwise it does nothing.  This is a way or ranking the relevancy of documents returned. Shoulds affect the relevancy of matching documents but otherwise do nothing. But there is one exception, if the search query has no "must" clause then at least one of the "should" clauses must match. So the should clauses behave like the logical "or" where at least one must be true. If at least one must clause is present then no should clauses are required to match and only affect the relevancy.
	
This will boost results that have spaghetti in their name but not exclude those that don't.



res = es.search(index="ecommerce", doc_type="product",
        body={"query": {
               "bool": {
                "must": [
                    {"match": {"name": "pasta"}}
                    ],
                    "should": [
                        {"match": {"name":"spaghetti"}}
                    ]
                }
              }   
            }
        )
print json.dumps(res, indent=4)

'''

'''
Create an index (myfoodblog) automatically
'''
res = es.index(index="myFoodBlog", doc_type="recipe", 
        body={"name": "Pasta Quattro Formaggi",
            "description": "First you boil the pasta, then you add the cheese",
            "ingrediants": [{
                "name": "Pasta",
                "amount": "500g"
                },{
                "name": "Fortina cheese",
                "amount": "100g"                    
                }, {
                    "name": "Parmesan cheese",
                    "amount": "100g"
                },{
                    "name": "Romana cheese",
                    "amount": "100g"
                    },{
                        "name": "Gorgonzola cheese",
                        "amount": "100g"
                        }
                ]
            })
#es.indices.refresh(index="myFoodBlog")
                    











