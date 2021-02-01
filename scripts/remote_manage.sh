#!/usr/bin/env bash

if [ "$#" == "0" ]; then
    echo "Usage: remote_manage.sh <command>"
    echo "Examples: (username, email and password all required!)"
    echo "remote_manage.sh createsuperuser --noinput --username wbastian --email will.bastian@sleepio.com --password mainlypicturegivingfamily

"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "jq is required. brew install jq
    "
    exit 1
fi

account=$(aws iam list-account-aliases --query AccountAliases[0] --output text)
safe_accounts=(
    bhdevacct
    # bhciacct
    # bhqaacct
)
if [[ ! " ${safe_accounts[@]} " =~ " ${account} " ]]; then
    echo "The current AWS account is not in the approved list of safe accounts to run this in"
    exit 1
fi

command="$@"

echo $command

community_web_function=$(aws lambda list-functions --query 'Functions[?contains(FunctionName,`community-app-web-`)][FunctionName]' --output text)

output_file=$(mktemp)

# --cli-binary-format raw-in-base64-out required for aws cli v2
aws lambda invoke --function-name $community_web_function --payload "{\"manage\":\"${command}\"}" --cli-binary-format raw-in-base64-out $output_file 1>/dev/null

cat $output_file | jq
