import keyss

# Amount pages to explore to find users. (51 is the limit)
MAX_PAGES_FOR_USERS = 51
MAX_USERS_PER_TYPE = 300

# Amount of posts liked by a user to extract.
MAX_PAGES_PER_USER = 20 # 20 posts per page.
MAX_STATUS_PAGES_PER_USER = 30
MAX_FOLLOWS_PAGES_PER_USER = 50

# Keys to authenticate multiple apps
keys = [
    # keyss.keys_dict1
    #     , keyss.keys_dict2,
    # keyss.keys_dict3, keyss.keys_dict4,
     keyss.keys_dict5
    #, keyss.keys_dict6
]

# Multiprocessing settings
NUMBER_OF_PROCESSES = 1
TOTAL_APPS = len(keys)
NUMBER_OF_APPS_PER_PROCESS = int(TOTAL_APPS/NUMBER_OF_PROCESSES)

# Keywords used to search for profiles.
KEYWORDS = [
        #  "INTJ",
        #  "INFJ",
        # "INTP",

        # "ENTP",
        # "ENTJ",
        #
        # "INFP",
        # "ENFP",
        # "ENFJ",
        # "ISFJ",
       # "ESTJ",
        "ESFJ"
        # "ISTP",
        # "ISFP",
        # "ESTP",
        # "ESFP",
        # "ISTJ",
    ]