# rest-counter

This is a REST service that keeps track of an integer counter.  
To use, the user must first authenticate with a POST request to http://restcounter.duckdns.org:5000/v1/authenticate with the following body:

{ "email": "xxx@gmail.com", "password": "xxx" }

The user may alternatively hit the same url in the browser, without a body, to authenticate through Google.  
The response will contain a bearer token which contains the time to expiry.

With the bearer token, the use may do the following:

To get the next integer:

curl http://restcounter.duckdns.org:5000/v1/next -H “Authorization: Bearer XXXXXX”

To get the current integer:

curl http://restcounter.duckdns.org:5000/v1/current -H “Authorization: Bearer XXXXXX”

To reset the current integer:

curl -X “PUT” https://restcounter.duckdns.org:5000/v1/current -H “Authorization: Bearer XXXXX”
--data “current=1000”


# Assumptions:

The counter is an integer, and will start from 0.
The state of the counter is persistent and consistent across all users.
Any new user can register without restrictions, as long as they do not collide with an existing user's email.

