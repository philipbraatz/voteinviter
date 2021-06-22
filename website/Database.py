import sqlite3 as sl

def getInviteLink(userId):
    with sl.connect('burbVote.db') as con:
        con.row_factory = sl.Row
        cur = con.cursor()
        return cur.execute("""SELECT inviteLink FROM elector
                WHERE id = ?;""",(userId,)).fetchone()

def getExisting(userId):
     with sl.connect('burbVote.db') as con:
        cur = con.cursor()
        return cur.execute("""SELECT * FROM elector
                WHERE id = ?;""",(userId,)).fetchone()

def filterResults(byDay=999,byApproved=False):
    with sl.connect('burbVote.db') as con:
        con.row_factory = sl.Row
        cur = con.cursor()
        
        mySQL = """SELECT [name], elector.id,elector.imgUrl as avatar,positive.count as positive, negative.count as negative, vote_date
                FROM elector
            LEFT OUTER JOIN (
                SELECT elector as id,COUNT(*) as count FROM vote
            WHERE yay = 0
                ) AS negative ON negative.id = elector.id
            LEFT OUTER JOIN (
                SELECT elector as id,COUNT(*) as count FROM vote
            WHERE yay = 1
                ) AS positive ON positive.id = elector.id
            WHERE vote_date > datetime('now', ? ) OR elector.isApproved = 1  OR elector.isApproved = ?
            ORDER BY vote_date desc;"""
        
        ret = cur.execute(mySQL,(f"{str(-byDay)}' day'", 1 if byApproved else 0)).fetchone()
        return ret

def getLastVoteResult():
    return filterResults(byDay=7,byApproved=True)
def getLastDayResult():
    return filterResults(byDay=1)

def getCleanHistory():
    return filterResults(byApproved=True)

def getAllHistory():
    return filterResults()