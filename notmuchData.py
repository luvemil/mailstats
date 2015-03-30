import notmuch
from notmuch import Database, Query
import re
import numpy as np

class mailDir(Query):
    """Works like Query:
        db = Database(path)
        addr = mailDir(db, pattern).search_addresses()
    """
    def __init__(self, *args, **kwargs):
        super(mailDir, self).__init__(*args, **kwargs)
        self.regexp = re.compile(r".*<(.*)>")

    def define_parser(self, regexp):
        """Use to set a different regexp to find the email address in a
        string."""
        self.regexp = regexp

    def search_addresses(self):
        """Returns an iterator containing the email of the sender of the nth
        matching the string, as in search_messages()."""
        msgs = self.search_messages()
        addresses = map(
            lambda x: self.regexp.sub(r'\1',x.get_header("from")),
            msgs
            )
        return addresses

    def count_addresses(self):
        """Count the number of unique addresses matching the query."""
        addresses = self.search_addresses()
        return len(set(addresses))

class getData(Database):
    """docstring for getData"""
    def __init__(self, *args, **kwargs):
        super(getData, self).__init__(*args, **kwargs)

    def addresses(self):
        addrs = mailDir(self,"*").search_addresses()
        count = {}
        for addr in addrs:
            if addr in count:
                count[addr] += 1
            else:
                count[addr] = 1
        data = np.array(list(count.values()))
        return data

    def mex_in_threads(self):
        threads = mailDir(self,"*").search_threads()
        data = np.array(list(map(
            lambda x: x.get_total_messages(),
            threads
        )))
        return data

    def addresses_in_threads(self):
        threads = mailDir(self,"*").search_threads()
        data = []
        for thread in threads:
            data.append(
                mailDir(self,
                        "thread:"+thread.get_thread_id()).count_addresses()
            )
        return np.array(data)
