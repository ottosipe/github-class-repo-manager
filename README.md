github-manager
==============

Manage a GitHub Org for project-based classes.

## To Get Going:
- Setup GitHub Organization for your class. [education.github.com](https://education.github.com/)
- Setup a GitHub Application for your org. (You may need two of these, one for test and one for prod)
- Set Authorization callback URL to `http://yourdomain.com/auth` (`localhost:5000/auth` for test)
- Setup a MongoDB instance somewhere. I recommend [compose.io](http://compose.io)' free 512 MB tier.
- Setup `Python` and `pip`. Google for more info.
- Run: `pip install virtualenv` and `gem install foreman` (you may need to `sudo`!)
- Setup `secret.sh`. I provided an example file, rename it
- Edit `.jade` templates as necessary to fit your class/school info

## To Setup:
- `virtualenv venv --distribute`
- `source venv/bin/activate` (run for every new terminal window)
- `pip install -r requirements.txt`

## To Start:
- Set environment variables (run `secret.sh`)
- `foreman start`

## To Deploy:
- I recommend using [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction). This app should be very easy to deploy as is!

## To Use:
- Once setup have all students login! (eg. eecs280signup.com)
- Students can create groups, and use a key to

# Features To Add:
Please submit a pull request if you'd like to add a feature!

- Admin Page (make it more user friendly for staff).
- Delete all projects at class end.
- Project Deadlines (remove students' push changes at a given time).
- Invite by email/link. Allow students to invite others via Email or a easy link.