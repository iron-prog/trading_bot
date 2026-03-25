import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

# We will configure the actual file output in logging_config.py later
logger = logging.getLogger(__name__)

class BinanceFuturesClient:
    """A wrapper for the Binance Futures Testnet API."""
    
    def __init__(self, api_key: str, api_secret: str):
        self.base_url = "https://testnet.binancefuture.com" # Required by assignment
        
        try:
            # Initialize the client with testnet=True
            self.client = Client(api_key, api_secret, testnet=True)
            # Force the client to use the futures testnet URL
            self.client.FUTURES_URL = self.base_url 
            logger.info("Successfully initialized Binance API client.")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise

    def check_connection(self) -> bool:
        """Pings the Binance Futures API to test connectivity."""
        try:
            self.client.futures_ping()
            logger.info("Successfully connected to Binance Futures Testnet.")
            return True
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"API connection failed: {e}")
            return False
            
    def get_client(self) -> Client:
        """Returns the raw python-binance client for order placement."""
        return self.client