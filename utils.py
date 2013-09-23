
def fixTeamDB(teams_db, users_db):

	ok_teams = del_teams = 0
	# loop to update team counts if they're off
	for team in teams_db.find({}):
	    members = 0
	    for user in users_db.find({"team_id":team['id']}):
	        members+=1

	    if (members == 0):
	        yield "delete " + team['id'] + "\n"
	        teams_db.remove({"id": team['id']})
	        del_teams+=1
	    elif (team['size'] - members) != 0:
	        yield team['id'] + ": d" + str(team['size'] - members) + " " + str(members)+ "\n"
	        team['size'] = members
	        teams_db.update({"id": team['id']}, team)
	    else:
	        yield team['id'] + " is OK"+ "\n"
	        ok_teams+=1
	    
	yield str(ok_teams) + " OK teams \n"
	yield str(del_teams) + " DELETED teams"


def createProj(teams_db, users_db, github, proj):

	org = github.get_organization("EECS485")
	req_start = github.rate_limiting[0]
	num_repos = 0
	num_teams = 0
	num_users = 0

	for team in teams_db.find({ "size": { "$ne":0 } }):

		try:
			yield "----------------------\n"
			
			# create github team first
			team_name = "team_"+ team['id']
			if not team.has_key('gh_team'):
				#check if it exists
				g_team = org.create_team(team_name, permission="push")
				num_teams += 1

				# save new github team to db
				team['gh_team'] = g_team.id
				teams_db.update({"id": team['id']}, team)
				yield "created team: " + team_name + " - " + str(g_team.id) + "\n"

			else:
				g_team = org.get_team(team['gh_team'])
				yield "team exists: " + team_name + " - " + str(g_team.id) + "\n"


			repo_name = proj+"_"+team['id']
			if not team.has_key('gh_'+proj):
				# create github repo, add team to it

				gh_repo = org.create_repo(repo_name, team_id=g_team, private=True)
				num_repos += 1

				team['gh_'+proj] = gh_repo.name
				teams_db.update({"id": team['id']}, team)

				yield "  created repo: " + gh_repo.full_name + "\n"

			else:
				#repo exists
				gh_repo = org.get_repo(team['gh_'+proj])
				yield "  repo exists: " + gh_repo.full_name + "\n"

			for user in users_db.find({"team_id":team['id']}):
				# add user
				g_user = github.get_user(user['github'])
				g_team.add_to_members(g_user)
				num_users += 1
				yield "   added user: " + user['github'] + "\n"

		except:
			yield " \n ...problem... \n"
	yield "\n----------------------\n"
	yield "created " + str(num_teams) + " teams \n"
	yield "created " + str(num_repos) + " repos \n"
	yield "added " + str(num_users) + " users \n\n"

	# print info about usage of github
	req_left = github.rate_limiting[0]
	yield "GitHub Requests:\n"
	yield "  used: " + str(req_start - req_left) + "\n"
	yield "  remaining: " +str(req_left)
