import re
def domain_name(url):
    return re.search('(https?://)?(www\d?\.)?(?P<name>[\w-]+)\.', url).group('name')
if __name__ == "__main__":
    print(domain_name("http://www.zombie-bites.com"))