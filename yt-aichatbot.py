from langchain.document_loaders import YoutubeLoader
import keys
import json
import boto3

session = boto3.Session(aws_access_key_id=keys.aws_access_key_id,
                        aws_secret_access_key=keys.aws_secret_access_key)
boto3_bedrock = session.client(service_name='bedrock', region_name='us-east-1')

url = input("Enter URL for the youtube video : ")

youtubeloder = YoutubeLoader.from_youtube_url(url)
yt_doc = youtubeloder.load()
if len(yt_doc) < 1:

    print("Error : Video has no transcript")
    exit()

yt_doc = "Human: Provide a summary of the following youtube video: \n" + \
    yt_doc[0].page_content + "\n\nAssistant:"

body = json.dumps({"prompt": yt_doc, "max_tokens_to_sample": 500})
modelId = "anthropic.claude-instant-v1"
accept = "application/json"
contentType = "application/json"

response = boto3_bedrock.invoke_model(
    body=body, modelId=modelId, accept=accept, contentType=contentType
)
response_body = json.loads(response.get("body").read())

print(response_body.get("completion"))
