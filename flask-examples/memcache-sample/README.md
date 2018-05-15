# Apache + Python WSGI app

----
## Base
Vagrant

* Ubuntu Xenial 16.04

----
## Pre-Requisites

* Vagrant
* VirtualBox
* ChefDK

----
## Usage
1. Runs an application over 8080 and redirects to HTTPS.
2. Runs a python based application over 80
   * / -> displays a test page
   * /stats -> displays memcache stats

*NOTE: To test this application, make sure you have pre-requisites Installed.*
```
# clone this github repository
git clone <git_url>
cd python-practices
vagrant up
```
----
## Host port mapping
1. *Test Application with HTTPS redirect*
    * Guest port: 8080, Host port: 9090
    * Guest port: 8443, Host port: 8443
2. *Python Application with WSGI*
    * Guest port: 80, Host port: 9080
----
## Connect to URL
*NOTE: Use Host port from your host machine to connect to the application*

----
## Samples
```
$ curl -I http://localhost:9090
HTTP/1.1 301 Moved Permanently
Date: Wed, 27 Sep 2017 13:40:57 GMT
Server: Apache/2.4.18 (Ubuntu)
Location: https://localhost:8443
Content-Type: text/html; charset=iso-8859-1

$ curl -Ik https://localhost:8443
HTTP/1.1 200 OK
Date: Wed, 27 Sep 2017 13:41:13 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Type: text/html;charset=UTF-8

$ curl -i http://localhost:9080
HTTP/1.1 200 OK
Date: Wed, 27 Sep 2017 13:41:47 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Length: 6
Vary: Accept-Encoding
Content-Type: text/html; charset=utf-8
Index!

$ curl -i http://localhost:9080/stats
HTTP/1.1 200 OK
Date: Wed, 27 Sep 2017 13:41:57 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Length: 576
Vary: Accept-Encoding
Content-Type: text/html; charset=utf-8
<html>
<head>
    <title>Website</title>
<style>
@import url(http://fonts.googleapis.com/css?family=Amatic+SC:700);
body{
    text-align: center;    
}
h1{
    font-family: 'Amatic SC', cursive;
    font-weight: normal;
    color: #8ac640;
    font-size: 2.5em;
}
</style>
</head>
<body>
<div class="block1">
<h1>Hello</h1>
  <h2>Here is a DevOps quote for you: </h2>
  <p>
DevOps is not about Automation
  </p>
  <h3>Key: test1</h3>
  <h3>KeySet: True</h3>
  <h3>Hits: 29</h3>
  <h3>Misses: 13</h3>
  <h2>Percentage Hit Ratio: 30.95 %</h2>
</div>
</body>
</html>
```

----
## Screenshot of python app
![screenshot](https://github.com/abhiTamrakar/python-practices/blob/master/flask-examples/memcache-sample/working_python_app.png "Python App with memcache")

----
## Thanks

