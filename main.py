from src.queries.host import find_hosts
from src.helpers.load import load_json
year = '2013'
data = load_json(year)
host_text = "The host(s) for the " + year + " Golden Globes are "
print(host_text + " and ".join(find_hosts(data, year)))