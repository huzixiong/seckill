import subprocess


def get_device_connect():
    try:
        result = subprocess.check_output('adb devices').decode('utf-8').split('\r\n')[1]
        if result:
            # print(result)
            return True
        else:
            # print("请检查设备是否连接或者端口是否打开")
            return False
    except Exception as e:
        print(e)


def get_device_ID():
    try:
        result_temp = subprocess.check_output('adb devices').decode('utf-8').split('\r\n')
        result = result_temp.split('\t')[0]
        print('获取到id为：', result)
        return result
    except:
        print('无法获取设备id')
        return False


if __name__ == '__main__':
    connect = get_device_connect()
    print(connect)
