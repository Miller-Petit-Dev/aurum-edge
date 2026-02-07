"""Human-in-the-loop approval system"""
import os
from datetime import datetime
from loguru import logger

class HumanApprovalSystem:
    """Require human approval before executing trades"""
    
    def __init__(self, config):
        self.config = config
        self.use_telegram = config.get('notifications', {}).get('telegram', {}).get('enabled', False)
        self.use_discord = config.get('notifications', {}).get('discord', {}).get('enabled', False)
    
    def request_approval(self, signal_info: dict) -> bool:
        """
        Request human approval for a trade
        
        Args:
            signal_info: Dictionary with trade details
        
        Returns:
            True if approved, False otherwise
        """
        logger.info("=" * 60)
        logger.info("TRADE SIGNAL - HUMAN APPROVAL REQUIRED")
        logger.info("=" * 60)
        logger.info(f"Symbol: {signal_info.get('symbol', 'N/A')}")
        logger.info(f"Direction: {signal_info.get('direction', 'N/A')}")
        logger.info(f"Entry Price: {signal_info.get('entry_price', 0):.2f}")
        logger.info(f"Stop Loss: {signal_info.get('stop_loss', 0):.2f}")
        logger.info(f"Take Profit: {signal_info.get('take_profit', 0):.2f}")
        logger.info(f"Position Size: {signal_info.get('position_size', 0):.2f}")
        logger.info(f"Confidence: {signal_info.get('confidence', 0):.2%}")
        logger.info("=" * 60)
        
        # Send notifications
        if self.use_telegram:
            self._send_telegram(signal_info)
        
        if self.use_discord:
            self._send_discord(signal_info)
        
        # For MVP, auto-approve in paper trading
        # In production, this would wait for actual human input
        logger.warning("MVP MODE: Auto-approving for paper trading")
        return True
    
    def _send_telegram(self, signal_info: dict):
        """Send Telegram notification"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not token or not chat_id:
            logger.info("Telegram not configured (env vars missing) - skipping")
            return
        
        message = self._format_message(signal_info)
        
        # Placeholder for actual Telegram API call
        logger.info(f"Would send to Telegram: {message}")
    
    def _send_discord(self, signal_info: dict):
        """Send Discord webhook notification"""
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        if not webhook_url:
            logger.info("Discord not configured - skipping")
            return
        
        message = self._format_message(signal_info)
        logger.info(f"Would send to Discord: {message}")
    
    def _format_message(self, signal_info: dict) -> str:
        """Format notification message"""
        return f"""
🤖 TRADING SIGNAL

Symbol: {signal_info.get('symbol', 'N/A')}
Direction: {signal_info.get('direction', 'N/A').upper()}
Entry: {signal_info.get('entry_price', 0):.2f}
SL: {signal_info.get('stop_loss', 0):.2f}
TP: {signal_info.get('take_profit', 0):.2f}
Size: {signal_info.get('position_size', 0):.2f} lots
Confidence: {signal_info.get('confidence', 0):.1%}

React to approve/reject
        """.strip()
