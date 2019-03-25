# -*- coding: utf-8 -*-
import boto3

def save_user_data(user, data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('unicamp_utils_bot')
    r = table.put_item(Item={ 'user_id' : user, 'data' : data})
    return r

def get_user_data(user):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('unicamp_utils_bot')
    r = table.get_item(Key={ 'user_id' : user})
    return r