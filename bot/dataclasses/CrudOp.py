import sqlite3 as sl


@staticmethod
class Crud(object):

    db = None

    @staticmethod
    def SetDB(constr):
        Crud.db = sl.connect(constr)
        Crud.db.row_factory = sl.Row

    @staticmethod
    def GetCursor():
        return Crud.db.cursor()

    @staticmethod
    def GetActiveVote():
        return Crud.GetData(Crud.GetCursor(), """SELECT id FROM elector
            WHERE vote_date >datetime('now','-1 day');""", all=False)

    @staticmethod
    def GetData(sql, variables=None, all=True):

        if(variables is not None and all):
            return Crud.GetCursor().execute(sql, variables).fetchall()
        elif(variables is not None and not all):
            return Crud.GetCursor().execute(sql, variables).fetchone()
        elif(variables is None and all):
            return Crud.GetCursor().execute(sql).fetchall()
        else:
            return Crud.GetCursor().execute(sql).fetchone()

    @staticmethod
    def SetData(sql, variables=None):
        if(variables is not None):
            Crud.GetCursor().execute(sql, variables)
        else:
            Crud.GetCursor().execute(sql)
        Crud.db.commit()
