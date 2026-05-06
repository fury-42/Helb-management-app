from loguru import logger
import time

class NotificationService:
    def __init__(self):
        # In production, you'd initialize the SDK here:
        # self.username = settings.AT_USERNAME
        # self.api_key = settings.AT_API_KEY
        # africastalking.initialize(self.username, self.api_key)
        # self.sms = africastalking.SMS
        pass

    @staticmethod
    def send_sms(phone_number: str, message: str):
        """
        Sends an SMS via Africa's Talking gateway.
        This runs in a FastAPI BackgroundTask.
        """
        logger.info(f"Background Task: Initiating SMS to {phone_number}")
        
        try:
            # Simulate Africa's Talking SDK call
            # response = self.sms.send(message, [phone_number])
            
            # Artificial delay to simulate network call to AT gateway
            time.sleep(2) 
            
            logger.success(f"SMS Sent Successfully to {phone_number} via Africa's Talking")
            logger.debug(f"SMS Content: {message}")
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
            # In a real app, you might retry or log this to a monitoring service

notification_service = NotificationService()
