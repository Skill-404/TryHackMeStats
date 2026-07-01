import requests
import sys
from datetime import date

print("""
.#############################.
#                             #
# TryHackMe Stats Reporter V2 #
#           Skill404          #
#          01/07/2026         #
#                             #
'#############################'
\n""")

url="https://tryhackme.com/api/v2/public-profile/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

#Check User Exists
def exists(user):
    exists = requests.get(url+"?username="+user, headers=headers).json()
    if exists['status'] == 'error':
        rtn = False
    else:
        rtn = True
    return rtn

def getStats(user):
    print(f"User \"{user}\" confirmed as present. Getting stats...\n")
    print("Stats on " + date.today().strftime("%d/%m/%Y") + "\n")
    
    #Get User Stats
    stats = requests.get(url+"?username="+user, headers=headers).json()
    print("User joined THM on ", stats['data']['dateSignUp'])
    print("Rooms Completed: ",stats['data']['completedRoomsNumber'])

    #Get User Rank
    user_rank = stats['data']['rank']
    ranking = stats['data']['topPercentage']
    print(f"User Rank: {user_rank}")
    print(f"In the top {ranking}%\n")

    #Get List of User Completed Rooms
    print("Rooms Completed:")
    print("Num | Name | Description")
  
    yy = 0
    page = 1
    completed_rooms =[]

    while yy < stats['data']['completedRoomsNumber']:
        completed_rooms.extend(requests.get(url+"completed-rooms?username=" + user + "&limit=100&page=" + str(page), headers=headers).json()['data']['docs'])
        yy+= 100
        page+= 1

    completed_rooms = sorted(completed_rooms, key=lambda x: x['title'])
    xx = 1
    for room in completed_rooms:
        print(f"{xx}|{room['title']}|{room['description']}")
        xx+= 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage is \"python3 THM_StatsV2.py <username>\"")
        sys.exit()
    else:
        if exists(sys.argv[1]):
            getStats(sys.argv[1])
            sys.exit()
        else:
            print(f"User \"{sys.argv[1]}\" not found; exiting")
            sys.exit()
    
