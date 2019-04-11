import click

import requests
import hashlib

class BreachedPassword(object):
   
   pass_url = 'https://api.pwnedpasswords.com/range/'
   
   def __init__(self, headers):
      self.headers = headers
      
   # Function to trigger pwned api and get response
   def get_response(self, initial_hash):
      response = requests.get(self.pass_url + initial_hash,
                              headers = self.headers)
      #TODO: Handle 429 and 400 cases
      if response.status_code == requests.codes.too_many_requests:
         return None
      
      return response

   # Function to check if password breach
   def check_passwd_breach(self, passwd):
      hashed_passwd_obj = hashlib.sha1(passwd.encode())
      hashed_passwd_str = hashed_passwd_obj.hexdigest()
      initial_hash = hashed_passwd_str[:5].upper()
      response = self.get_response(initial_hash)
      hashed_pass_list = response.text.split('\n')
      
      for passwd in hashed_pass_list:
         remaining_hash = passwd.split(':')[0]
         passwd_breach_count = passwd.split(':')[1]
         current_hash = initial_hash + remaining_hash
         if hashed_passwd_str.upper() == current_hash.encode('UTF-8'):
            print "OOPS!! Looks like your password been breached :("
            print "Times it appeared in the breach dataset: {0}".format(passwd_breach_count)
            #TODO: password suggestion mechanism
            break
