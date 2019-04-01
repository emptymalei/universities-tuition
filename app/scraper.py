import argparse
import wolframalpha
from util import tuition_pipe as _tuition_pipe


def main():
    """
    entry point for running pipelines
    """

    # logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Get university tuition fee')
    parser.add_argument(
        '--wolframalpha', 
        dest='wa_app_id', 
        default='None',
        help='Please provide the wolfram alpha app id here'
        )
    
    args = parser.parse_args()
    wa_app_id = args.wa_app_id

    if wa_app_id == 'None':
        raise Exception('Please provide a wolfram alpha app_id using the --wolframalpha option')

    try:
        client = wolframalpha.Client(wa_app_id)
    except Exception as ee:
        raise Exception('Could not initialize wolframalpha client: {}'.format(ee) )

    print(
        _tuition_pipe(client, 'Texas A&M University')
    )



if __name__ == "__main__":

    wa_app_id = "" # add your key here to test
    client = wolframalpha.Client(wa_app_id)
    
    print(
        _tuition_pipe(client, 'Texas A&M University').get('tuition')
        )
    
    print('END')