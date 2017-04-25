
### Ensembl Client
### Version: Beta
### Python : 2.7
### Author : alessio.marcozzi@gmail.com
### API    : http://rest.ensembl.org/

import sys
import httplib2
import json

http = httplib2.Http(".cache") 
server = "http://rest.ensembl.org"


def check_response(resp):
    if not resp.status == 200:
        print("Invalid response: ", resp.status)
        sys.exit()


def decode(content):
    decoded = json.loads(content)
    print repr(decoded)


def request(server, ext, method="GET", content_type="application/json"):
        return http.request(server+ext, method, headers={"Content-Type":content_type})


def get_archive(ensembl_stable_id): # ...callback=None):
    '''Uses the given identifier to return the archived sequence'''
    ext = "/archive/id/"+ensembl_stable_id+"?"
    resp, content = request(server, ext)
    check_response(resp)
    decode(content)
#Example:
#get_archive('ENSG00000157764')


def get_gentree(ensembl_gentree_id): # ...aligned=0, callback=None, compara='multi', nh_format='simple', sequence='protein'):
    '''Retrieves a gene tree dump for a gene tree stable identifier'''
    ext = "/genetree/id/"+ensembl_gentree_id+"?"
    resp, content = request(server, ext)
    check_response(resp)
    decode(content) 
#Example
#get_gentree('ENSGT00390000003602')


def get_xrefs(species, symbol): # ...callback=None, db_type='core', external_db=None, object_type=None):
    '''Looks up an external symbol and returns all Ensembl objects linked to it.
    This can be a display name for a gene/transcript/translation,
    a synonym or an externally linked reference.
    If a gene's transcript is linked to the supplied symbol
    the service will return both gene and transcript (it supports transient links).'''
    ext = "/xrefs/symbol/homo_sapiens/BRCA2?"
    resp, content = request(server, ext)
    check_response(resp)
    decode(content)
#Example:
#get_xrefs('homo_sapiens','BRCA2')