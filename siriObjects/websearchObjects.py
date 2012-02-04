from siriObjects.baseObjects import ClientBoundCommand, AceObject

class WebSearch(ClientBoundCommand):
    def __init__(self, refId=None, aceId=None, query="", provider="Default"):
        super(WebSearch, self).__init__("Search", "com.apple.ace.websearch", aceId, refId)
        self.query = query
        self.provider = provider

    def to_plist(self):
        self.add_property('query')
        self.add_property('provider')
        return super(WebSearch, self).to_plist()