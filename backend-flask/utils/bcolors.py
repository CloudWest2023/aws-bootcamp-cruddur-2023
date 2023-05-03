class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Print header
def printh(string):
    print(f"{bcolors.HEADER}{bcolors.BOLD}{string}{bcolors.ENDC}\n")

# Print content
def printc(string):
    print(f"{bcolors.OKGREEN}{string}{bcolors.ENDC}\n")

def printe(string):
    print(f"{bcolors.FAIL}{string}{bcolors.ENDC}\n")

# Print SQL
def print_sql(title, sql, params={}):
    print(f"{bcolors.OKCYAN}SQL STATEMENT-[{title}]---------{bcolors.ENDC}\n")
    print(sql, params)

def printb(string):
    print(f"{bcolors.HEADER}{bcolors.BOLD}{string}{bcolors.ENDC}")