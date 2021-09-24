import json
import multiprocessing
from tqdm import tqdm
from multiprocessing import Pool
import auth
import search_users
import utils #twitter.utils as utils
import userLikes #twitter.user_likes as user_likes
import parameters as p

file = utils.update_json("users.json")

def all_users(t):
    print(t)
    index, keyword = t
    count = 0

    user_type = lambda id: file.data[id]["MBTI type"] == keyword

    l = list(filter(user_type, file.data.keys()))[:p.MAX_USERS_PER_TYPE]

    for i, id in enumerate(tqdm(l)):
        app_num = (index%p.NUMBER_OF_PROCESSES)*p.NUMBER_OF_PROCESSES+i%p.NUMBER_OF_APPS_PER_PROCESS
        s = userLikes.user_likes(key_number=app_num, multiprocess=keyword)
        s.all_likes(id)
        count+=1
        if count>p.MAX_USERS_PER_TYPE:
            break

def create_copies():
    s = search_users.search()
    s.users_likes()

    file = utils.update_json("users_likes.json")
    for i in p.KEYWORDS:
        filename = "users_likes"+str(i)+".json"
        duplicate = utils.update_json(filename)
        duplicate.data = file.data
        duplicate.write()

def join_copies():
    file = utils.update_json("users_likes.json")
    for i in range(p.KEYWORDS):
        filename = "users_likes"+str(i)+".json"
        duplicate = utils.update_json(filename)
        

def main():
    indexed_keywords = list(enumerate(p.KEYWORDS))
    create_copies()
    pool = Pool(processes=p.NUMBER_OF_PROCESSES)
    pool.map(all_users, indexed_keywords)
    pool.close()

if __name__ == '__main__':
    main()