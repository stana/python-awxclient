from awxclient import base
from awxclient import connection
from awxclient import exception

API_VER = 'v2'

class Client(object):

    def __init__(self, awx_host, username=None, password=None, token=None, api_ver=None, verify=False):
        base_url = awx_host
        if not awx_host.startswith("http"):
            base_url = f"https://{awx_host}"
        # default to 'v2' ('.../api/v2/...')
        ver = api_ver or 'v2'
        base_url = f"{base_url}/api/{ver}" 
        self._conn = connection.Connection(base_url, verify=verify)
        if username and password:
            self._conn.login(username=username, password=password)
        elif token:
            self._conn.login(token=token)

    def login(self, username=None, password=None, token=None):
        self._conn.login(username=username, password=password, token=token)

    def logout(self):
        self._conn.logout()

    @property
    def applications(self):
        return ApplicationManager(self._conn)

    @property
    def organizations(self):
        return OrganizationManager(self._conn)

    @property
    def projects(self):
        return ProjectManager(self._conn)

    @property
    def teams(self):
        return TeamManager(self._conn)

    @property
    def job_templates(self):
        return JobTemplateManager(self._conn)

    @property
    def jobs(self):
        return JobManager(self._conn)

    @property
    def job_events(self):
        return JobEventManager(self._conn)


class ApplicationManager(base.BaseManager):
    def __init__(self, conn):
        super(ApplicationManager, self).__init__(conn, 'applications')


class OrganizationManager(base.BaseManager):
    def __init__(self, conn):
        super(OrganizationManager, self).__init__(conn, 'organizations')


class ProjectManager(base.BaseManager):
    def __init__(self, conn):
        super(ProjectManager, self).__init__(conn, 'projects')


class TeamManager(base.BaseManager):
    def __init__(self, conn):
        super(TeamManager, self).__init__(conn, 'teams')


class JobTemplateManager(base.BaseManager):
    def __init__(self, conn):
        super(JobTemplateManager, self).__init__(conn, 'job_templates')

    def launch_job(self, job_template_id, params=None):
        post_json = {
            "extra_vars": params or {}
        }
        return self._conn.post(f"{self._relative_url_base}/{job_template_id}/launch/", json=post_json)


class JobManager(base.BaseManager):
    def __init__(self, conn):
        super(JobManager, self).__init__(conn, 'jobs')

    def is_job_cancellable(self, job_id):
        return self._conn.get(f"{self._relative_url_base}/{job_id}/cancel/")

    def cancel_job(self, job_id):
        return self._conn.post(f"{self._relative_url_base}/{job_id}/cancel/")

    def get_job_events(self, job_id):
        return self._conn.get(f"{self._relative_url_base}/{job_id}/job_events/")

    def get_job_labels(self, job_id):
        return self._conn.get(f"{self._relative_url_base}/{job_id}/labels/")

    def get_job_notifications(self, job_id):
        return self._conn.get(f"{self._relative_url_base}/{job_id}/notifications/")

    def relaunch_job(self, job_id):
        return self._conn.post(f"{self._relative_url_base}/{job_id}/relaunch/")

    def get_job_stdout(self, job_id):
        return self._conn.get(f"{self._relative_url_base}/{job_id}/notifications/")


class JobEventManager(base.BaseManager):
    def __init__(self, conn):
        super(JobEventManager, self).__init__(conn, 'job_events')
