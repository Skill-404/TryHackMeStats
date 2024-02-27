import requests
import sys
from datetime import date

print("""
.##########################.
#                          #
# TryHackMe Stats Reporter #
#         Skill404         #
#        27/02/2024        #
#                          #
'##########################'
\n""")

url="https://tryhackme.com/api/"

#Check User Exists
def exists(user):
    exists = requests.get(url+"user/exist/"+user).json()
    return(exists['success'])

def getStats(user):
    print(f"User \"{user}\" confirmed as present. Getting stats...\n")
    print("Stats on " + date.today().strftime("%d/%m/%Y") + "\n")
    
    #Get User Stats
    num_completed = requests.get(url+"no-completed-rooms-public/"+user).json()
    print("Rooms Completed: ",num_completed)

    #Get User Rank
    user_rank = requests.get(url+"user/rank/"+user).json()['userRank']
    site_stats = requests.get(url+"site-stats").json()
    num_of_users = site_stats['totalUsers']
    num_of_ranked_users = site_stats['totalUsersForRanking']
    ranking = round((user_rank / num_of_ranked_users) * 100)
    print(f"User Rank: {user_rank} of {num_of_users} total users")
    print(f"In the top {ranking}%\n")

    #Get List of User Completed Rooms
    print("Rooms Completed:")
    print("Num | Name | Description")
    
    yy = 0
    page = 1
    completed_rooms =[]
    while yy < num_completed:
        completed_rooms = completed_rooms + (requests.get(url+"all-completed-rooms?username=" + user + "&limit=100&page=" + str(page)).json())
        yy+= 100
        page+= 1

    completed_rooms = sorted(completed_rooms, key=lambda x: x['title'])
    xx = 1
    for room in completed_rooms:
        print(f"{xx}|{room['title']}|{room['description']}")
        xx+= 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage is \"python3 THM_Stats.py <username>\"")
        sys.exit()
    else:
        if exists(sys.argv[1]):
            getStats(sys.argv[1])
            sys.exit()
        else:
            print(f"User \"{sys.argv[1]}\" not found; exiting")
            sys.exit()
    
