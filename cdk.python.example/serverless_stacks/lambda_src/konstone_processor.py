# -*- coding: utf-8 -*-

from decimal import Decimal
import json
import logging
import os
import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(level=os.getenv('LOG_LEVEL', 'DEBUG').upper())

def lambda_handler(event, context):
    # global LOGGER
    #LOGGER.info(f"Received_event:{event}")

    rows = read_from_s3()
    table_name = os.getenv('DYNAMODB_TABLE', 'Movies')
    lod_movies(rows, table_name)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": event})
    }


def read_from_s3(s3Bucket=None):
    if not s3Bucket:
        s3 = boto3.client('s3')
    csvfile = s3.get_object(Bucket='bucket-list-files', Key='moviedata.json')
    csvcontent = csvfile['Body'].read().decode('utf-8')
    return json.loads(csvcontent, parse_float=Decimal)


def lod_movies(movies, tableName, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
        # dynamodb = boto3.client('dynamodb')

    table = dynamodb.Table(tableName)
    for movie in movies:
        insetItem = {}
        year = int(movie['year'])
        insetItem['year'] = year
        title = movie['title']
        insetItem['title'] = title
        if 'genres'in movie['info']:
            insetItem['genres'] =  movie['info']['genres']
        if 'directors' in movie['info']:
            insetItem['directors'] = movie['info']['directors']
        if 'rating' in movie['info']:
            insetItem['rating'] = movie['info']['rating']
        insetItem['info'] = movie['info']
        print("Adding movie:", year, title)
        table.put_item(Item=insetItem)
        #table.put_item(Item=movie)