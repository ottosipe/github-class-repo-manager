
def fixTeamDB(teams_db, users_db):

	ok_teams = del_teams = 0
	# loop to update team counts if they're off
	for team in teams_db.find({}):
	    members = 0
	    for user in users_db.find({"team_id":team['id']}):
	        members+=1

	    if (members == 0):
	        yield "delete " + team['id'] + "\n"
	        #teams_db.remove({"id": team['id']})
	        del_teams+=1
	    elif (team['size'] - members) != 0:
	        yield team['id'] + ": d" + str(team['size'] - members) + " " + str(members)+ "\n"
	        team['size'] = members
	        #teams_db.update({"id": team['id']}, team)
	    else:
	        yield team['id'] + " is OK"+ "\n"
	        ok_teams+=1
	    
	yield str(ok_teams) + " OK teams \n"
	yield str(del_teams) + " DELETED teams"


def createProj(teams_db, users_db, github):

	org = github.get_organization("EECS485")
	

	for team in teams_db.find({ "id": "ij6l8nkx1or", "size": { "$ne":0 } }):

		yield "----------------------\n"
		
		# create github team first
		team_name = "team_"+ team['id'] 								#TODO: make this pretty? list of uniqs?
		if not team.has_key('gh_team'):
			#check if it exists
			g_team = org.create_team(team_name, permission="push")

			# save new github team to db
			team['gh_team'] = g_team.id
			teams_db.update({"id": team['id']}, team)
			yield "created team: " + team_name + " - " + str(g_team.id) + "\n"

		else:
			g_team = org.get_team(team['gh_team'])
			yield "team exists: " + team_name + " - " + str(g_team.id) + "\n"


		# create github repo, add team to it
		repo_name = "pa_1"+team['id'] 									#TODO: make this pretty too?
		gh_repo = org.create_repo(repo_name, team_id=g_team, private=True)
		yield "  created repo: " + repo_name + "\n"

		for user in users_db.find({"team_id":team['id']}):
			# add user
			g_user = github.get_user(user['github'])
			g_team.add_to_members(g_user)
			yield "   added user: " + user['github'] + "\n"


