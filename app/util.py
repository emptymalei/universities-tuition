import wolframalpha
import random
import logging
from time import sleep




def flatten_json(y):
    '''Flattens the JSON data
    '''
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '__')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '__')
                i += 1
        else:
            out[name[:-2]] = x

    flatten(y)

    return out


def retry_timer(which_retry, retry_base_interval, mode = None):
    """Calculate a random retry interval

    Args:
        mode(optional, default=None): specify the mode of retry time
            list of possible values: 'random', 'multiply', 'multirand'
    """

    if mode == None:
        mode = 'random'

    if mode == 'random':
        retry_wait_interval = retry_base_interval * random.random()
    elif mode == 'multiply':
        retry_wait_interval = which_retry * retry_base_interval
    elif mode == 'multirand':
        retry_wait_interval = which_retry * retry_base_interval * random.random()

    return {'mode': mode, 'interval': retry_wait_interval, 'retry': which_retry }


def get_query(wa_client, uni_inp):
    
    res_out = wa_client.query(uni_inp)
    
    if res_out.get('@success') == 'true':
        return {
            'success': True, 
            'university': uni_inp, 
            'pod': res_out.get('pod')
        }
    else:
        return {
            'success': False,
            'university': uni_inp,
            'pod': None
        }


def get_tuition_text(wa_pod, key=None):
    
    if key is None:
        key = 'Tuition'
    
    tuition_fee_text = None

    for pod in wa_pod:
        if pod.get('@title') == 'Tuition':
            tuition_fee_text = pod.get('subpod', {}).get('plaintext')
            break
    
    if not tuition_fee_text:
        tuition_fee_text = 'No Data'

    return {'tuition': tuition_fee_text}


def tuition_pipe(wa_client, uni_inp):

    which_retry = 0
    max_retry = 10

    while True and (which_retry < max_retry):
        the_query = get_query(wa_client, uni_inp)
        if the_query.get('success'):
            break
        else:
            which_retry = which_retry + 1
            retry_sleep_time = _retry_timer( which_retry, 5, mode = 'multirand' ).get('interval')
            logging.debug('Retry ({}) in {} seconds.'.format(which_retry, retry_sleep_time), flush=True)
            sleep(retry_sleep_time)

    if not the_query.get('success'):
        raise Exception('Could not get data for: {}'.format(uni_inp), the_query )
        the_tuition_text = {'tuition': 'No Data'}
        pass
    else:
        the_tuition_text = get_tuition_text(the_query.get('pod',{}) )
        
    res = { **the_query, **the_tuition_text }

    return res
