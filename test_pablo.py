import pybiwenger
from pybiwenger import Market

pybiwenger.authenticate()

market = Market()
data = market.get_market_data()