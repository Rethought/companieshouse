#!/usr/bin/env python

import sys

from companieshouse import (
    Company,
    CompaniesHouseClient
    )
import settings


if __name__ == '__main__':
    #info = ch.info(sys.argv[1])
    client = CompaniesHouseClient(settings.api_key)
    co = client.company(sys.argv[1])
    print(co.company_name)
#    info = client.search(sys.argv[1])
#    for co in info['items']:
#        print("{}: {}".format(
#            co['company_number'],
#            co['title']))
