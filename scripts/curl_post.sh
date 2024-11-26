#!/bin/bash
#watch -n 1 curl -X  POST 127.0.0.1:8080/echo -v
#curl -X POST -H "Content-Type: application/json" -d '{"name":"John Doe", "age": 30, "city": "New York"}' 127.0.0.1:8080/echo
curl -X POST -H "Content-Type: application/json" -d @data.json 127.0.0.1:8080
