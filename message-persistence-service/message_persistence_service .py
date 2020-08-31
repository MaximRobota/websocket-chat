print('Hi')
import asyncio
import json
import config
import requests
import re

from kafka.common import KafkaError
from aiokafka import AIOKafkaConsumer
from kafka import KafkaProducer

from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict


def encode_dict(data):
    return json.dumps(data).encode()

def order_dict(dictionary):
    sorted_keywords = ['id','event', 'data', 'zones']
    ordered_dict = OrderedDict()
    for kword in sorted_keywords:
        ordered_dict[kword] = dictionary[kword]
    return ordered_dict



def call_segmentation(producer, im_data, kafka_json, loop, request_counter):

    obj = {'rect_bbox': False,
        'merge_win_door': True,
        'draw_objects': 20,
            'wind_thr': 5,
            'detect_list': ['door', 'windowpane',
            'floor', 'furniture', 'houseware',
            'plant', 'road', 'ceiling',
            'grass', 'wall', 'curtain', 'painting',
            'fence', 'refrigerator', 'base', 'column',
            'stage', 'screen', 'person', 'bench',
            'table', 'desk', 'wardrobe', 'bookcase',
            'bathhub', 'counter', 'countertop', 'shelf'],
        'door_thr': 6,
        'base64_img': im_data, 'bbox_filter': 0}
    data = json.dumps({'data': obj}).encode('utf-8')

    print('\x1b[6;30;42m' + 'Request to GPU id=' + str(request_counter)+ '\x1b[0m')
    response =  requests.post('http://10.0.0.202/segmentation/process_kafka',
            data=data)


    #kafka_json['data']['data'] = im_data

    #-------------------
    # FOR TEST
    kafka_json['data']['data'] = 'image_base64_data_not_showing_in_json_for_test'
    #-------------------

    kafka_json['zones'] = response.json()
    kafka_json['event'] = 'management'

    #kafka_json['id'] = 'MGT_{}'.format(re.search(r'\d+', kafka_json['id']).group())
    print('\x1b[6;30;42m' + 'Response from GPU id=' + str(request_counter)+ '\x1b[0m')
    ordered_dict_out = order_dict(kafka_json)

    # DO SOME POSTING TO KAFKA
    # RETURN JSON TO SP
    ##################################################################
    # Sending data to other topic
    producer.send("MGT", json.dumps(ordered_dict_out).encode('utf-8'))
    ##################################################################
    #TODO FIND BUG


async def consume_task(consumer, producer, loop, executor):
    request_counter = 0
    while True:
        try:
            msg = await consumer.getone()
            data = json.loads(msg.value.decode())

            print('\n### - ', data['event'])
            segment = False
            base64_image = ''
            for k, v in data.items():

                if k == 'data':
                    if 'type' in data[k]:
                        if data[k]['type'] == 'bkg_image/jpeg': segment = True
                    for k2, v2 in data[k].items():

                        if k2 == 'data':
                            if segment == True: base64_image = v2
                            print('     ', k2, v2[-10:])
                        else:
                            print('     ', k2, v2)
                else:
                    print('     ', k, v)
            if segment == True:
                #future = asyncio.run_coroutine_threadsafe(call_segmentation(), loop)
                request_counter += 1
                future = loop.run_in_executor(executor, call_segmentation,
                                            producer, base64_image, data, loop,
                                            request_counter)

                #response = await future
                #print (dir(future))
                #print (future)

        except KafkaError as err:
            print("error while consuming message: ", err)


loop = asyncio.get_event_loop()
consumer = AIOKafkaConsumer(
    "MED", loop=loop, bootstrap_servers=config.bootstrap_servers)

producer = KafkaProducer(bootstrap_servers=config.bootstrap_servers)
# Bootstrap client, will get initial cluster metadata
loop.run_until_complete(consumer.start())
executor = ThreadPoolExecutor(max_workers=2)
c_task = loop.create_task(consume_task(consumer, producer, loop, executor))

try:
    loop.run_forever()
finally:
    # Will gracefully leave consumer group; perform autocommit if enabled
    loop.run_until_complete(consumer.stop())
    c_task.cancel()

    loop.close()

