import csv
import multiprocessing

import utils #twitter.utils as utils
import auth #twitter.auth as auth
import parameters as p
from datetime import datetime
from tqdm import tqdm

class user_likes:
    def __init__(self, key_number, multiprocess=None):
        self.twitter_keys, self.api = auth.auth(index=key_number)

        self.filename = "generic.json"
        self.status_name = "generic.json"
        self.follows_name = "generic.json"

        self.filename2 = "users_likes.json"
        self.filename3 = "users_stats.json"
        self.filename4 = "users_follows.json"

        if multiprocess is not None:
            self.filename2 = "users_likes"+str(multiprocess)+".json"
            self.filename3 = "users_stats" + str(multiprocess) + ".json"
            self.filename4 = "users_follows" + str(multiprocess) + ".json"

    def all_likes(self, user_id):
        file = utils.update_json("users.json")
        if user_id in file.data:
            user = file.data[user_id]
            fav_count = user["favorites_count:"]
            stat_count = user["statuses_count"]
            follows_count = user["follows_count"]

            self.filename = user["MBTI type"]+"_likes_records.json"
            self.status_name = user["MBTI type"] + "_stats_records.json"
            self.follows_name = user["MBTI type"] + "_follows_records.json"

        else:
            user = self.api.get_user(id=user_id)
            fav_count = user.favourites_count
            stat_count = user.status_count
            follows_count = user.follows_count

        pages = min(int(fav_count/20), p.MAX_PAGES_PER_USER)
        status_pages = min(int(stat_count/20), p.MAX_STATUS_PAGES_PER_USER)
        follows_pages = min(int(follows_count/20), p.MAX_FOLLOWS_PAGES_PER_USER)

        for page in (range(1, pages)):
            self.likes(user_id, page=page)
        for page in (range(1, status_pages)):
            self.stats(user_id, pages = page)
        for page in (range(1, follows_pages)):
            self.follows(user_id, pages = page)

    def likes(self, user_id, page=1):
        try:
            if self.check(user_id, page):
                results = self.api.favorites(id=user_id, page=page, tweet_mode="extended", trim_user=True)
                self.save_posts(user_id, results)
                self.save_queries(user_id, page)
        except Exception as ex:
            print(ex)

    def stats(self, user_id, pages = 1):
        try:
            if self.check_status(user_id, pages):
                ids = self.api.user_timeline(id=user_id, page=pages, tweet_mode="extended", exclude_replies = True, include_rts = False)
                self.save_stats(user_id, ids)
                self.save_queries_stats(user_id, pages)
        except Exception as ex:
            print(ex)

    def follows(self, user_id, pages = 1):
        try:
            if self.check_follows(user_id, pages):
                ids = self.api.friends(id=user_id, page = pages,  count = 1000)
                self.save_follows(user_id, ids)
                self.save_queries_follows(user_id, pages)
        except Exception as ex:
            print(ex)

    def save_queries(self, user_id, page):
        file_handle = open("user_favs.csv", "a")
        with file_handle as csv_file:
            row = [user_id, page,] #datetime.today()]
            writer = csv.writer(csv_file)
            writer.writerow(row)

    def save_queries_stats(self, user_id, page):
        file_handle = open("user_stats_check.csv", "a")
        with file_handle as csv_file:
            row = [user_id, page,] #datetime.today()]
            writer = csv.writer(csv_file)
            writer.writerow(row)

    def save_queries_follows(self, user_id, page):
        file_handle = open("user_follows_check.csv", "a")
        with file_handle as csv_file:
            row = [user_id, page] #datetime.today()]
            writer = csv.writer(csv_file)
            writer.writerow(row)

    def check(self, user_id, page):
        with open("user_favs.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0:2] == [str(user_id), str(page)]:
                    print("already queried")
                    return False
        return True

    def check_status(self, user_id, page):
        with open("user_stats_check.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0:2] == [str(user_id), str(page)]:
                    print("status already queried")
                    return False
        return True

    def check_follows(self, user_id, page):
        with open("user_follows_check.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0:1] == [str(user_id)]:
                    print("status already queried")
                    return False
        return True

    def save_posts(self, user_id, results):

        updater_posts = utils.update_json(self.filename)
        updater_user  = utils.update_json(self.filename2)
        for result in results:
            if result.id_str in updater_posts.data:
                updater_posts.data[result.id_str]["liked_by"] += [user_id]
                updater_posts.data[result.id_str]["liked_by"] = list(set(updater_posts.data[result.id_str]["liked_by"]))
                continue
            
            hashtags = [hashtag["text"] for hashtag in result.entities["hashtags"]] if "hashtags" in result.entities else []
            media = [media["media_url_https"] for media in result.entities["media"]] if "media" in result.entities else []
            
            dic = {
                result.id_str:{
                    "creator_id": result.user.id,
                    "created_at":result.created_at,
                    "liked_by": [user_id],
                    "text": result.full_text,
                    "hashtags": hashtags,
                    "media": media}
                    }
                    
            updater_posts.data.update(dic)

            if user_id in updater_user.data:
                updater_user.data[user_id]["posts_liked"]+=[result.id_str]
                updater_user.data[user_id]["posts_liked"] = list(set(updater_user.data[user_id]["posts_liked"]))
        updater_posts.write()
        updater_user.write()

    def save_stats(self, user_id, results):

        updater_posts = utils.update_json(self.status_name)
      #  updater_user = utils.update_json(self.filename3)
        for result in results:

            hashtags = [hashtag["text"] for hashtag in
                        result.entities["hashtags"]] if "hashtags" in result.entities else []
            media = [media["media_url_https"] for media in
                     result.entities["media"]] if "media" in result.entities else []

            dic = {
                result.id_str: {
                    "creator_id": result.user.id,
                    "created_at": result.created_at,
                    "text": result.full_text,
                    "retweets": result.retweet_count,
                    "likes": result.favorite_count,
                    "hashtags": hashtags,
                    "media": media,
                    "lang": result.lang,
                }
            }

            updater_posts.data.update(dic)

        updater_posts.write()
       # updater_user.write()

    def save_follows(self, user_id, results):

        updater_posts = utils.update_json(self.follows_name)
        updater_user = utils.update_json(self.filename4)
        for result in results:

            if result.id_str in updater_posts.data:
                updater_posts.data[result.id_str]["followed_by"] += [user_id]
                updater_posts.data[result.id_str]["followed_by"] = list(set(updater_posts.data[result.id_str]["followed_by"]))
                continue

            dic = {

                result.id_str: {
                    "followed_by": [user_id],
                    "screen_name": result.screen_name,
                    "name": result.name,
                    "bio": result.description,
                    "favorites_count:": result.favourites_count,
                    "statuses_count": result.statuses_count,
                    "follows_count": result.friends_count,
                    "profile_back_url": result.profile_background_image_url,
                    "profile_pic_url": result.profile_image_url,
                    "language": result.lang,
                    "queried_at": datetime.today()
                }
            }
            updater_posts.data.update(dic)

            if user_id in updater_user.data:
                updater_user.data[user_id]["follows"] += [result.id_str]
                updater_user.data[user_id]["follows"] = list(set(updater_user.data[user_id]["follows"]))
        updater_posts.write()
        updater_user.write()

def main():
    file = utils.update_json("users.json")
    for i,id in enumerate(tqdm(file.data.keys())):
        s = user_likes(key_number=i%4)
        s.all_likes(id)

if __name__ == "__main__":
    main()