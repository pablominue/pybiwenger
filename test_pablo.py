import dotenv

import pybiwenger

dotenv.load_dotenv()

pybiwenger.authenticate()

client = pybiwenger.Players()

print(client.get_my_players())