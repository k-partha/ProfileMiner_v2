import json
import csv

import utils
import auth
import parameters

from datetime import datetime
from tqdm import tqdm
import tweepy

class search:
    def __init__(self):
        self.twitter_keys, self.api = auth.auth(0)
        
    def search_all(self, query):
        self.saved = 0
        for i in tqdm(range(1, parameters.MAX_PAGES_FOR_USERS+1)):
            self.search(query, i)
            if self.saved >parameters.MAX_USERS_PER_TYPE:
                break
        print("total saved of ",query, self.saved)
        self.users_likes()

    def search(self, query, page=None):
        c = self.check("#"+query, page)
        if c == 1:
            try:
                results = self.api.search_users("#"+query, page=page)
                # utils.parse(results[0])
                self.save_results(query, page, results)
            except Exception as ex:
                print(ex)
                
    def save_results(self, query, page, results):
        updater = utils.update_json("users.json")
        for result in results:
            if result.id_str in updater.data:
                continue
            if self.profile_validity(query, result):
                dic = {
                    result.id_str:{
                        "screen_name":result.screen_name,
                        "name":result.name,
                        "bio":result.description,
                        "MBTI type": query,
                        "page":page,
                        "favorites_count:":result.favourites_count,
                        "statuses_count":result.statuses_count,
                        "follows_count": result.friends_count,
                        "profile_back_url": result.profile_background_image_url,
                        "profile_pic_url": result.profile_image_url,
                        "language": result.lang,
                        "location":result.location,
                        "queried_at":datetime.today()
                        }
                    }
                updater.data.update(dic)
                self.saved+=1
        updater.write()

    def users_likes(self):
        updater = utils.update_json("users_likes.json")
        user_ids_obj = utils.update_json("users.json")
        user_ids = user_ids_obj.data.keys()
        for id in user_ids:
            if id not in updater.data:
                updater.data[id] = {"posts_liked":[], "posts_posted":[]}
        updater.write()

    def check(self, query, page):
        file = utils.update_json("users.json")
        for id in file.data.keys():
            if str(file.data[id]["MBTI type"]) == str(query) and str(file.data[id]["page"]) == str(page):
                print("already queried")
                return 0
        return 1

    def profile_validity(self, query, result):
        query = query.lower()
        name = result.name.lower()
        display_name = result.screen_name.lower()
        description = result.description.lower()

        value = True
        value = value and query not in name and query not in display_name
        value = value and query in description
        value = value and not result.protected

        return value

def main():
    s = search()
    # s.users_likes()
    
    for keyword in parameters.KEYWORDS:
        s.search_all(keyword)

if __name__ == "__main__":
    main()
