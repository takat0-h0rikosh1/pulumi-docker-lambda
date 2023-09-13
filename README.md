# rds-box-query-uploader

RDSにクエリした結果をBOM付きXLSXファイルに変換してBOXにアップロードします。

# 設定手順

TODO: あとでちゃんと書く

1. ./pulumi_code/queries 配下にSQLを配置
1. ./pulumi_code/config/ 配下の設定ファイル(環境毎)のlambda_configsに設定を追加
1. デプロイする
   - ```
     $ cd pulumi_code

     $ aws-vault exec <profile>

     $ pulumi login <s3_bucket>

     $ export PULUMI_CONFIG_PASSPHRASE=""; pulumi up -y -s <qa | prod>
     ```  
