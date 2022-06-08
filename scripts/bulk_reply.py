# first merge the two source files to pair ticket # with macro references
# post a comment on a ticket
# given the ticket number and a reference to which macro to use
# some kind of output file to record any potential edge cases/failures
from base64 import b64encode
from merger import merge_csv_files
import configparser
import requests
import logging
import json
import time
import sys

config = configparser.RawConfigParser()
config.read('./src/auth.ini')
DOMAIN = config['zendesk']['Domain'].strip('"')
AUTH = config['zendesk']['Credentials'].strip('"')

def main(logger,args): 
    print(args)
    user_csv = ('./src/users.csv')
    code_csv = ('./src/codes.csv')
    merge_file = merge_csv_files(user_csv, code_csv)
    for i,request in enumerate(merge_file):
        result = post_comment(ticket_num=str(request[0]), macro=str(request[1]))
        merge_file[i].append(result.status_code)
    print(merge_file)
    return merge_file

def post_comment(ticket_num, macro):
        url = 'https://{}.zendesk.com/api/v2/tickets/update_many.json?ids={}'.format(DOMAIN, ticket_num)
        print("URL, ", url)
        header = {"Authorization": "Basic {}".format(str(b64encode(AUTH.encode('utf-8')))[2:-1]), 'Content-type': 'application/json'}
        print("HEADER, ", header)
        dat = macro_data(macro)
        print("DATA, ", dat)
        try:
            result = requests.put(url, data=json.dumps(dat), headers=header)
            print(result, "\n","=="*15)
            time.sleep(3)          
            return result
        except Exception as e:
            print('Error posting comment', str(e))
            exit()

def macro_data(code): 
    scenario = ("Hi there,\n"
                "Thanks for reaching out and we apologize for the delayed response!\n\n"
                "Here's a new link for the 60-day free trial:\n\n"
                "https://www.crunchyroll.com/welcome/nextlevel?coupon_code="+str(code)+"&campaign=funimation\n\n"
                "If for any reason you should still need assistance with anything please don't hesitate to reach out to us. Thanks and have a great day!")

    formatted = {"ticket": {"assignee": {"id" :399987185412, "email": "daniel.galca@ellation.com"}, "comment": { "body": "{}".format(scenario), "public": True}}} 
    return formatted

if __name__ =="__main__":
    # TODO: set logging level based on input
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    args = sys.argv
    main(logger,args)