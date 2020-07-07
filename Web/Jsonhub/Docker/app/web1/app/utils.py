import re
def ssrf_check(url ,white_list):
    for i in range(len(white_list)):
        if url.startswith("http://" + white_list[i] + "/"):
            return False
    return True
