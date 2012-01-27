from siriObjects.baseObjects import ClientBoundCommand, AceObject

class PersonSearch(ClientBoundCommand):
    def __init__(self, refId, name="", scope="Local"):
        super(PersonSearch, self).__init__("PersonSearch", "com.apple.ace.contact", None, refId)
        self.name = name
        self.scope = scope
    
    def to_plist(self):
        self.add_property('name')
        self.add_property('scope')
        return super(PersonSearch, self).to_plist()

    
# TODO: Missing objects for use in creating or updating a contact.