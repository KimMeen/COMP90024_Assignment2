import sys
import couchdb,
sys.path.append("../util/")
import jsonHarvester
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-n", "--node", dest="node_address", help="The address of the couchDB node")
parser.add_argument("-d", "--database", dest="database_name", help="The name of the couchDB database")
parser.add_argument("-j", "--json", dest="json_file_name", help="The path of the json file")

couch = couchdb.Server(node_address)
jsonHarvester.harvest_json_couchdb(json_file_name, couch, database_name,"../util/aus_regions.json")