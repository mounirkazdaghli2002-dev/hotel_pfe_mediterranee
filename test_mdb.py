import comtypes.client
mdb_path = r'C:\Users\LENOVO\Desktop\Nouveau dossier\CardLock.mdb'
passwords = ['admin', '1234', '12345', 'password', 'master', 'system', 'twinlock', 'TWINLOCK', '']

for pwd in passwords:
    try:
        engine = comtypes.client.CreateObject('DAO.DBEngine.120')
        db = engine.OpenDatabase(mdb_path, False, False, f';PWD={pwd}')
        print(f'SUCCESS with password: {pwd}')
        tables = [db.TableDefs(i).Name for i in range(db.TableDefs.Count)]
        print('Tables:', tables[:5])
        db.Close()
        break
    except Exception as e:
        print(f'Failed with "{pwd}": {str(e)[:40]}')

