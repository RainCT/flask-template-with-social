import json
import traceback

CONFIG_FILE = 'webapp/config.json'

__all__ = ['config']

def fatal(msg):
    stars = '*' * len(msg)
    print '\n%s\n%s\n%s\n' % (stars, msg, stars)
    traceback.print_exc()
    raise SystemExit

try:
    config = json.load(open(CONFIG_FILE))
except Exception:
    fatal('Error parsing configuration file: %s' % CONFIG_FILE)
