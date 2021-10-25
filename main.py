from jd_spider_requests import JdSeckill


def main():
    # 1. 初始化
    seckill = JdSeckill()
    # 2. 预约
    seckill.reserve()
    # 3. 抢购
    seckill.seckill_by_proc_pool()


if __name__ == '__main__':
    main()
