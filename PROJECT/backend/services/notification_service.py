import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class NotificationService:
    """Service for sending notifications to users."""
    
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.email = Config.EMAIL_ADDRESS
        self.password = Config.EMAIL_PASSWORD
    
    def send_risk_alert(self, recipient_email, risk_data):
        """Send high-risk alert email."""
        if not Config.ENABLE_NOTIFICATIONS:
            logger.info("Notifications disabled")
            return False
        
        try:
            subject = f"⚠️ Health Risk Alert - {risk_data['overall_risk_level']}"
            
            body = f"""
            Dear User,
            
            Your recent health assessment indicates a {risk_data['overall_risk_level']} risk level.
            
            Primary Concern: {risk_data['primary_concern']}
            
            Risk Scores:
            {self._format_risk_scores(risk_data['risk_scores'])}
            
            Recommendations:
            {self._format_recommendations(risk_data['recommendation'])}
            
            Please seek medical attention if you experience any concerning symptoms.
            
            Best regards,
            Healthcare Risk Detection System
            """
            
            self._send_email(recipient_email, subject, body)
            logger.info(f"Alert sent to {recipient_email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send alert: {str(e)}")
            return False
    
    def _send_email(self, recipient, subject, body):
        """Send email via SMTP."""
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
    
    def _format_risk_scores(self, scores):
        """Format risk scores for email."""
        return '\n'.join([f"  - {disease}: {score*100:.1f}%" 
                         for disease, score in scores.items()])
    
    def _format_recommendations(self, recommendations):
        """Format recommendations for email."""
        if isinstance(recommendations, list):
            return '\n'.join([f"  - {rec}" for rec in recommendations])
        return f"  - {recommendations}"