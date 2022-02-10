from .base import *
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
from configparser import RawConfigParser
config = RawConfigParser()
initfile = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'settings.ini')
config.read(initfile)

if config.get('ENV', 'SETTING_FILE') == "PROSOR.settings.prod":
    from .prod import *
else:
    from .dev import *
     

