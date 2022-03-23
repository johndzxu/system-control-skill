import subprocess, os, re
from mycroft import MycroftSkill, intent_handler


class SystemControl(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.log.info("System Control Skill loaded")

    @intent_handler('ShutDown.intent')
    def handle_shut_down_intent(self, message):
        self.speak_dialog('shutdown')

    @intent_handler('OpenApp.intent')
    def handle_open_app_intent(self, message):
        app_name = message.data.get('app')
        ls = subprocess.run(['ls ~/.local/share/applications/*.desktop'],
                            shell=True,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
        user_apps = ls.stdout.splitlines()
        matches = [app for app in user_apps if app_name in app]
        #print(user_apps)
        #print(sorted(matches, key=len))
        if matches:
            with open(os.path.join('~/.local/share/applications/', sorted(matches, key=len)[0])) as f:
                lines = f.readlines()
                for line in lines:
                    path = re.match(r'^Exec=(.*)', line)
                    if path:
                        self.log.info('Executing ' + path.group(1))
                        launch = subprocess.run('exec ' + path.group(1),
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
                        if not launch.stderr:
                            self.speak_dialog('open.app', data={'app': app_name})
                        else:
                            self.speak(launch.stderr)

        else:
            self.speak('I did not find ' + app_name)


def create_skill():
    return SystemControl()

