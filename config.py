from pickle import load

with open('data\\POST_ID', 'rb') as psts_ids:
	POST_ID = load(psts_ids)
with open('data\\ROLES', 'rb') as rls:
	ROLES = load(rls)

EXCROLES = {}

HIGHTROLES = [714082027019698207]

MAX_ROLES_PER_USER = 3333
