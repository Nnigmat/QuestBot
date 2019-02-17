def parse(path):
    res = []
    with open(path) as config:
        for line in config.readlines():
            temp = line.split(' ')
            temp[3] = temp[3].strip('\n')
            text = 'aqua'
            if temp[2] not in ['img', 'audio', 'video']:
                text = open('src//{}//{}'.format(temp[2], temp[3])).read()
            else:
                text = open(f'src/{temp[2]}/{temp[3]}', 'rb').read()
            res.append({'current':temp[0], 'next':temp[1], 'type':temp[2], 'text':text})
    return res
