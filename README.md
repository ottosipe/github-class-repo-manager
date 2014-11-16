github-class-repo-manager
==============

Manage a project-based class on GitHub! Create group repos for students to use for collaboration and project submission!

## Get Started:
- Setup GitHub Organization for your class. More info: [education.github.com](https://education.github.com/).
- Setup a GitHub Application for your org. (You may need two of these, one for test and one for prod).
- Set Authorization callback URL to `http://yourdomain.com/auth`. (`localhost:5000/auth` for test).
- Setup a MongoDB instance somewhere. I recommend [compose.io](http://compose.io)'s free 512 MB tier.
- Setup `Python` and `pip`. Google for more info.
- Run: `pip install virtualenv` and `gem install foreman` (you may need to `sudo`).
- Setup `secret.sh`. I provided an example file, rename it.
- Edit `.jade` templates as necessary to fit your class/school info.
- Look over the code! You may need to customize group size or other settings.

## To Setup App:
- `virtualenv venv --distribute`
- `source venv/bin/activate` (run for every new terminal window)
- `pip install -r requirements.txt`

## To Start App:
- Set environment variables (run `. secret.sh`)
- `foreman start`

## To Deploy App:
- I recommend using [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction). This app should be very easy to deploy as is!

## To Use:
- Once setup give all students a link to sign up!
- Students can create teams, and use a secret key to invite others.
- Admin Endpoints:
	- Only registered GitHub Organization administrators can use these endpoints.
	- `/create/<project_name>` (eg. `eecs280signup.com/create/proj1`).
		- This will create a repo for each group. (e.g. `proj1_teamid`).
		- If it fails or new students are added, just run it again. It wont hurt existing groups.
	- `/csv` download a `.csv` of all student groups.

# Features To Add:
Please submit a pull request if you'd like to add a feature!

- Admin Page (make it more user friendly for staff).
- Delete all projects at class end.
- Project Deadlines (remove students' push changes at a given time).
- Invite by email/link. Allow students to invite others via Email or a easy link.