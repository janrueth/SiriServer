from siriObjects.baseObjects import ClientBoundCommand, AceObject

class AddViews(ClientBoundCommand):
    def __init__(self, refId, scrollToTop=False, temporary=False, dialogPhase="Completion", views=None, callbacks=None):
        super(AddViews, self).__init__("AddViews", "com.apple.ace.assistant", None, refId, callbacks)
        self.scrollToTop = scrollToTop
        self.temporary = temporary
        self.dialogPhase = dialogPhase
        self.views = views if views != None else []
    
    def to_plist(self):
        self.add_property('scrollToTop')
        self.add_property('temporary')
        self.add_property('dialogPhase')
        self.add_property('views')
        return super(AddViews, self).to_plist()

# Assistant-related objects
class AssistantUtteranceView(AceObject):
    def __init__(self, text="", speakableText="", dialogIdentifier="Misc#ident", listenAfterSpeaking=False):
        super(AssistantUtteranceView, self).__init__("AssistantUtteranceView", "com.apple.ace.assistant")
        self.text = text
        self.speakableText = speakableText
        self.dialogIdentifier = dialogIdentifier
        self.listenAfterSpeaking = listenAfterSpeaking
    def to_plist(self):
        self.add_property('text')
        self.add_property('speakableText')
        self.add_property('dialogIdentifier')
        self.add_property('listenAfterSpeaking')
        return super(AssistantUtteranceView, self).to_plist()

class Button(AceObject):
    def __init__(self, text="", commands=None):
        super(Button, self).__init__("Button", "com.apple.ace.assistant")
        self.text = text
        self.commands = commands if commands != None else []

    def to_plist(self):
        self.add_property('text')
        self.add_property('commands')
        return super(Button, self).to_plist()

class OpenLink(AceObject):
    def __init__(self, ref=""):
        super(OpenLink, self).__init__("OpenLink", "com.apple.ace.assistant")
        self.ref = ref
    
    def to_plist(self):
        self.add_property('ref')
        return super(OpenLink, self).to_plist()


class HtmlView(AceObject):
    def __init__(self, html=""):
        super(HtmlView, self).__init__("HtmlView", "com.apple.ace.assistant")
        self.html = html
    
    def to_plist(self):
        self.add_property('html')
        return super(HtmlView, self).to_plist()

class MenuItem(AceObject):
    def __init__(self, title="", subtitle="", ref="", icon="", commands=None):
        super(MenuItem, self).__init__("MenuItem", "com.apple.ace.assistant")
        self.title = title
        self.subtitle = subtitle
        self.ref = ref
        self.icon = icon
        self.commands = commands if commands != None else []
    
    def to_plist(self):
        self.add_property('title')
        self.add_property('subtitle')
        self.add_property('ref')
        self.add_property('icon')
        self.add_property('commands')
        return super(MenuItem, self).to_plist()


class ConfirmationOptions(AceObject):
    def __init__(self, denyCommands=None, submitCommands=None, confirmText="Confirm", denyText="Cancel", cancelCommands=None, cancelLabel="Cancel", submitLabel="Confirm", confirmCommands=None, cancelTrigger="Deny"):
        super(ConfirmationOptions, self).__init__("ConfirmationOptions", "com.apple.ace.assistant")
        self.denyCommands = denyCommands if denyCommands != None else []
        self.submitCommands = submitCommands if submitCommands != None else []
        self.confirmText = confirmText
        self.denyText = denyText
        self.cancelCommands = cancelCommands if cancelCommands != None else []
        self.cancelLabel = cancelLabel
        self.submitLabel = submitLabel
        self.confirmCommands = confirmCommands if confirmCommands != None else []
        self.cancelTrigger = cancelTrigger
    
    def to_plist(self):
        self.add_property('denyCommands')
        self.add_property('submitCommands')
        self.add_property('confirmText')
        self.add_property('denyText')
        self.add_property('cancelCommands')
        self.add_property('cancelLabel')
        self.add_property('submitLabel')
        self.add_property('confirmCommands')
        self.add_property('cancelTrigger')
        return super(ConfirmationOptions, self).to_plist()

class CancelSnippet(AceObject):
    def __init__(self):
        super(CancelSnippet, self).__init__("CancelSnippet", "com.apple.ace.assistant")
    
class ConfirmSnippet(AceObject):
    def __init__(self):
        super(ConfirmSnippet, self).__init__("ConfirmSnippet", "com.apple.ace.assistant")
    
