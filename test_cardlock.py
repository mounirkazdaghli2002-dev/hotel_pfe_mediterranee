import os

mdb_path = r"C:\Users\LENOVO\Desktop\twinlock pfe\CardLock.mdb"
print(f"Testing with comtypes DAO: {mdb_path}")
print(f"File exists: {os.path.exists(mdb_path)}")

try:
    import comtypes
    from comtypes.client import CreateObject
    
    # Create DAO engine
    print("Creating DAO DBEngine...")
    engine = CreateObject('DAO.DBEngine.120')
    
    # Try different passwords
    passwords = ['jesuishssine', 'Jesuishssine', 'maintenance', 'MAIN', '1234', '']
    
    for pwd in passwords:
        print(f"\nTrying password: '{pwd}'")
        try:
            # DAO OpenDatabase: db.OpenDatabase(name, options, readonly, connect)
            # For password-protected DB: OpenDatabase(path, False, False, ";PWD=password")
            if pwd:
                connect_str = f";PWD={pwd}"
            else:
                connect_str = ""
            
            db = engine.OpenDatabase(mdb_path, False, False, connect_str)
            print(f"SUCCESS with password: '{pwd}'")
            
            # Get table names
            print(f"Tables in database: {db.TableDefs.Count}")
            tables = []
            for i in range(db.TableDefs.Count):
                table_name = db.TableDefs(i).Name
                if not table_name.startswith('MSys'):
                    tables.append(table_name)
            print(f"  Tables: {tables}")
            
            # Try to read data from first table if available
            if tables:
                try:
                    rs = db.OpenRecordset(tables[0])
                    print(f"  Reading {tables[0]}...")
                    count = 0
                    if not rs.EOF:
                        rs.MoveFirst()
                        while not rs.EOF:
                            count += 1
                            rs.MoveNext()
                    print(f"  Records: {count}")
                    rs.Close()
                except Exception as e2:
                    print(f"  Error reading: {e2}")
            
            db.Close()
            break
            
        except Exception as e:
            print(f"  Failed: {str(e)[:60]}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

