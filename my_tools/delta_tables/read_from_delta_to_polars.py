import polars as pl
from deltalake import DeltaTable
import os
from rich import print
from rich.progress import Progress
import questionary
from azure.storage.blob import BlobServiceClient

def read_delta_to_polars(storage_account_name, storage_account_key, container_name, delta_table_name):

    full_table_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/{delta_table_name}"

    storage_options = {
        "account_name": storage_account_name,
        "account_key": storage_account_key
    }
    
    try:
        delta_table = DeltaTable(full_table_path, storage_options=storage_options)
        pa_table = delta_table.to_pyarrow_table()
        df = pl.from_arrow(pa_table)
        print(f"Successfully loaded Delta table '{delta_table_name}' into Polars DataFrame.")
        return df
    
    except Exception as e:
        print(f"Error reading Delta table: {str(e)}")
        return None


def initialize_container(storage_account_name, storage_account_key, container_name):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net",
        credential=storage_account_key
    )
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    with Progress() as progress:
        tasks = progress.add_task(f"[cyan]Deleting all contents of the container {container_name}...", total=None, pulse=True)
        for blob in blob_list:
            container_client.delete_blob(blob.name)
            progress.update(tasks, advance=1)
    print(f"Successfully deleted all contents of the container {container_name}.")


if __name__ == '__main__':

    print("[bright_red]Welcome to Delta Tables Tools![/bright_red]")

    with Progress() as progress:
        tasks = progress.add_task("[cyan]Loading Environment Variables...", total=4)
        storage_account_name = os.getenv('DEV_STORAGE_ACCOUNT_NAME', "salakefrandev")
        progress.update(tasks, advance=1)
        storage_account_key = os.getenv('DEV_STORAGE_ACCOUNT_KEY')
        progress.update(tasks, advance=1)
        delta_table_container = os.getenv('DEV_STORAGE_DELTA_CONTAINER', "delta-lake")
        progress.update(tasks, advance=1)
        checkpoints_container = os.getenv('DEV_STORAGE_CHECKPOINTS_CONTAINER', "checkpoints")
        progress.update(tasks, advance=1)

    while True:

        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Read Delta Table to Polars DataFrame",
                "Initialize Development Delta Lake",
                "Initialize Checkpoints",
                "Exit"
            ]
        ).ask()

        if choice == "Initialize Development Delta Lake":
            confirm = questionary.confirm(f"Are you sure you want to delete all contents of the Delta Lake container?\n" +
                                        f"Storage Account: {storage_account_name} \n" + 
                                        f"Container Name: {delta_table_container}").ask()
            if confirm:
                initialize_container(
                    storage_account_name=storage_account_name,
                    storage_account_key=storage_account_key,
                    container_name=delta_table_container
                )
            else:
                continue
        elif choice == "Initialize Checkpoints":
            confirm = questionary.confirm(f"Are you sure you want to delete all contents of the Checkpoints container?\n" +
                                        f"Storage Account: {storage_account_name} \n" + 
                                        f"Container Name: {checkpoints_container}").ask()
            if confirm:
                initialize_container(
                    storage_account_name=storage_account_name,
                    storage_account_key=storage_account_key,
                    container_name=checkpoints_container
                )
            else:
                continue

        elif choice == "Read Delta Table to Polars DataFrame":
            df = read_delta_to_polars(
            storage_account_name=storage_account_name,
            storage_account_key=storage_account_key,
            container_name=delta_table_container,
            delta_table_name="bronze"
        )
            if df is not None:
                print(df.head())
        else:
            print("Exiting...")
            break
