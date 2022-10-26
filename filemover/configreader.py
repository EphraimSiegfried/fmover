from logger import logger


def read():
    categories = [{}]
    f = open("/Users/ephraimsiegfried/PycharmProjects/DownloadsMover/move_config.txt", 'r')
    for line in f.readlines():
        if line.strip() == "END":
            categories.append({})
            continue
        if line in ['\n', '\r\n']:  # is empty line
            continue
        if len(line.split(":")) != 2:
            logger.info("line couldn't be mapped: " + line)
            continue
        (key, value) = line.split(":")
        categories[-1][key] = value.strip()
    if not categories[-1]: # last element is empty
        categories.pop()
    return categories


