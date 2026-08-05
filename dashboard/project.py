import logging
import os
import time
import pandas as pd
from sqlalchemy import create_engine

# Ensure 'logs' folder exists
os.makedirs("logs", exist_ok=True)

# Logging Setup
logging.basicConfig(
    filename="logs/ingestion.dblog",
    level=logging.DEBUG,
    format="%(asctime)s-%(levelname)s-%(message)s",
    filemode="a",
)

# 1. Database Connection Bridge
engine = create_engine("sqlite:///inventory.db")


# 2. Main Data Loading Function (Chunk-by-Chunk Ingestion)
def load_raw_data():
    start = time.time()

    for file in os.listdir("data"):
        if file.endswith(".csv"):
            logging.info(f"Ingesting {file} into DB...")
            print(f"Starting ingestion for: {file}...")

            file_path = os.path.join("data", file)
            table_name = file[:-4]

            # 1 Lakh rows ke chunks me read & write (Safe for 2 Crore+ entries)
            chunksize = 100000

            for i, chunk in enumerate(
                pd.read_csv(file_path, chunksize=chunksize)
            ):
                # Pehla chunk purani table replace karega, agle chunks data append karenge
                mode = "replace" if i == 0 else "append"

                with engine.begin() as connection:
                    chunk.to_sql(
                        table_name, con=connection, if_exists=mode, index=False
                    )

                print(f"Uploaded {(i + 1) * chunksize:,} rows of {file}...")

            print(
                f"✅ Successfully loaded '{file}' as table '{table_name}' into inventory.db\n"
            )

    # Final Timer Calculation
    end = time.time()
    total_time = (end - start) / 60

    logging.info("Ingestion Complete")
    logging.info(f"Total time taken: {total_time:.2f} minutes")
    print(f"🎉 Total time taken: {total_time:.2f} minutes")


if __name__ == "__main__":
    load_raw_data()