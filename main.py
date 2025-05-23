import boto3
from discord_webhook import DiscordWebhook, DiscordEmbed

print('Loading function')

def lambda_handler(context, event):

    # config
    bucket = 'splunk-logs-cisa-group2'

    client = boto3.client('s3')
    response = client.list_objects(Bucket=bucket)['Contents']
    items = 0
    list_of_items = ""
    list_of_storage_class = ""
    list_of_last_modified = ""

    for item in response:
        items += 1
        list_of_items = list_of_items + "\n" + item['Key']
        list_of_storage_class = list_of_storage_class + "\n" + item['StorageClass']
        list_of_last_modified = list_of_last_modified + "\n" + str(item['LastModified'])

    print(response)

    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1375509400994971758/Iam9qNCW_Dt68KIKQlx7jDV4onQGfbErNcsqg8XKEmxQ_CiGYEw0PuuIGjajSpkjT9_w')
    embed = DiscordEmbed(title='Amazon S3', description=f"AWS S3 has been updated with **{items}** item(s):", color='FF9900')
    embed.add_embed_field(name="Items in S3:", value=f"{list_of_items}")
    embed.add_embed_field(name="Storage Class:", value=f"{list_of_storage_class}")
    embed.add_embed_field(name="Last Modified:", value=f"{list_of_last_modified}")

    webhook.add_embed(embed)
    webhook.execute()

