import argparse
import datetime
import wolframalpha
from util import tuition_pipe as _tuition_pipe
from util import extract_universities as _extract_universities
import logging
import time
import json

started_at = '{}'.format(datetime.datetime.now())

logging.basicConfig(level=logging.INFO)

logging.basicConfig(
    filename='app.log', filemode='w', 
    format='%(name)s - %(levelname)s - %(message)s'
    )

logging.info( started_at)


def main():
    """
    entry point for running pipelines
    """

    parser = argparse.ArgumentParser(description='Get university tuition fee')
    parser.add_argument(
        '--wolframalpha', 
        dest='wa_app_id', 
        default='None',
        help='Please provide the wolfram alpha app id here'
        )
    
    parser.add_argument(
        '--input', 
        dest='input_file', 
        default='data/input.csv',
        help='Please provide the path to university list'
        )

    parser.add_argument(
        '--output', 
        dest='output_file', 
        default='data/output.csv',
        help='Please provide the path to university list'
        )
    
    parser.add_argument(
        '--start', 
        dest='start_name', 
        default='None',
        help='Start from a certain university'
        )
    parser.add_argument(
        '--sleep', 
        dest='sleep_seconds', 
        default='2',
        help='Time to sleep before start the next university; This is added to prevent the ip from being banned.'
        )

    args = parser.parse_args()
    wa_app_id = args.wa_app_id
    input_file = args.input_file
    output_file = args.output_file
    start_name = args.start_name
    sleep_seconds = int(args.sleep_seconds)

    print('Using wolframalpha app_id: {}'.format(wa_app_id))
    if wa_app_id == 'None':
        raise Exception('Please provide a wolfram alpha app_id using the --wolframalpha option')
    else:
        logging.debug('Using wolframalpha app_id: {}'.format(wa_app_id) )

    if start_name == 'None':
        start_name = None

    try:
        client = wolframalpha.Client(wa_app_id)
    except Exception as ee:
        raise Exception('Could not initialize wolframalpha client: {}'.format(ee) )


    try: 
        uni_list_to_be_queried = _extract_universities(
            input_file, start=start_name
            )
    except Exception as ee:
        raise Exception('Could not extract list of universities: {}'.format(ee) )

    with open(output_file, 'a+') as fp:
        for uni in uni_list_to_be_queried:
            the_tuition = _tuition_pipe(client, uni)
            fp.write(json.dumps(the_tuition) + '\n' )
            logging.info( "{} - {} -  {}".format(
                datetime.datetime.now() , uni, the_tuition) 
                )
            time.sleep(sleep_seconds)


if __name__ == "__main__":

    main()

    # wa_app_id = "" # add your key here to test
    # client = wolframalpha.Client(wa_app_id)
    
    # print(
    #     _tuition_pipe(client, 'Texas A&M University').get('tuition')
    #     )
    
    print('END')