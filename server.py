"""import tornado.ioloop
import tornado.web

class Hello(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class User(tornado.web.RequestHandler):

    def get(self):
        form = <form method="post">
        <input type="text" name="username"/>
        <input type="text" name="designation"/>
        <input type="submit"/>
        </form>
        self.write(form)

    def post(self):
        username = self.get_argument('username')
        designation = self.get_argument('designation')
        self.write("Wow " + username + " you're a " + designation)

application = tornado.web.Application([
    (r"/", Hello),
    (r"/user/", User),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()"""

import logging
import pandas
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import uuid
import json
import time
import pprint
import requests as req
from  tornado.escape import json_decode
from  tornado.escape import json_encode

from tornado.options import define, options

notes=pandas.read_csv("output.csv")
note = notes.as_matrix()
adrs = notes['Code'].as_matrix()
ident = notes['ident'].as_matrix()
surf= notes['Surface'].as_matrix()




def getPostalCode(adresse):
    url ="https://maps.googleapis.com/maps/api/geocode/json?address="+adresse+"&key=AIzaSyAcEgaNSix7lzDrxQP7IufvnPFUw0gQvQc"
    page = req.get(url)
    response = json.loads(page.text)
    latlong=str(response['results'][0]['geometry']['location']['lat'])+','+str(response['results'][0]['geometry']['location']['lng'])
    url2="https://maps.googleapis.com/maps/api/geocode/json?latlng="+latlong+"&key=AIzaSyAcEgaNSix7lzDrxQP7IufvnPFUw0gQvQc"
    page = req.get(url2)
    response = json.loads(page.text)
    code = str(response['results'][0]['address_components'][6]['long_name'])
    return  code
   
def getclosestschools(address, number):
	ad =[]
	postcode = getPostalCode(address)
        for i in range (len(adrs) ): 
		if abs(int(adrs[i])-int(postcode))<= 5 :
			if abs(int(surf [i]) - int(number))<=50:
				ad.append(note[i])

				
			
	


       
	return ad

define("port", default=8005, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/signup/", TestHandler),
            (r"/signin/", SignHandler),
	    (r"/test/", ResponseHandler),

        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=None)
    def post(self):
	self.redirect("/test/")

"""class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("signin.html", messages=None)"""


class TestHandler(tornado.web.RequestHandler):
    def get(self):
      self.render("signup.html", messages=None)
    def post(self):
        json_obj = json_encode(self.request.body)
        print json_obj
        dico= {}
        dico['data1'] = "Hello"
        self.write(json.dumps(dico))



class SignHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("signin.html", messages=None)

    """def post(self):
        json_obj = json_decode(self.request.body)
        print('Post data received')

        for key in list(json_obj.keys()):
            print('key: %s , value: %s' % (key, json_obj[key]))

        # new dictionary
        response_to_send = {}
        response_to_send['newkey'] = json_obj['key1']

        print('Response to return')

        pprint.pprint(response_to_send)

        self.write(json.dumps(response_to_send))"""
	
class ResponseHandler(tornado.web.RequestHandler):
	def get(self):
        	exams = getclosestschools("rue vivienne", "3886")
		self.render("test1.html", exams = exams, messages=None)
		for exam in exams:
                	print exam
        time.sleep(1)
      #  req.get("http://sms.tritux.com/v1/send?username=tunihack15&password=apt15189&origin=tunihack&destination=20041974&text=hello")
	def post(self):
		res = json_decode(self.request.body)
		print res
        
	


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen('8005', address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
