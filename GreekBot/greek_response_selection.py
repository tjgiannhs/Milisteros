"""
Response selection methods determines which response should be used in
the event that multiple responses are generated within a logic adapter.
"""
import logging

def get_heaviest_response(input_statement, response_list, storage=None):
    '''
    Returns the response with the biggest weight from a list of responses

    :param response_list: the responses available to the user's input
    :return: statement with biggest weight
    '''

    from GreekBot.greek_sql_storage import GreekSQLStorageAdapter

    logger = logging.getLogger(__name__)
    logger.info('Selecting response with the biggest weight from list of {} options.'.format(
        len(response_list)
    ))

    sa = GreekSQLStorageAdapter()

    #finding the response with the biggest weight
    heaviest_weight = -1
    for response in response_list:
        response_weight = sa.getWeightFromId(response.id)
        print("Considering ",response.text," with weight of ",response_weight," Confidence: ",response.confidence)
        if response_weight >= heaviest_weight:
            heaviest = response
            heaviest_weight=response_weight

    #if the confidence and the weight are low we prefer giving the default answer instead of a bad response
    if heaviest.confidence*heaviest_weight<0.5:
        from GreekBot.greek_logic_adapter import LogicAdapter
        la = LogicAdapter
        heaviest = la.get_default_response()
        print("Returning default answer")

    return heaviest