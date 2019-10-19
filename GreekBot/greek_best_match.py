from GreekBot.greek_logic_adapter import LogicAdapter
from chatterbot import filters

class BestMatch(LogicAdapter):
    """
    A logic adapter that returns a response based on known responses to
    the closest matches to the input statement.

    :param excluded_words:
        The excluded_words parameter allows a list of words to be set that will
        prevent the logic adapter from returning statements that have text
        containing any of those words. This can be useful for preventing your
        chat bot from saying swears when it is being demonstrated in front of
        an audience.
        Defaults to None
    :type excluded_words: list
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.excluded_words = kwargs.get('excluded_words')

    def process(self, input_statement, additional_response_selection_parameters=None):
        search_results = self.search_algorithm.search(input_statement)

        # Use the input statement as the closest match if no other results are found
        closest_match = next(search_results, input_statement)
        print("Closest: ",closest_match.text, closest_match.confidence)
        # Search for the closest match to the input statement
        if closest_match.confidence < self.maximum_similarity_threshold:
            for result in search_results:

                #prints all sentences the input statement approximates
                print(result.text,result.confidence)
                '''
                # Stop searching if a match that is close enough is found
                if result.confidence >= self.maximum_similarity_threshold:
                    closest_match = result
                    break
                '''
                if result.confidence > closest_match.confidence:
                    closest_match = result
                    if result.confidence >= self.maximum_similarity_threshold:
                        break

        #prints the sentence from the ones in the database that is closest to the input statement
        print("Closerest: ",closest_match.id,closest_match.text,closest_match.confidence)

        self.chatbot.logger.info('Using "{}" as a close match to "{}" with a confidence of {}'.format(
            closest_match.text, input_statement.text, closest_match.confidence
        ))

        recent_repeated_responses = filters.get_recent_repeated_responses(
            self.chatbot,
            input_statement.conversation
        )

        for index, recent_repeated_response in enumerate(recent_repeated_responses):
            self.chatbot.logger.info('{}. Excluding recent repeated response of "{}"'.format(
                index, recent_repeated_response
            ))

        response_selection_parameters = {
            'in_response_to': closest_match.text,
    #        'search_in_response_to': closest_match.search_text,
    #        'exclude_text': recent_repeated_responses,
            'exclude_text_words': self.excluded_words
        }

        alternate_response_selection_parameters = {
            'search_in_response_to': self.chatbot.storage.tagger.get_bigram_pair_string(
                input_statement.text
            ),
   #         'exclude_text': recent_repeated_responses,
            'exclude_text_words': self.excluded_words
        }

        if additional_response_selection_parameters:
            response_selection_parameters.update(additional_response_selection_parameters)
            alternate_response_selection_parameters.update(additional_response_selection_parameters)

        # Get all statements that are in response to the closest match
        response_list = list(self.chatbot.storage.filter(**response_selection_parameters))
        print("Possible responses:",response_list)
        alternate_response_list = []

        if not response_list:
            self.chatbot.logger.info('No responses found. Generating alternate response list.')
            alternate_response_list = list(self.chatbot.storage.filter(**alternate_response_selection_parameters))

        if response_list:
            self.chatbot.logger.info(
                'Selecting response from {} optimal responses.'.format(
                    len(response_list)
                )
            )

            for resp in response_list:
                resp.confidence = closest_match.confidence

            #in case of incomplete data we need to use try
            try:
                response = self.select_response(
                    input_statement,
                    response_list,
                    self.chatbot.storage
                )

                print("From response list: ",response.text)
                self.chatbot.logger.info('Response selected. Using "{}"'.format(response.text))
            except:
                response = self.get_default_response()
                print("No response found. Using the default.")
        elif alternate_response_list:
            '''
            The case where there was no responses returned for the selected match
            but a value exists for the statement the match is in response to.
            '''
            self.chatbot.logger.info(
                'Selecting response from {} optimal alternate responses.'.format(
                    len(alternate_response_list)
                )
            )

            for resp in alternate_response_list:
                resp.confidence = closest_match.confidence

            #in case of incomplete data we need to use try
            try:
                response = self.select_response(
                    input_statement,
                    alternate_response_list,
                    self.chatbot.storage
                )

                print("From alternate response list: ", response.text)
                self.chatbot.logger.info('Alternate response selected. Using "{}"'.format(response.text))
            except:
                response = self.get_default_response()
                print("No alternate response found. Using the default.")
        else:
            #in case of no possible responses
            response = self.get_default_response()
            print("No possible answers, saying: ",response.text)

        return response
