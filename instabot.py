#PROJECT : *****INSTABOT***** ! [ ACADVIEW ] ||||| instabot.py
    

'''
Importing REQUEST & URLLIB Libraries
'''
import requests , urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


'''
APP_ACCESS_TOKEN & BASE_URL will be
constant throughout the program
'''
APP_ACCESS_TOKEN = "1344230767.5ece09e.19c0effb0d91426a8dcf382f45351677"
BASE_URL = "https://api.instagram.com/v1/"


'''
Function Used To Get Your Own Information
'''
def self_info() :
    '''
    Create URL
    Request
    If code 200
    Print The Informations
    :return:
    '''
    request_url = (BASE_URL + "users/self/?access_token=%s") %(APP_ACCESS_TOKEN)
    print "GET request URL : %s" %(request_url)
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200 :
        if len(user_info["data"]) > 0:
            print "Username = %s" %(user_info["data"]["username"])
            print "No. Of Followers = %s" %(user_info["data"]["counts"]["followed_by"])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else :
            print "USERNAME does not exist !"
    else :
        print "STATUS CODE NOT 200 !"
        exit()


'''
Function Used To Get Information
Of User By Username
'''
def get_user_info(insta_username) :
    '''
        Create URL
        Request
        If code 200
        Get The Informations
        Print The Information
        :return:
        '''
    user_id = get_user_id(insta_username)
    if user_id == None :
        print "USER DOES NOT EXIST !"
        exit()
    request_url = (BASE_URL + "users/%s?access_token=%s") % (user_id, APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200 :
        if len(user_info["data"]) > 0:
            print "Username: %s" % (user_info["data"]["username"])
            print "No. of followers: %s" % (user_info["data"]["counts"]["followed_by"])
            print "No. of people you are following: %s" % (user_info["data"]["counts"]["follows"])
            print "No. of posts: %s" % (user_info["data"]["counts"]["media"])
        else:
            print "There is no data for this user!"
    else :
        print "STATUS CODE NOT 200 !"


'''
Function Used To Get ID Of User By USERNAME
'''
def get_user_id(insta_username) :
    '''
        Create URL
        Request
        If code 200
        Create ID
        :return:
        '''
    request_url = (BASE_URL + "users/search?q=%s&access_token=%s") %(insta_username ,APP_ACCESS_TOKEN)
    print 'GET request url : %s' %(request_url)
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200 :
        if len(user_info["data"])> 0 :
            return user_info["data"][0]["id"]
        else :
            return None

    else :
        print "STATUS CODE NOT 200 !"
        exit()


'''
Function Used To Get Your Own Recent Post
'''
def get_own_post() :
    '''
        Create URL
        Request
        If code 200
        Post The Informations
        :return:
    '''
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()
    image = []

    if own_media["meta"]["code"] == 200 :
        if len(own_media["data"]) > 0:
            for i in own_media["data"]:
                image.append(
                    {
                        'url': i['images']['standard_resolution']['url'],
                        'name': i['id'] + ".jpeg"
                    }
                )
            for i in image:
                download_image(i)
            return image

            #WE CAN USE THIS CODE TOO FOR DOWNLOADING THE IMAGE !
            '''
            image_name = own_media["data"][0]["id"] + ".jpeg"
            image_url = own_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url,image_name)
            '''
            print "IMAGE DOWNLOADED !"
        else:
            print "POST DOES NOT EXIST !"
    else:
        print "STATUS CODE NOT 200 !"



'''
Function Used To Download Post
'''
def download_image(pic) :
    urllib.urlretrieve(pic['url'], pic['name'])
    print "ALL THE RECENT POST'S DOWNLOADED !"
    return None



'''
Function Used To Get User's Recent Post
'''
def get_user_post(insta_username):
    '''
        Create URL
        Request
        If code 200
        Download Post
        :return:
        '''
    user_id = get_user_id(insta_username)
    if user_id == None :
        print "USER DOES NOT EXIST !"
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media["meta"]["code"] == 200 :
        if len(user_media["data"]) > 0:
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print "POST'S DOWNLOADED !"
        else:
            print "Post does not exist!"
    else:
        print "STATUS CODE NOT 200 !"


'''
Function Used To Get User's Unique ID
'''
def get_post_id(insta_username):
    '''
        Create URL
        Request
        If code 200
        Get Unique ID
        :return:
        '''
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data'])>0:
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'STATUS CODE NOT 200 !'
        exit()


'''
Function Used To Post A Like
'''
def like_a_post(insta_username):
    '''
        Create URL
        Request
        If code 200
        Hit A Like
        :return:
    '''
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes") %(media_id)
    payload = {
        "access_token" : APP_ACCESS_TOKEN
    }
    print "POST URL request : %s" %(request_url)
    post_a_like = requests.post(request_url , payload).json()
    if post_a_like["meta"]["code"] == 200 :
        print "LIKE WAS SUCCESSFULLY POSTED !"
    else:
        print 'Your like was UNSUCCESSFUL . May be Due to the POOR CONNECTION !'


'''
Function Used To Get A Comment List
'''
def get_comment_list(insta_username) :
    '''
        Create URL
        Request
        Pass The Comments In A LIST
        Print
        :return:
        '''
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s") %(media_id ,APP_ACCESS_TOKEN)
    print "GET request URL : %s" %(request_url)
    comment_list = requests.get(request_url).json()

    comments = []
    for i in comment_list["data"]:
        comments.append(i["text"])

    print comments


'''
Function Used To Get A Like List
'''
def get_like_list(insta_username) :
    '''
            Create URL
            Request
            Pass The USER who liked the Post In A LIST
            Print
            :return:
            '''
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes?access_token=%s") %(media_id ,APP_ACCESS_TOKEN)
    print "GET request URL : %s" %(request_url)
    like_list = requests.get(request_url).json()

    users = []
    for i in like_list["data"]:
        users.append(i["username"])

    print users

#WE CAN USE THIS CODE TOO
'''
    if like_list["meta"]["code"] == 200:
        if len(like_list["data"]) >0 :
            print 'Username: %s' % (like_list["data"]["username"])
'''



'''
Function Used To Post A Comment
'''
def post_a_comment(insta_username) :
    '''
            Create URL
            Request
            Post The Comment
            :return:
    '''
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {
        "access_token": APP_ACCESS_TOKEN,
        "text": comment_text
    }
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print "POST request url : %s" % (request_url)

    make_comment = requests.post(request_url , payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"



'''
Function Used To DELETE NEGATIVE Comments
From The Post
'''
def delete_negative_comment(insta_username) :
    '''
            Create URL
            Request
            If code 200
            Use TextBlob
            Differntiate Between Positive & Negative Comments
            Print Whether Positive or Negative
            :return:
    '''
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments/?access_token=%s") % (media_id, APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info["meta"]["code"] == 200:
        if len(comment_info["data"]) > 0:
            for x in range(0, len(comment_info["data"])):
                comment_id = comment_info["data"][x]["id"]
                comment_text = comment_info["data"][x]["text"]
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print "Negative comment : %s" % (comment_text)
                    delete_url = (BASE_URL + "media/%s/comments/%s/?access_token=%s") % (
                    media_id, comment_id, APP_ACCESS_TOKEN)
                    print "DELETE request url : %s" % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info["meta"]["code"] == 200:
                        print "COMMENT SUCCESSFULLY DELETED !\n"
                    else:
                        print "COMMENT DELETION UNSUCCESSFUL , due to POOR CONNECTION!"
                else:
                    print "POSITIVE Comment : %s\n" % (comment_text)
        else:
            print "NO COMMENTS ON THE POST!"
    else:
         print "STATUS CODE NOT 200"



'''
Function To Start The BOT
'''
def start_bot() :



    print "                                                             ------------------------------\n" \
          "                                                             ||                      O    ||\n" \
          "                                                             ||       ___________         ||\n" \
          "                                                             ||      ' ' ------- ' '      ||\n" \
          "                                                             ||    / /            \ \     ||\n" \
          "                                                             ||   / /              \ \    ||\n" \
          "                                                             ||   | |               | |   ||\n" \
          "                                                             ||   | |               | |   ||\n" \
          "                                                             ||    \ \             / /    ||\n" \
          "                                                             ||     ' ' --------- ' '     ||\n" \
          "                                                             ||       ~~~~~~~~~~~~~       ||\n" \
          "                                                              -----------------------------\n" \

    print \
    " .----------------. .-----------------..----------------. .----------------. .----------------. .----------------. .----------------. .----------------. \n"\
    "| .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |\n"\
    "| |     _____    | | | ____  _____  | | |    _______   | | |  _________   | | |      __      | | |   ______     | | |     ____     | | |  _________   | |\n"\
    "| |    |_   _|   | | ||_   \|_   _| | | |   /  ___  |  | | | |  _   _  |  | | |     /  \     | | |  |_   _ \    | | |   .'    `.   | | | |  _   _  |  | |\n"\
    "| |      | |     | | |  |   \ | |   | | |  |  (__ \_|  | | | |_/ | | \_|  | | |    / /\ \    | | |    | |_) |   | | |  /  .--.  \  | | | |_/ | | \_|  | |\n"\
    "| |      | |     | | |  | |\ \| |   | | |   '.___`-.   | | |     | |      | | |   / ____ \   | | |    |  __'.   | | |  | |    | |  | | |     | |      | |\n"\
    "| |     _| |_    | | | _| |_\   |_  | | |  |`\____) |  | | |    _| |_     | | | _/ /    \ \_ | | |   _| |__) |  | | |  \  `--'  /  | | |    _| |_     | |\n"\
    "| |    |_____|   | | ||_____|\____| | | |  |_______.'  | | |   |_____|    | | ||____|  |____|| | |  |_______/   | | |   `.____.'   | | |   |_____|    | |\n"\
    "| |              | | |              | | |              | | |              | | |              | | |              | | |              | | |              | |\n"\
    "| '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |\n"\
    " ----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' \n"\


    print '                                                    -----:::::Hey! Welcome to INSTABOT !:::::-----'
    while True :
        print "\n"
        print '```` MENU OPTION ~~~~~\n'
        print "a. Get Your Own Details"
        print "b. Get Details of a User by Username"
        print "c. Get Your Own Recent Post "
        print "d. Get Recent Post Of User by Username "
        print "e. Like the Recent Post of a User "
        print "f. Get a List of Comments on the Recent Post of a User "
        print "g. Make a Comment on the Recent Post of a User "
        print "h. Delete Negative Comments from the Recent Post of a User "
        print "i. Get a List of People Who have Liked the Recent Post of a User"
        print "j. Exit"



        choice = raw_input("Enter your choice :")
        if choice == "a" :
            self_info()
        elif choice == "b" :
            insta_username = raw_input("Name of User (EXACT SAME As On INSTAGRAM !) :")
            get_user_info(insta_username)
        elif choice =="c" :
            get_own_post()
        elif choice == "d" :
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e" :
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "f" :
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice == "g" :
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "h" :
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "i" :
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice == "j" :
            exit()
        else:
            print "PLEASE TRY AGAIN , YOU ENTERED WRONG CHOICE !"



'''
Function To START OUR SMART INSTA-KIDDO !
'''
start_bot()
