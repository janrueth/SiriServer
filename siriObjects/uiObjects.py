from siriObjects.baseObjects import ClientBoundCommand, AceObject

class AddViews(ClientBoundCommand):
    def __init__(self, refId, scrollToTop=False, temporary=False, dialogPhase="Completion", views=None):
        super(AddViews, self).__init__("AddViews", "com.apple.ace.assistant", None, refId)
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
    def __init__(self, requestId=""):
        super(CancelSnippet, self).__init__("CancelSnippet", "com.apple.ace.assistant")
        self.requestId = requestId
    def to_plist(self):
        self.add_property('requestId')
        return super(CancelSnippet, self).to_plist()
class ConfirmSnippet(AceObject):
    def __init__(self, requestId=""):
        super(ConfirmSnippet, self).__init__("ConfirmSnippet", "com.apple.ace.assistant")
        self.requestId = requestId
    def to_plist(self):
        self.add_property('requestId')
        return super(ConfirmSnippet, self).to_plist()

# System objects
class SendCommands(AceObject):
    def __init__(self, commands=None):
        super(SendCommands, self).__init__("SendCommands", "com.apple.ace.system")
        self.commands = commands if commands != None else []
    def to_plist(self):
        self.add_property('commands')
        return super(SendCommands, self).to_plist()
class StartRequest(AceObject):
    def __init__(self, handsFree=False, utterance=""):
        super(StartRequest, self).__init__("StartRequest", "com.apple.ace.system")
        self.handsFree = handsFree
        self.utterance = utterance
    def to_plist(self):
        self.add_property('handsFree')
        self.add_property('utterance')
        return super(StartRequest, self).to_plist()

# Alarm-related objects
class AlarmSnippet(AceObject):                
    def __init__(self, temporary=False, dialogPhase="Completion", alarms=None):
        super(AlarmSnippet, self).__init__("Snippet", "com.apple.ace.alarm")
        self.temporary = temporary
        self.dialogPhase = dialogPhase
        self.alarms = alarms if alarms != None else []
    def to_plist(self):
        self.add_property('temporary')
        self.add_property('dialogPhase')
        self.add_property('alarms')
        return super(AlarmSnippet, self).to_plist()
class AlarmObject(AceObject):
    def __init__(self, identifier=""):
        super(AlarmObject, self).__init__("Object", "com.apple.ace.alarm")
        self.identifier = identifier
    def to_plist(self):
        self.add_property('identifier')
        return super(AlarmObject, self).to_plist()
    
# Event-related objects
class EventSnippet(AceObject):
    def __init__(self, temporary=False, dialogPhase="Confirmation", events=None, confirmationOptions=None):
        super(EventSnippet, self).__init__("EventSnippet", "com.apple.ace.calendar")
        self.temporary = temporary
        self.dialogPhase = dialogPhase
        self.events = events if events != None else []
        self.confirmationOptions = confirmationOptions
    def to_plist(self):
        self.add_property('temporary')
        self.add_property('dialogPhase')
        self.add_property('events')
        self.add_property('confirmationOptions')
        return super(EventSnippet, self).to_plist()
class ExistingEventObject(AceObject):
    def __init__(self, identifier=""):
        super(ExistingEventObject, self).__init__("Event", "com.apple.ace.calendar")
        self.identifier = identifier
    def to_plist(self):
        self.add_property('identifier')
        return super(ExistingEventObject, self).to_plist()
    
# Reminder-related objects
class ReminderSnippet(AceObject):
    def __init__(self, reminders=None, temporary=False, dialogPhase="Confirmation"):
        super(ReminderSnippet, self).__init__("Snippet", "com.apple.ace.reminder")
        self.reminders = reminders if reminders != None else []
        self.temporary = temporary
        self.dialogPhase = dialogPhase
    def to_plist(self):
        self.add_property('reminders')
        self.add_property('temporary')
        self.add_property('dialogPhase')
        return super(ReminderSnippet, self).to_plist()
class ReminderObject(AceObject):
    def __init__(self, dueDateTimeZoneId="America/Chicago", dueDate=None, completed=False, lists=None, trigger=None, subject="", important=False, identifier=""):
        super(ReminderObject, self).__init__("Object", "com.apple.ace.reminder")
        self.dueDateTimeZoneId = dueDateTimeZoneId
        self.dueDate = dueDate
        self.completed = completed
        self.lists = lists if lists != None else []
        self.trigger = trigger if trigger != None else []
        self.subject = subject
        self.important = important
        self.identifier = identifier
    def to_plist(self):
        self.add_property('dueDateTimeZoneId')
        self.add_property('dueDate')
        self.add_property('completed')
        self.add_property('lists')
        self.add_property('trigger')
        self.add_property('subject')
        self.add_property('important')
        self.add_property('identifier')
        return super(ReminderObject, self).to_plist()
class ListObject(AceObject):
    def __init__(self, name = "Tasks"):
        super(ListObject, self).__init__("ListObject", "com.apple.ace.reminder")
        self.name = name
    def to_plist(self):
        self.add_property('name')
        return super(ListObject, self).to_plist()
class DateTimeTrigger(AceObject):
    def __init__(self, date=None):
        super(DateTimeTrigger, self).__init__("DateTimeTrigger", "com.apple.ace.reminder")
        self.date = date
    def to_plist(self):
        self.add_property('date')
        return super(DateTimeTrigger, self).to_plist()

# Note-related objects
class NoteSnippet(AceObject):
    def __init__(self, notes=None, temporary=False, dialogPhase="Summary"):
        super(NoteSnippet, self).__init__("Snippet", "com.apple.ace.note")
        self.notes = notes if notes != None else []
        self.temporary = temporary
        self.dialogPhase = dialogPhase
    def to_plist(self):
        self.add_property('notes')
        self.add_property('temporary')
        self.add_property('dialogPhase')
        return super(NoteSnippet, self).to_plist()
class NoteObject(AceObject):
    def __init__(self, contents="", identifier=""):
        super(NoteObject, self).__init__("Object", "com.apple.ace.note")
        self.contents = contents
        self.identifier = identifier
    def to_plist(self):
        self.add_property('contents')
        self.add_property('identifier')
        return super(NoteObject, self).to_plist()

