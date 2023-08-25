export OPENAI_TOKEN=`aws ssm get-parameter --name secret-mti-nerve-prd-azure_openai_token --with-decryption --output=text --query Parameter.Value`
