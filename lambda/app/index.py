from typing import Dict, Any
import os
import pandas as pd
from box.box_authenticator import BoxAuthenticator
from box.box_uploader import BoxUploader
from rds.rds_query_executor import RDSQueryExecutor
from file.excel_exporter import ExcelExporter
from config import ConfigLoader
from slack.slack_notifier import SlackNotifier


def handler(event, context):
    # Load configs and authenticate
    config = ConfigLoader()
    box_config = config.load_box_config()
    box_authenticator = BoxAuthenticator(box_config)
    box_client = box_authenticator.authenticate()
    box_uploader = BoxUploader(box_client, box_config)
    rds_query_executor = RDSQueryExecutor(config.load_rds_config())

    # Execute RDS query and fetch results
    query_result: Dict[str, Any] = rds_query_executor.execute_query()

    # Export query results to xlsx
    local_dist_file_path = f"/tmp/{box_config.box_dist_file_name}"
    dataframe_exporter = ExcelExporter()
    dataframe_exporter.save_to_xlsx(pd.DataFrame(query_result), local_dist_file_path)

    # Upload to Box
    result = box_uploader.upload_file(local_dist_file_path)
    os.remove(local_dist_file_path)

    # Notify to Slack
    notifier = SlackNotifier(config.load_slack_config())
    notifier.send_message(
        f":rocket: *Boxへのアップロードが完了しました* :rocket:\n"
        f"==============================================\n"
        f"◇ファイル名: {result['box_file_name']}\n"
        f"◇ファイルID: {result['box_file_id']}\n"
        f"◇フォルダID: {result['box_folder_id']}\n"
        f"◇共有リンク: {result['shared_link']}\n"
        f"=============================================="
    )

    return {"statusCode": 200, "body": result}


def main():
    print(handler(None, None))


if __name__ == "__main__":
    main()
