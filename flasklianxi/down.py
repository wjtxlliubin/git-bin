import redis, os
import json
import wget
import qiniu


def download(url):
    """

    :param url:
    :return:
    """
    filename = wget.download(url)
    return filename


def upload(file_name, key):
    """

    :return:
    """
    # todo 修改七牛参数
    ak, sk = 'GL-d8gkb3agN8peLMq_FTOZQzoKPo576C-InyE3y', 'hOfFTmQ3UNYn-i8oImMhMgZGlCvLMAvJXp2cFK_q'
    bucket_name = 'liubin'
    q = qiniu.Auth(ak, sk)
    policy = {
        # todo 修改地址
        'callbackUrl': 'http://139.224.135.112:8000/callback',
        'callbackBody': '{"filename":"$(fname)","filesize":"$(fsize)","key":"' + key + '"}'
    }

    token = q.upload_token(bucket_name, file_name, 3600, policy)
    local_file = os.path.join(os.curdir, file_name)
    print(local_file)
    ret, info = qiniu.put_file(token, file_name, local_file)
    print("ret:", ret, "info", info)


def main():
    rds = redis.Redis(host='localhost', port=6379, db=0, password=None)
    ps = rds.pubsub()
    ps.subscribe('download_job')
    for item in ps.listen():
        print(item)
        if isinstance(item['data'], int):
            continue
        message = item['data'].decode() if isinstance(item['data'], bytes) else item['data']
        message = json.loads(message)
        print(message['url'])
        file_name = download(message['url'])
        print(file_name)
        upload(file_name, message['key'])


if __name__ == '__main__':
    main()
