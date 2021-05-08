import uuid, os
from hotqueue import HotQueue
from redis import StrictRedis

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = StrictRedis(host=redis_ip, port=6379, db=0) # contains all jobs
q = HotQueue("queue", host=redis_ip, port=6379, db=1) # contains job queue
db = StrictRedis(host=redis_ip, port=6379, db=2) # contains data

# Job operations ***********************
def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, status, state, county, start, end, categories):
    if state.title() == 'Usa':
        state = ""
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'sub_region_1': state,
                'sub_region_2': county,
                'start_date': start,
                'end_date': end,
                'interested_categories': str(categories)
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'sub_region_1': state.decode('utf-8'),
            'sub_region_2': county.decode('utf-8'),
            'start_date': start.decode('utf-8'),
            'end_date': end.decode('utf-8'),
            'interested_categories': str(categories).decode('utf-8')
    }

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(state, county, start, end, categories, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, state, county, start, end, categories)
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    return job_dict

def update_job_status(jid, new_status):
    """Update the status of job with job id `jid` to status `status`."""
    rd.hset(_generate_job_key(jid), 'status', new_status)
    
def add_image(jid, image):
    key = _generate_job_key(jid)
    rd.hset(key, 'image', image)

def get_job(jid):
    return rd.hgetall(_generate_job_key(jid))

def get_image(jid):
    job = get_job(jid)
    return job[b'image']

# Database operations *************************

def db_size():
    return db.dbsize()

def add_data_point(key, data):
    db.hmset(key, data)
    return data

def delete_data_point(key):
    db.delete(key)
    
def update_data_point(key, data):
    for k, v in data.items():
        db.hset(key, k, v)

def get_data_point(key):
    row = {k.decode('utf-8'): value.decode('utf-8') for k, value, in db.hgetall(key).items()}
    return row
