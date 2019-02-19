from .scoreboard import Scoreboard


# Uses discord bot to find players in match channels
def get_player_discord():
    return False

# Queries AWS Cognito for users' esea profile
def get_player_esea():
    return False

# scans users' profile for ongoing NACCS club matches
def search_club_match():
    return False
    
if __name__ == '__main__':
    print("test")