# Companies House API wrapper
import requests


BASE_URL = "api.companieshouse.gov.uk"


class CompaniesHouseRequestError(Exception):
    pass


class CompaniesHouseClient(object):
    """
    Class to wrap operations against the Companies House API
    """
    def __init__(self, api_key):
        """
        Initialise the client with the API key. The key is not validated.
        """
        self.api_key = api_key

    def _request(self, uri, params={}):
        """
        Perform the actual request to Companies House.
        """
        url = "https://{}/{}".format(BASE_URL, uri)
        r = requests.get(url, auth=(self.api_key, ''), params=params)
        if r.status_code != 200:
            raise CompaniesHouseRequestError(
                "Response: {}: {}".format(r.status_code, r.reason))
        return r.json()


    def company(self, company_number):
        """
        Return data on company `company_number`.  Returns a Company object.

        @todo: lots, but crucially raise CompanyNotFoundError if so
        """

        # Number needs to be 8 digits, zero padded for companies house.
        # Accommodate argument being either string or integer
        company_number = "{}".format(company_number).zfill(8)
        return Company(self._request('company/{}'.format(company_number)))


    def search(self, search_term):
        """
        Search the companies database with the search term.
        """
        return self._request('search/companies', params={"q": search_term})


class Company(object):
    def __init__(self, json):
        """
        Initialise this Company with JSON response from Companies House.

        Use for convenient access to more company information. Lazily evaluates
        certain properties with subsequent API calls (well, it will do
        shortly...)
        """
        self.details = json

    def __getattr__(self, key):
        if key in self.details:
            return self.details[key]
        else:
            raise AttributeError("'{}' not found in company '{}'"
                                 .format(key, self.details['company_name']))
