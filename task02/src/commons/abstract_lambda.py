from abc import ABC, abstractmethod

class AbstractLambda(ABC):
    @abstractmethod
    def handle_request(self, event, context):
        validation_response = self.validate_request(event)
        
        if validation_response:
            return validation_response  # Ensure this has the correct structure (statusCode)
        
        # Return default response in case validation is successful
        return {
            'statusCode': 200,
            'message': 'Hello from Lambda'
        }
