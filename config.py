def parse_config(filename) -> dict:
    config = {}
    with open(filename) as f:
        for line in f:
            parsed_line = line.split()
            config[parsed_line[0]] = parsed_line[1]
    return config


config = parse_config('/etc/httpd.conf')
# config = parse_config('/home/viktoria/Technopark_3_sem/highload/hw1_polling/httpd.conf')

# SERVER_ADDRESS = ('localhost', 8082)
SERVER_ADDRESS = ('0.0.0.0', int(config["port"]))
ROOT_DIR = config["document_root"]
CPU = int(config["cpu_limit"])
