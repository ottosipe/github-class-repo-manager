
# loop to update team counts if they're off
for team in teams_db.find({}):
    members = 0
    for user in users_db.find({"team_id":team['id']}):
        members+=1

    if (members == 0):
        print "delete " + team['id']
        teams_db.remove({"id": team['id']})
    elif (team['size'] - members) != 0:
        print team['id'] + ": d" + str(team['size'] - members) + " " + str(members)
        team['size'] = members
        teams_db.update({"id": team['id']}, team)