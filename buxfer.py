import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class BuxferError(Exception):
  pass

class Buxfer(object):
  URL_BASE = 'https://www.buxfer.com/api'

  def __init__(self, username, password):
    '''Sets up a session, calls login to set token.'''

    self.session = requests.session()
    self.login(username, password)

  def login(self, username, password):
    '''Uses self.username and self.password to acquire and set a token.'''

    login_info = {'userid': username, 'password': password}
    url = '/'.join([self.URL_BASE, 'login.json'])
    response = self.session.get(url, params=login_info)
    self.token = response.json()['response']['token']

  def api_call(self, action='get', endpoint=None, **params):
    '''Make the API call against Buxfer using our login token.  Return the response.'''

    def decode_response(response):
      '''Check the response for errors and unwrap it from its json cocoon. Return the unwrapped
      response dictionary.'''
      if response.status_code == 200:
        response = response.json()
      else:
        print response.content
        raise BuxferError('Received %s status code from server.' % response.status_code)
      if 'response' in response:
        response = response['response']
      else:
        raise BuxferError('No response key in json response from server.')
      if 'status' not in response:
        raise BuxferError('Unable to parse response from server.')
      if response['status'] == 'OK':
        return response
      else:
        raise BuxferError(response['status'])

    if not endpoint:
      raise BuxferError("api_call must have an endpoint")
    else:
      url = '/'.join([self.URL_BASE, endpoint+'.json'])
      logger.debug('api_call: url: %s' % url)
    call_dict = {'token': self.token}
    if params:
      call_dict.update(params)
    logger.debug('api_call: params: %s' % params)
    if action == 'get':
      response = decode_response(self.session.get(url, params=call_dict))
    elif action == 'post':
      response = decode_response(self.session.post(url, params=call_dict))
    else:
      raise BuxferError("api_call action must be 'get' or 'post'")
    logger.debug('api_call: response: %s' % response)
    return response

  def add_transaction(self, txn_txt):
    '''Accepts a txn_txt sms format transaction text and uses self.token to post a new
    transaction.'''

    transaction_info = {'token': self.token, 'format': 'sms', 'text': txn_txt}
    response = self.api_call(action='post', endpoint='add_transaction', **transaction_info)
    return response

  def _transaction_constraints(self, **kwargs):
    '''Accepts several parameters. Enforces Buxfer's limits on which parameters may be passed
    together. The restrictions are as follows:
    * You may pass either a *Name or *Id but not both
    * You may pass a startDate AND and endDate OR a month
    * You may also pass a page parameter to get a specific page of your transaction log.'''

    acceptable_keywords = ['accountName', 'accountId', 'tagName', 'tagId', 'startDate', 'endDate',
        'month', 'budgetName', 'budgetId', 'contactName', 'contactId', 'groupName', 'groupId',
        'page']
    filter_keys = []
    for k, v in kwargs:
      if k not in acceptable_keywords:
        filter_keys.append(k)
    for k in filter_keys:
      del(kwargs[k])
    eitheror = lambda a,b: a in kwargs and b in kwargs
    if eitheror('accountName', 'accountId'):
      raise BuxferError('transactions may have either accountName or accountId but not both')
    if eitheror('tagName', 'tagId'):
      raise BuxferError('transactions may have either tagName or tagId but not both')
    if eitheror('budgetName', 'budgetId'):
      raise BuxferError('transactions may have either budgetName or budgetId but not both')
    if eitheror('contactName', 'contactId'):
      raise BuxferError('transactions may have either contactName or contactId but not both')
    if eitheror('groupName', 'groupId'):
      raise BuxferError('transactions may have either groupName or groupId but not both')
    if (('startDate' in kwargs and not 'endDate' in kwargs) or
       ('endDate' in kwargs and not 'startDate' in kwargs)):
      raise BuxferError('transactions must have both startDate and endDate or neither')
    if eitheror('startDate', 'month'):
      raise BuxferError('transactions may have startDate and endDate or month but not both')
    return kwargs

  def transactions(self, **kwargs):
    '''Returns a transaction log dictionary.'''

    transactions_info = self._transaction_constraints(**kwargs)
    response = self.api_call(endpoint='transactions', **transactions_info)
    return response

  def reports(self, **kwargs):
    '''Returns a reports dictionary.'''

    reports_info = self._transaction_constraints(**kwargs)
    response = self.api_call(endpoint='reports', **reports_info)
    return response

  def accounts(self):
    '''Returns information about your accounts.'''

    response = self.api_call(endpoint='accounts')
    return response

  def loans(self):
    '''Returns information about your loans.'''

    response = self.api_call(endpoint='loans')
    return response

  def tags(self):
    '''Returns information about your tags.'''

    response = self.api_call(endpoint='tags')
    return response

  def budgets(self):
    '''Returns information about your budgets.'''

    response = self.api_call(endpoint='budgets')
    return response

  def reminders(self):
    '''Returns information about your reminders.'''

    response = self.api_call(endpoint='reminders')
    return response

  def groups(self):
    '''Returns information about your groups.'''

    response = self.api_call(endpoint='groups')
    return response

  def contacts(self):
    '''Returns information about your contacts.'''

    response = self.api_call(endpoint='contacts')
    return response
