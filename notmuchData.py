import notmuch
from notmuch import Database, Query
import re

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
