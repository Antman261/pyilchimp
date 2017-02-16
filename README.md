# pyilchimp
Python wrapper for Mailchimp's 3.0+ API

## Installation

Install via pip:

```
pip install pyilchimp
```

## Usage

### Basic example

First connect to an account:

```
from pyilchimp.mailchimp_manager import MailchimpManager

mc = MailchimpManager(api_key='1qaz2wsx3edc4rfv5tgb667yhn', server='us1')
```

Now we can make requests:

```
campaigns = mc.campaigns.all()

recent_campaigns = mc.campaigns.all(filters={'sort_dir': 'DESC', 'count': 20})
```

### Managers and resources

If you've ever used Django's ORM, Pyilchimp is structured in a similar way. Resources have managers which can find and return objects, such as a CampaignManager finding and returning campaigns. The name of the manager is the lower case pluralised form of each resource and provides a `.get()` and `.all()` method. `get()` can return a single instance when provided an id, while `all()` will return all objects matching a provided filter, or the last 10 by default.

### Mailchimp actions

Mailchimp provides actions that do not fit into standard RESTful API guidelines. Making use of these actions map to methods with the same name for each resource.

```
campaign = mc.campaigns.get('123123123c')
campaign.pause()
```
