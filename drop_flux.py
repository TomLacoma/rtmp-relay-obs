from bdd import *

tout = session.query(Flux).all()

for tou in tout:
    session.delete(tou)
session.commit()
