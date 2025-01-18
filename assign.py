import pandas as pd
import mysql.connector
from mysql.connector import Error

# MySQL database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "naman@0706"
DB_NAME = "stock_analysis"

def import_stock_data(file_path):
    try:
        # Load the Excel file with parse_dates
        print("Reading Excel file...")
        data = pd.read_excel(file_path, parse_dates=['datetime'])
        
        # Ensure the datetime column is in datetime format
        data['datetime'] = pd.to_datetime(data['datetime'])
        
        # Print sample for verification
        print("\nFirst few rows after date conversion:")
        print(data.head())
        print("\nData types after conversion:")
        print(data.dtypes)
        
        try:
            # Connect to MySQL database
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                print("\nConnected to MySQL database")
                
                # Drop existing table
                cursor.execute("DROP TABLE IF EXISTS stock_data")
                
                # Create new table
                create_table_sql = """
                CREATE TABLE stock_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    datetime DATE,
                    close DECIMAL(10,2),
                    high DECIMAL(10,2),
                    low DECIMAL(10,2),
                    open DECIMAL(10,2),
                    volume BIGINT,
                    instrument VARCHAR(20)
                )
                """
                cursor.execute(create_table_sql)
                print("Created new table")
                
                # Insert data
                insert_sql = """
                INSERT INTO stock_data 
                (datetime, close, high, low, open, volume, instrument)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                # Convert DataFrame to list of tuples
                values = []
                for _, row in data.iterrows():
                    values.append((
                        row['datetime'].to_pydatetime(),  # Convert pandas Timestamp to Python datetime object
                        float(row['close']),
                        float(row['high']),
                        float(row['low']),
                        float(row['open']),
                        int(row['volume']),
                        str(row['instrument'])
                    ))
                
                # Debug information
                print("\nSample value for insertion:")
                print(f"First row to be inserted: {values[0]}")
                print(f"Types of first row: {[type(x) for x in values[0]]}")
                
                # Insert in batches
                batch_size = 1000
                for i in range(0, len(values), batch_size):
                    batch = values[i:i + batch_size]
                    cursor.executemany(insert_sql, batch)
                    connection.commit()
                    print(f"Inserted {len(batch)} records")
                
                print(f"\nSuccessfully inserted all {len(values)} records!")
                
                # Verify the data
                cursor.execute("SELECT COUNT(*) FROM stock_data")
                count = cursor.fetchone()[0]
                print(f"\nTotal records in database: {count}")
                
        except Error as e:
            print(f"\nMySQL Error: {e}")
            print("\nError Details:")
            print(f"Error Code: {e.errno}")
            print(f"SQLSTATE: {e.sqlstate}")
            print(f"Error Message: {e.msg}")
            if 'connection' in locals() and connection.is_connected():
                connection.rollback()
                print("Transaction rolled back due to error")
            
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
                
    except Exception as e:
        print(f"Error during data processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    file_path = "D:/Downloads/HINDALCO_1D.xlsx"
    import_stock_data(file_path)
