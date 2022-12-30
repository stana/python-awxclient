# python-awxclient

AWX python API client.

## Usage

### Client object
```
from awxclient import Client as AWXClient

awx = AWXClient('myawx.example.com', username=..., password=...)
```

Could also provide auth token -
```
awx = AWXClient('myawx.example.com', token=...)
```

By default connections to AWX made via https. If not https prefix protocol to awx host name - 
```
awx = AWXClient('http://myawx.example.com' ...)
```

If don't want to initiate connection while creating client object use login method -
```
awx = AWXClient('myawx.example.com')
awx.login(username=..., password=...)

# or using token
awx.login(token=...)
```

### Fetching data

#### Getting all data
```
awx.applications.get_all()

awx.organizations.get_all()

awx.job_templates.get_all()
```

#### Getting object by ID
```
awx.job_templates.get_by_id(7)
```

#### Fetching object by name
```
awx.job_templates.get_by_name('Demo Job Template')
```

### Launching Job Template
```
job_params = {'name': 'Ringo', 'surname': 'Starr'}
awx.job_templates.launch_job(7, params=job_params}
```
