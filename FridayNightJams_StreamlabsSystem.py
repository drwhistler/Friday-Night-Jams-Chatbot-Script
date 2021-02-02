import os
import sys
import clr
import time
import random
import datetime
import shutil
clr.AddReference('IronPython.SQLite.dll')
clr.AddReference('IronPython.Modules.dll')

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = 'Friday Night Jams - Singles'
Website = 'https://www.StreamlabsChatbot.com'
Description = 'Friday Night Jams - Singles (!fnjs)'
Creator = 'DrWhistler'
Version = '1.0.0.0'

#---------------------------------------
# Set Variables
#---------------------------------------
m_Response = 'This is a test message'
m_Command = '!fnjs'
m_CooldownSeconds = 10
m_CommandPermission = 'Moderator'
m_CommandInfo = ''

userId = ""

def Init():
 global m_Response
 m_Response = '' 
 return

def Execute(data):
    
    global userId
    userId = data.User.lower()

    if data.IsChatMessage():

        if data.GetParam(0).lower() == m_Command and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):

            if data.GetParam(1).lower() == 'adv':   

                if data.GetParam(2):
                    bonus=True
                    AdvanceChallenger(bonus)
                else:
                    bonus=False
                    AdvanceChallenger(bonus)

            elif data.GetParam(1).lower() == 'out':   
                Knockout()

            elif data.GetParam(1).lower() == 'vote':   

                if data.GetParam(2) == 'open':
                    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\vote.txt','w') as file:
                        file.writelines("1")
                else:
                    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\vote.txt','w') as file:
                        file.writelines("0")

            elif data.GetParam(1).lower() == 'reset':               
                ResetSession()

            else:
                Parent.SendTwitchMessage('/w drwhistler Invalid agurment. !mj \'ch <challenger>\', \'op <opponent> <position>\', \'swap <pos1> <pos2>\', \'adv\', \'out\', \'vote <open or close>\',\'reset\',\'refresh\'.')

        if (data.GetParam(0).lower() == '!red' or data.GetParam(0).lower() == '!blue') and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,'Everyone',m_CommandInfo):
            RecordVote(userId,data.GetParam(0).lower())

        if data.GetParam(0).lower() == '!showvotes' and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,'Everyone',m_CommandInfo):
            ReturnVotes()

        if data.GetParam(0).lower() == '!showscores' and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,'Everyone',m_CommandInfo):
            ReturnScores()

        if data.GetParam(0).lower() == '!showseason' and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,'Everyone',m_CommandInfo):
            ReturnSeason()
    
    return

def Tick():
    return

#####################################

def AdvanceChallenger(bonus):               #C Advance Challenger up the Challenge Tower

    challenger = ''
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\challengerName.txt','r') as file:
        challenger = file.readline().replace('\n','')

    challengeRound=0
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\round.txt','r') as file:
        challengeRound = int(file.readline().replace('\n',''))

    sessionScore=0
    seasonScore=0
    sessionScore = int(ReadSessionScore(challenger))
    seasonScore = int(ReadSeasonScore(challenger))

    if (challengeRound==1):
        if (bonus==True):
            sessionScore=sessionScore+20
            seasonScore=seasonScore+20
        else:
            sessionScore=sessionScore+10
            seasonScore=seasonScore+10

    if (challengeRound==2):
        if (bonus==True):
            sessionScore=sessionScore+40
            seasonScore=seasonScore+40
        else:
            sessionScore=sessionScore+20
            seasonScore=seasonScore+20

    if (challengeRound==3):
        if (bonus==True):
            sessionScore=sessionScore+60
            seasonScore=seasonScore+60
        else:
            sessionScore=sessionScore+30
            seasonScore=seasonScore+30

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreSession\\' + challenger + '.txt','w') as file:
        file.writelines(str(sessionScore))
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreSeason\\' + challenger + '.txt','w') as file:
        file.writelines(str(seasonScore))
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\challengerPoints.txt','w') as file:
        file.writelines(str(sessionScore))

    UpdateSessionLeaderboard(challenger,sessionScore)    
    UpdateSeasonLeaderboard(challenger,seasonScore)    

    ShowSplatter('opponent',challengeRound)

    if (challengeRound==3):

        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\challengeMaster.txt','w') as file:
            file.writelines("Challenge Master")
    
        if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\challengeMasters\\' + challenger + '.txt'):
            with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\challengeMasters\\' + challenger + '.txt','r') as file:
                line=file.readline().replace('\n','')
                count=int(line)+1
        else:
            count=1

        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\challengeMasters\\' + challenger + '.txt','w') as file:
            file.writelines(str(count))

    else:
        challengeRound=challengeRound+1

        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\round.txt','w') as file:
            file.writelines(str(challengeRound))

    ScoreVotes('red')

    return

def Knockout():                             #C When challenger is defeated by his opponent, the opponent scores +10

    challengeRound = ''
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\round.txt','r') as file:
        challengeRound = file.readline().replace('\n','')

    ScoreVotes('blue')
    ShowSplatter('challenger',challengeRound)

    return

def ResetSession():                         #C Reset Session

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSession\\leaderboard.txt','w') as file:
        file.writelines("")        
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSession\\names.txt','w') as file:
        file.writelines("")        
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSession\\scores.txt','w') as file:
        file.writelines("")        

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardVoting\\leaderboard.txt','w') as file:
        file.writelines("")        
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardVoting\\names.txt','w') as file:
        file.writelines("")        
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardVoting\\scores.txt','w') as file:
        file.writelines("")        

    folder = 'C:/Users/Jason/AppData/Roaming/AnkhHeart/AnkhBotR2/Services/Scripts/DiscJamFNJ/scoreSession'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

    folder = 'C:/Users/Jason/AppData/Roaming/AnkhHeart/AnkhBotR2/Services/Scripts/DiscJamFNJ/scoreVoting'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

    return

#####################################

def RecordVote(user,color):                 #C Record users vote if voting is open

    votes=[]
    voteStatus=0
    voteFound=False

    challenger = ''
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\challengerName.txt','r') as file:
        challenger = file.readline().replace('\n','')

    opponent=''
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\round.txt','r') as file:
        challengeRound = file.readline().replace('\n','')
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\opponent' + str(challengeRound) + '.txt','r') as file:
        opponent = file.readline().replace('\n','')


    if (user != challenger) and (user != opponent):
        
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\vote.txt','r') as file:
            voteStatus = file.readline().replace('\n','')

        if (voteStatus=='1'):

            # Get current votes
            with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\votes.txt','r') as file:
                line = file.readline().replace('\n','')
                while (line != ''):
                    votes.append(line)
                    line = file.readline().replace('\n','')

            # Check if user has already voted
            for vote in votes:
                if (user == vote.split(',')[0]):
                    voteFound=True

            if (voteFound==False):
                if (color=='!red'):
                    votes.append(user + ',red')
                else:
                    votes.append(user + ',blue')

                with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\votes.txt','w') as file:
                    for vote in votes:
                        file.writelines( str(vote + '\n') )

    return

def ReturnVotes():                          #C Return current voting leaders    

    votingLeaders=[]
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardVoting\\leaderboard.txt','r') as file:
        contestant = file.readline().replace('\n','')
        while (contestant != ''):
            votingLeaders.append(contestant)
            contestant = file.readline().replace('\n','')
                
    if (len(votingLeaders) == 0):
        Parent.SendTwitchMessage('No votes have been casted or tallied yet, try again after the next match has concluded.')
    else:

        message = "Voting Leaders: "
        for vote in votingLeaders:    
            message = message + vote.split(',')[0] + '(' + vote.split(',')[1] + ') '
        Parent.SendTwitchMessage(message)

    return

def ReturnScores():                         #C Return current session scoring leaders

    scoringLeaders=[]
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSession\\leaderboard.txt','r') as file:
        contestant = file.readline().replace('\n','')
        while (contestant != ''):
            scoringLeaders.append(contestant)
            contestant = file.readline().replace('\n','')
                
    if (len(scoringLeaders) == 0):
        Parent.SendTwitchMessage('No scores have been tallied yet, try again after the next match has concluded.')
    else:

        message = "Scoring Leaders: "
        for score in scoringLeaders:    
            message = message + score.split(',')[0] + '(' + score.split(',')[1] + ') '
        Parent.SendTwitchMessage(message)

    return

def ReturnSeason():                         #C Return every challengers season scoring results

    scoringLeaders=[]
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSeason\\leaderboard.txt','r') as file:
        contestant = file.readline().replace('\n','')
        while (contestant != ''):
            scoringLeaders.append(contestant)
            contestant = file.readline().replace('\n','')
                
    if (len(scoringLeaders) == 0):
        Parent.SendTwitchMessage('No scores have been tallied yet, try again after the next match has concluded.')
    else:

        message = "Season Leaders: "
        for score in scoringLeaders:    
            message = message + score.split(',')[0] + '(' + score.split(',')[1] + ') '
        Parent.SendTwitchMessage(message)

    return

def ScoreVotes(color):                      #C Process all votes (+5 for correct vote, -3 for wrong vote) and update all players voting results and leaderboard

    votes=[]
    m_Response1 = '+5 Points awarded to: '
    m_Response2 = '-3 Points forfeited from: '

    if (color == "red"):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreVoting\\redVoteResult.txt','w') as file:
            file.writelines('+5')
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreVoting\\blueVoteResult.txt','w') as file:
            file.writelines('-3')
    else:
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreVoting\\blueVoteResult.txt','w') as file:
            file.writelines('+5')
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreVoting\\redVoteResult.txt','w') as file:
            file.writelines('-3')

    # Get current votes
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\votes.txt','r') as file:
        line = file.readline().replace('\n','')
        while (line != ''):
            votes.append(line)
            line = file.readline().replace('\n','')

    redString=""
    blueString=""
    
    for vote in votes:

        if ( str(vote.split(',')[1]) == "red"):
            redString = redString + str(vote.split(',')[0]) + '\n'
        else:
            blueString = blueString + str(vote.split(',')[0]) + '\n'

        # Retrieve users session voting score
        if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreVoting\\' + vote.split(',')[0] + '.txt'):
            with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreVoting\\' + vote.split(',')[0] + '.txt','r') as file:
                line = file.readline().replace('\n','')
                votingScore = int(line)
        else:
            votingScore = 0

        if (color == vote.split(',')[1]):
            m_Response1 = m_Response1 + vote.split(',')[0] + ' '
            votingScore=votingScore+5
        else:
            m_Response2 = m_Response2 + vote.split(',')[0] + ' '
            votingScore=votingScore-3

        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreVoting\\' + vote.split(',')[0] + '.txt','w') as file:
            file.writelines(str(votingScore))

        UpdateVotingLeaderboard(vote.split(',')[0],votingScore)    

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreVoting\\redVoters.txt','w') as file:
        file.writelines(redString)
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreVoting\\blueVoters.txt','w') as file:
        file.writelines(blueString)

    Parent.SendTwitchMessage('Voting Results ... ' + m_Response1 + ' and ' + m_Response2)
    
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\votes.txt','w') as file:
        file.writelines("")

    return

#####################################

def UpdateSessionLeaderboard(participant,score):    #C Updates session leaderboard after each match
    
    leaderboard=[]
    participantFound=False

    # Read in session leaderboard
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSession\\leaderboard.txt','r') as file:
        line = file.readline().replace('\n','')
        while (line != ''):
            if (line.split(',')[0] == participant):
                participantFound=True
                leaderboard.append(participant + ',' + str(score))
            else:
                leaderboard.append(line)   
            line = file.readline().replace('\n','')

    if (participantFound==False):
         leaderboard.append(participant + ',' + str(score))

    # Sort session leaderboard    
    for j in range(len(leaderboard)):
        swapped = False
        i = 0
        while i < (len(leaderboard) -1):
            if int(leaderboard[i].split(',')[1]) < int(leaderboard[i+1].split(',')[1]):
                leaderboard[i],leaderboard[i+1] = leaderboard[i+1],leaderboard[i]
                swapped = True
            i = i+1
        if swapped == False:
            break

    # Write new session leaderboard    
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSession\\leaderboard.txt','w') as file:
        for player in leaderboard:
            file.writelines(str(player+'\n'))


    # Write top 5 leaders names to file
    x=0
    string=''
    for player in leaderboard:
        string = string + leaderboard[x].split(',')[0] + '\n'
        x=x+1
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSession\\names.txt','w') as file:
        file.writelines(string)
        
    # Write top 5 leaders scores to file
    x=0
    string=''
    for player in leaderboard:
        string = string + leaderboard[x].split(',')[1] + '\n'
        x=x+1
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSession\\scores.txt','w') as file:
        file.writelines(string)
        
    return

def UpdateSeasonLeaderboard(participant,score):     #C Updates season leaderboard after each match
    
    leaderboard=[]
    participantFound=False

    # Read in season leaderboard
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSeason\\leaderboard.txt','r') as file:
        line = file.readline().replace('\n','')
        while (line != ''):
            if (line.split(',')[0] == participant):
                participantFound=True
                leaderboard.append(participant + ',' + str(score))
            else:
                leaderboard.append(line)   
            line = file.readline().replace('\n','')

    if (participantFound==False):
         leaderboard.append(participant + ',' + str(score))

    # Sort session leaderboard    
    for j in range(len(leaderboard)):
        swapped = False
        i = 0
        while i < (len(leaderboard) -1):
            if int(leaderboard[i].split(',')[1]) < int(leaderboard[i+1].split(',')[1]):
                leaderboard[i],leaderboard[i+1] = leaderboard[i+1],leaderboard[i]
                swapped = True
            i = i+1
        if swapped == False:
            break

    # Write new session leaderboard    
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSeason\\leaderboard.txt','w') as file:
        for player in leaderboard:
            file.writelines(str(player+'\n'))

    # Write top 5 leaders names to file
    x=0
    string=''
    for player in leaderboard:
        string = string + leaderboard[x].split(',')[0] + '\n'
        x=x+1
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSeason\\names.txt','w') as file:
        file.writelines(string)
        
    # Write top 5 leaders scores to file
    x=0
    string=''
    for player in leaderboard:
        string = string + leaderboard[x].split(',')[1] + '\n'
        x=x+1
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardSeason\\scores.txt','w') as file:
        file.writelines(string)
        
    return

def UpdateVotingLeaderboard(participant,score):     #C Updates voting leaderboard after each match
    
    leaderboard=[]
    participantFound=False

    # Read in session leaderboard
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardVoting\\leaderboard.txt','r') as file:
        line = file.readline().replace('\n','')
        while (line != ''):
            if (line.split(',')[0] == participant):
                participantFound=True
                leaderboard.append(participant + ',' + str(score))
            else:
                leaderboard.append(line)   
            line = file.readline().replace('\n','')

    if (participantFound==False):
         leaderboard.append(participant + ',' + str(score))

    # Sort session leaderboard    
    for j in range(len(leaderboard)):
        swapped = False
        i = 0
        while i < (len(leaderboard) -1):
            if int(leaderboard[i].split(',')[1]) < int(leaderboard[i+1].split(',')[1]):
                leaderboard[i],leaderboard[i+1] = leaderboard[i+1],leaderboard[i]
                swapped = True
            i = i+1
        if swapped == False:
            break

    # Write new voting leaderboard    
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardVoting\\leaderboard.txt','w') as file:
        for player in leaderboard:
            file.writelines(str(player+'\n'))


    # Write top 5 leaders names to file
    x=0
    string=''
    for player in leaderboard:
        string = string + leaderboard[x].split(',')[0] + '\n'
        x=x+1
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardVoting\\names.txt','w') as file:
        file.writelines(string)
        
    # Write top 5 leaders scores to file
    x=0
    string=''
    for player in leaderboard:
        string = string + leaderboard[x].split(',')[1] + '\n'
        x=x+1
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\leaderboardVoting\\scores.txt','w') as file:
        file.writelines(string)
        
    return

#####################################

def ReadSessionScore(participant):                  #C Retreives participants current session score

    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreSession\\' + participant + '.txt'):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreSession\\' + participant + '.txt','r') as file:
            x = file.readline().replace('\n','')
    else:
        x = 0

    return x

def ReadSeasonScore(participant):                   #C Retrieves participants current season score

    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreSeason\\' + participant + '.txt'):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\scoreSeason\\' + participant + '.txt','r') as file:
            x = file.readline().replace('\n','')
    else:
        x = 0

    return x

#####################################

def ShowSplatter(player,challengeRound):                     #C Display splatter on loser after each match
    
    if (player=='opponent'):
        if (challengeRound==1):
            shutil.copyfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\images\\opponentSplat1A.png', 'C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\images\\opponentSplat1B.png')

        if (challengeRound==2):
            shutil.copyfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\images\\opponentSplat2A.png', 'C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\images\\opponentSplat2B.png')

        if (challengeRound==3):
            shutil.copyfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\images\\opponentSplat3A.png', 'C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\images\\opponentSplat3B.png')

    return
