import questionary
from rich.console import Console
from rich.progress import Progress
from rich import print
console = Console()
import os
import time
from azure.storage.blob import BlobServiceClient
import zipfile36 as zipfile
from io import BytesIO
import re

class CombinedUnzipper():
    def __init__(self, blob_name, blob_data):
        self.blob_name = blob_name
        self.blob_data = blob_data
        self.log_name = None
        self.log_data = None
        self.unzip_largest_combined_log()

    def unzip_largest_combined_log(self):
        largest_file = None
        largest_size = 0
        with zipfile.ZipFile(BytesIO(blob_data), 'r') as zip_ref:
            for info in zip_ref.infolist():
                if 'Combined' in info.filename and info.filename.endswith('.txt'):
                    if info.file_size > largest_size:
                        largest_file = info.filename
                        largest_size = info.file_size

        if largest_file is None:
            print("[bright_red]No combined log files found in the zip file[/bright_red]")

        sn = self.blob_name.split('/')[0]
        combined_date = re.search(r'\d{4}-\d{2}-\d{2}', largest_file).group(0)
        self.log_name = f"{combined_date}_combined_{sn}.txt"

        with zipfile.ZipFile(BytesIO(blob_data), 'r') as zip_ref:
            with zip_ref.open(largest_file) as file:
                self.log_data = file.read()
    


class StorageAccountHandler:
    def __init__(self, account_name, account_key, container_name):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.connect_to_storage_account()

    def connect_to_storage_account(self):
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{self.account_name}.blob.core.windows.net",
            credential=self.account_key
        )
        self.container_client = self.blob_service_client.get_container_client(self.container_name)


    def download_blob_to_memory(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob().readall()
        return blob_data

    def upload_blob(self, blob_name, data):
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)

    def get_blobs_by_sn_and_date(self, target_sn=None, target_date=None, max_results=None):
        if not target_date:
            target_date = time.strftime("%y%m%d", time.localtime(time.time() - 30*24*60*60))
        logs_for_date = []

        if max_results is not None:
            max_results = int(max_results)

        serial_numbers = [target_sn] if target_sn else range(2001, 7001)

        for sn in serial_numbers:
            prefix = f'h19{sn}/AllLogs-H19{sn}-NDS-WKS-SN{sn}-{target_date}'
            try:
                blobs = self.container_client.list_blobs(name_starts_with=prefix)
                regex_pattern = f"{prefix}-.*\\.zip"
                for blob in blobs:
                    if re.match(regex_pattern, blob.name):
                        logs_for_date.append(blob.name)
                        if max_results is not None and len(logs_for_date) >= max_results:
                            return logs_for_date
            except Exception as e:
                print(f"Error retrieving blobs for SN {sn}: {e}")
        
        return logs_for_date


if __name__ == "__main__":
    print("[bright_red]Welcome to Combined Log Tools![/bright_red]")

    with Progress() as progress:
        tasks = progress.add_task("[cyan]Loading Environment Variables...", total=6)
        vida_logs_account_name = os.getenv("VIDA_STORAGE_ACCOUNT_NAME")
        progress.update(tasks, advance=1)
        vida_logs_account_key = os.getenv("VIDA_STORAGE_ACCOUNT_KEY")
        progress.update(tasks, advance=1)
        vida_logs_container_name = os.getenv("VIDA_STORAGE_CONTAINER_NAME")
        progress.update(tasks, advance=1)
        dev_storage_account_name = os.getenv("DEV_STORAGE_ACCOUNT_NAME")
        progress.update(tasks, advance=1)
        dev_storage_account_key = os.getenv("DEV_STORAGE_ACCOUNT_KEY")
        progress.update(tasks, advance=1)
        dev_container_name = os.getenv("DEV_STORAGE_LOGS_CONTAINER")
        progress.update(tasks, advance=1)

    with Progress() as progress:
        task = progress.add_task("[cyan]Connecting to Azure Storage Account", total=2)
        vida_logs_handler = StorageAccountHandler(vida_logs_account_name, vida_logs_account_key, vida_logs_container_name)
        progress.update(task, advance=1)
        dev_handler = StorageAccountHandler(dev_storage_account_name, dev_storage_account_key, dev_container_name)
        progress.update(task, advance=1)
    
    print(f"\n[bright_green]Source:[/bright_green] [white]{vida_logs_account_name}:{vida_logs_container_name}[/white]")
    print(f"[bright_green]Destination:[/bright_green] [white]{dev_storage_account_name}:{dev_container_name}[/white]\n")

    while True:
        main_menu_choices = [
            f"Unzip single log.",
            f"Unzip many logs.",
            f"Exit"
        ]
        
        choice = questionary.select("Select an option", choices=main_menu_choices).ask()
        if choice in ["Unzip single log.", "Unzip many logs."]:
            output = questionary.select("Unzip single log. Choose a destination:", 
                                        choices=["Download local", 
                                                    f"Upload to  {dev_storage_account_name}:{dev_container_name}",
                                                    "Cancel and go back"]).ask()
            if output == "Cancel and go back":
                print("[bright_yellow]Going back to main menu[/bright_yellow]")
                continue
            else:
                if output == "Download local":
                    download_local = True
                else:
                    download_local = False

        if  choice == "Unzip single log.":
            sn = questionary.text("Enter Serial Number (2001-7000)").ask()
            if not sn.isdigit() or int(sn) < 2001 or int(sn) > 7000:
                print("[bright_red]Invalid Serial Number[/bright_red]")
                continue
            date = questionary.text("Enter Date (YYMMDD)").ask()
            if not re.match(r'\d{6}', date):
                print("[bright_red]Invalid Date[/bright_red]")
                continue
            blob_names = vida_logs_handler.get_blobs_by_sn_and_date(target_sn=sn, target_date=date, max_results=15)
            if not blob_names:
                print("[bright_red]No logs found[/bright_red]")

            else:
                blob_names.append("Go Back")
                print(f"[bright_yellow]Found {len(blob_names)-1} logs[/bright_yellow]")

            selected_blob = questionary.select("Select a log to unzip", choices=blob_names).ask()
            if selected_blob == "Go Back":
                print("[bright_yellow]Going back to main menu[/bright_yellow]")
            else:
                blob_data = vida_logs_handler.download_blob_to_memory(selected_blob)
                combined_unzipper = CombinedUnzipper(selected_blob, blob_data)
                if download_local:
                    if not os.path.exists("tmp"):
                        os.makedirs("tmp")
                    with open(f"tmp/{combined_unzipper.log_name}", 'wb') as f:
                        f.write(combined_unzipper.log_data)
                    print(f"[bright_green]Log unzipped and saved locally: {combined_unzipper.log_name}[/bright_green]\n")
                else:
                    dev_handler.upload_blob(combined_unzipper.log_name, combined_unzipper.log_data)
                    print(f"[bright_green]Log unzipped and uploaded to Destination: {combined_unzipper.log_name}[/bright_green]\n")

        elif choice == "Unzip many logs.":
            date = questionary.text("Enter Date (YYMMDD)").ask()
            if not re.match(r'\d{6}', date):
                print("[bright_red]Invalid Date[/bright_red]")
                continue
            max_results = questionary.text("Enter max number of logs to unzip").ask()
            if not max_results.isdigit():
                print("[bright_red]Invalid Number[/bright_red]")
                continue
            all_blobs = vida_logs_handler.get_blobs_by_sn_and_date(target_date=date, max_results=max_results)
            if not all_blobs:
                print("[bright_red]No logs found[/bright_red]")
            else:
                print(f"[bright_yellow]Found {len(all_blobs)} logs[/bright_yellow]")
                with Progress() as progress:
                    task = progress.add_task("[cyan]Unzipping logs...", total=len(all_blobs))
                    for blob_name in all_blobs:
                        blob_data = vida_logs_handler.download_blob_to_memory(blob_name)
                        combined_unzipper = CombinedUnzipper(blob_name, blob_data)
                        if download_local:
                            if not os.path.exists("tmp"):
                                os.makedirs("tmp")
                            with open(f"tmp/{combined_unzipper.log_name}", 'wb') as f:
                                f.write(combined_unzipper.log_data)
                            print(f"\n[bright_green]Log unzipped and saved locally: {combined_unzipper.log_name}[/bright_green]\n")
                        else:
                            dev_handler.upload_blob(combined_unzipper.log_name, combined_unzipper.log_data)
                        progress.update(task, advance=1)
                    print(f"\n[bright_green]All logs unzipped and uploaded to Destination[/bright_green]\n")
        elif choice == "Exit":   
            print("[bright_red]Goodbye![/bright_red]")
            exit()
