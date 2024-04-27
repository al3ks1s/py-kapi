# py-kapi

Python Kmanga API Wrapper for fetching metadatas about chapters.

# Todo

- Authentication-required decorator
- Documentation
- Swagger github page for api responses (Some are very verbose)

# Common issues

- Code 403 - ERROR: The request could not be satisfied : Standard rejection from the delivery network due to geolocking, you must have an IP from the USA for the api to answer

You can use a public proxy to access kmanga but be careful about sending your credentials through it, can't guarantee that they're not logged as they're sent in cleartext .