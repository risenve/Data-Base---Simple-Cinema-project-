# test_queries.py
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# using environment variables for DB connection
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'reportage_db')

#two forms of DATABASE_URL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
DATABASE_URL_SQLALCHEMY = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

print("=" * 60)
print("Testing Database Connection")
print("=" * 60)
print(f"Host: {POSTGRES_HOST}:{POSTGRES_PORT}")
print(f"Database: {POSTGRES_DB}")
print(f"User: {POSTGRES_USER}")
print(f"URL: postgresql://{POSTGRES_USER}:****@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

def test_connection():
    """Test basic database connection"""
    try:
        engine = create_engine(DATABASE_URL_SQLALCHEMY)
        connection = engine.connect()
        print("Connection successful!")
        
        # check existing tables
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        
        tables = [row[0] for row in result]
        
        if tables:
            print(f" Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table}")
        else:
            print(" No tables found in the database")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def test_table_counts():
    """Test counts of records in tables"""
    try:
        engine = create_engine(DATABASE_URL_SQLALCHEMY)
        connection = engine.connect()
        
        print("\n" + "=" * 60)
        print("Testing Table Records")
        print("=" * 60)
        
        # check counts in each table
        tables = ['events', 'correspondent', 'reportage']
        
        for table in tables:
            try:
                result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"{table}: {count} records")
            except Exception as e:
                print(f"⚠️  Error counting {table}: {e}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"Error testing table counts: {e}")
        return False

def test_specific_queries():
    """Test specific queries from the project"""
    try:
        engine = create_engine(DATABASE_URL_SQLALCHEMY)
        connection = engine.connect()
        
        print("\n" + "=" * 60)
        print("Testing Project Queries")
        print("=" * 60)
        
        # check events with high danger level
        print("\n1. Events with high danger level:")
        result = connection.execute(text("""
            SELECT id, place, city, date, danger 
            FROM events 
            WHERE danger = 'high' 
            LIMIT 5
        """))
        
        for row in result:
            print(f"   ID: {row.id}, Place: {row.place}, City: {row.city}, Date: {row.date}, Danger: {row.danger}")
        
        # check correspondents who are operators
        print("\n2. Correspondents who are operators:")
        result = connection.execute(text("""
            SELECT id, name, city, specification, price 
            FROM correspondent 
            WHERE operator = true 
            LIMIT 5
        """))
        
        for row in result:
            print(f"   ID: {row.id}, Name: {row.name}, City: {row.city}, Spec: {row.specification}, Price: {row.price}")
        
        # check json field
        print("\n3. Checking extra_metadata field:")
        result = connection.execute(text("""
            SELECT id, place, extra_metadata->>'attendance' as attendance
            FROM events 
            WHERE extra_metadata IS NOT NULL 
            LIMIT 3
        """))
        
        for row in result:
            print(f"   ID: {row.id}, Place: {row.place}, Attendance: {row.attendance}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"Error testing specific queries: {e}")
        return False

def test_pg_trgm_extension():
    """Check if pg_trgm extension is installed"""
    try:
        engine = create_engine(DATABASE_URL_SQLALCHEMY)
        connection = engine.connect()
        
        print("\n" + "=" * 60)
        print(" Checking PostgreSQL Extensions")
        print("=" * 60)
        
        result = connection.execute(text("""
            SELECT extname, extversion 
            FROM pg_extension 
            WHERE extname = 'pg_trgm'
        """))
        
        extension = result.fetchone()
        
        if extension:
            print(f"pg_trgm extension installed (version: {extension[1]})")
        else:
            print("pg_trgm extension NOT installed")
            print("Run: CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        
        connection.close()
        return extension is not None
        
    except Exception as e:
        print(f"Error checking extensions: {e}")
        return False

def main():
    """Main test function"""
    print("Starting database tests...")
    
    tests = [
        ("Basic Connection", test_connection),
        ("Table Counts", test_table_counts),
        ("Specific Queries", test_specific_queries),
        ("pg_trgm Extension", test_pg_trgm_extension),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"{test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print(" Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n📈 {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n All tests passed! Database is ready.")
    else:
        print(f"\n {total - passed} test(s) failed. Check the errors above.")

if __name__ == "__main__":
    main()