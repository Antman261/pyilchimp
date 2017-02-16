import requests
import simplejson as json


class MailchimpManager(object):
    def __init__(self, api_key, server, api_version='3.0', auth_user='a'):
        self.api_key = api_key
        self.server = server
        self.api_version = api_version
        self.auth_user = auth_user
        self.campaigns = CampaignManager(self)


class ResourceManager(object):
    def __init__(self, parent):
        self.name = self.__class__.__name__
        self.subject_name = self.name[:-7]
        self.subject_class = globals()[self.subject_name]
        self.path = self.subject_name.lower()+'s'
        self.parent = parent

    def _build_path(self, resource):
        return 'https://{}.api.mailchimp.com/{}/{}'.format(self.parent.server,
                                                           self.parent.api_version,
                                                           resource)

    def _request(self, resource, filters=None, type='GET', post_data={}):
        url = self._build_path(resource)
        if type == 'GET':
            res = requests.get(url, auth=(self.parent.auth_user, self.parent.api_key),
                               params=filters)
            if res.status_code == 200:
                return json.loads(res.text, use_decimal=True)
            print res, url
            return False
        if type == 'POST':
            res = requests.post(url, auth=(self.parent.auth_user, self.parent.api_key),
                                data={})
            return json.loads(res.text)

    def get(self, id_or_resource, filters=None):
        if isinstance(id_or_resource, self.subject_class):
            resource = id_or_resource
            data = self._request(resource, filters)
            return resource._update_with_dict(data)
        else:
            id = id_or_resource
            resource_path = '{}/{}'.format(self.path, id)
            data = self._request(resource_path, filters)
            return self.subject_class(manager=self)._update_with_dict(data)

    def all(self, filters=None):
        data = self._request(self.path, filters)
        key_name = self.subject_name.lower()+'s'
        result_list = []
        for item in data[key_name]:
            result_list.append(self.subject_class(data_dict=item, manager=self))
        return result_list


class CampaignManager(ResourceManager):
    pass


class Resource(object):
    """
    Resources in Mailchimp can be queried, filtered, AND perform actions.
    """
    def __init__(self, id=None, data_dict=None, manager=None):
        self.id = id
        self.name = self.__class__.__name__
        self.manager = manager
        if data_dict is not None:
            self._update_with_dict(data_dict)

    def get_resource_path(self):
        path = self.name.lower()+'s'
        if self.id is not None:
            return '{}/{}'.format(path, self.id)

    def __str__(self):
        return self.get_resource_path()

    def __repr__(self):
        return '<{}: {}>'.format(self.name, str(self))

    def _update_with_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class Campaign(Resource):
    """
    http://developer.mailchimp.com/documentation/mailchimp/reference/campaigns/#
    """
    def __str__(self, human=False):
        if human:
            return self.settings['subject_line'].encode('ascii', 'ignore')
        return self.get_resource_path()

    def pause(self):
        path = '{}/actions/pause'.format(self.get_resource_path())
        self.manager._request(path, type='POST')
