from rest_framework.throttling import UserRateThrottle

def create_new_scope(self, request, obj):
    """
        Dynamically creates and applies a throttling scope based on the given object
        and the current HTTP request method.

        The scope is generated in the format:
            "<obj>-<http_method>"

        If the generated scope exists in ``self.THROTTLE_RATES``, this method updates
        the throttle configuration by setting:
            - ``self.scope`` to the new scope
            - ``self.rate`` to the corresponding throttle rate
            - ``self.num_requests`` and ``self.duration`` based on the parsed rate

        Args:
            request (rest_framework.request.Request): The incoming HTTP request.
            obj (str): Base scope name used to construct the throttling scope.

        Returns:
            None
    """
    new_scope = obj +'-' + request.method.lower()
    if new_scope in self.THROTTLE_RATES:
        self.scope = new_scope
        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)

class QuestionThrottle(UserRateThrottle):
    scope = 'question'
    
    def allow_request(self, request, view):
        
        if request.method == "GET":
            return True
        create_new_scope(self, request, 'question')
        
        return super().allow_request(request, view)
    
class AnswerThrottle(UserRateThrottle):
    scope = 'answer'
    
    def allow_request(self, request, view):
        
        if request.method == "GET":
            return True
        create_new_scope(self, request, 'answer')
        
        return super().allow_request(request, view)
    

    