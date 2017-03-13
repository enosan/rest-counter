# rest-counter

This is a REST service that keeps track of an integer counter.  
To use, the user must first authenticate with a POST request to https://restcounter.duckdns.org:5000/v1/authenticate with the following body:

{ "email": "xxx@gmail.com", "password": "xxx" }

An example using curl:

curl -X "POST" https://restcounter.duckdns.org:5000/v1/authenticate -H "Content-Type: application/json" --insecure --data '{"email":"xxx@gmail.com","password":"xxx"}'

This returns something like this:

{
  "data": {
    "attributes": {
      "access_token": "eyJhbR5cCI6IkpXVCJ9.eyJpYXQiOjE0ODk0MjYwMDQsInN1YiI6ImVub0BnbWFpbC5jb20iLCJleHAiOjE0ODk0Mjk2MDR9.7S4nyMG2TFadUOaUH4-iDuskhcnMvXgN7g4d_C7BJWc",
      "expires_in": 3600,
      "token_type": "Bearer"
    },
    "id": "Mon, 13 Mar 2017 17:26:44 GMT",
    "type": "token"
  }
}

The user may alternatively hit the same url in the browser, without a body, to authenticate through Google.  
The response will contain a bearer token which contains the time to expiry.

With the bearer token, the use may do the following:

To get the next integer:

curl https://restcounter.duckdns.org:5000/v1/next -H “Authorization: Bearer XXXXXX” --insecure

To get the current integer:

curl https://restcounter.duckdns.org:5000/v1/current -H “Authorization: Bearer XXXXXX” --insecure

To reset the current integer:

curl -X “PUT” https://restcounter.duckdns.org:5000/v1/current -H “Authorization: Bearer XXXXX” --insecure
--data “current=1000”

The "insecure" flag is necessary as the SSL certificate used for this server is self-signed and not CA-issued.


# Assumptions:

The counter is an integer, and will start from 0.

The state of the counter is persistent and consistent across all users.

Any new user can register without restrictions, as long as they do not collide with an existing user's email.

