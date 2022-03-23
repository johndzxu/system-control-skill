from mycroft import MycroftSkill, intent_file_handler


class SystemControl(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('control.system.intent')
    def handle_control_system(self, message):
        application = message.data.get('application')

        self.speak_dialog('control.system', data={
            'application': application
        })


def create_skill():
    return SystemControl()

