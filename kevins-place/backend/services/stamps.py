"""
Bitcoin Stamps Service
Interacts with Stampchain API to verify SRC-20 token balances.
"""

import httpx
import logging

# Logger
logger = logging.getLogger(__name__)

STAMPCHAIN_API_BASE = "https://stampchain.io/api/v2"

async def get_src20_balance(address: str, ticker: str = "KEVIN") -> float:
    """
    Get SRC-20 token balance for an address.
    
    Args:
        address: Bitcoin address (bc1q...)
        ticker: Token ticker (default: KEVIN)
        
    Returns:
        float: Balance of the token
    """
    try:
        url = f"{STAMPCHAIN_API_BASE}/src20/balance/{address}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            
            if response.status_code == 404:
                return 0.0
                
            response.raise_for_status()
            data = response.json()
            
            # Find our specific token
            for item in data.get('balances', []):
                if item.get('tick', '').upper() == ticker.upper():
                    return float(item.get('amt', 0))
                    
            return 0.0
            
    except Exception as e:
        logger.error(f"Error fetching Stamps balance for {address}: {e}")
        return 0.0

async def verify_kevin_holder(address: str, min_balance: float = 1.0) -> bool:
    """Check if address holds enough KEVIN tokens."""
    balance = await get_src20_balance(address, "KEVIN")
    return balance >= min_balance
