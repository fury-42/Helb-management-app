from loguru import logger
import time

class NotificationService:
    @staticmethod
    def send_sms(phone_number: str, message: str):
        """
        Simulates sending an SMS via Africa's Talking gateway.
        In production, this would use the africastalking SDK.
        """
        logger.info(f"Background Task Started: Sending SMS to {phone_number}")
        
        # Simulate network latency
        time.sleep(2) 
        
        # Log success
        logger.success(f"SMS Successfully sent to {phone_number}: {message}")

notification_service = NotificationService()
