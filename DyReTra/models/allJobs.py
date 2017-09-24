from models.connection import Db


class AllJobs:
    """
        Stores all jobs scheduled by APS for carrying forward
        simulation
    """

    def __init__(self, job_id=None):
        Db.__init__(self)
        self.coll_name = "all_jobs"
        self._exists = False
        self._schema = {
            "job_id": None,  # string
            "cluster_id": None,  # string
            "tl_id": None  # string
        }

        if self.coll_name not in self.db.collection_names():
            self.db.create_collection(self.coll_name)

        if job_id:
            cursor = self.db[self.coll_name].find({"job_id": job_id})
            if cursor.count() == 1:
                self._exists = True
                self._schema = cursor[0]

    def exists(self):
        return self._exists

    def get(self):
        return self._schema

    def create(self, data):
        self.db[self.coll_name].insert_one(data)
        return data['cluster_id']
