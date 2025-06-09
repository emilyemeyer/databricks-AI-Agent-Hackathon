import json
from datetime import datetime

LOG_PATH = 'agent.log'

def log_event(event_type, details):
    event = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'details': details
    }
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(event) + '\n')

# Optionally, a helper for LLM logs

def log_llm_interaction(prompt, response):
    log_event('llm_interaction', {'prompt': prompt, 'response': response}) 