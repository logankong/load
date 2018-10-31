# -*- coding:utf-8 -*-
from __future__ import division
import CRedis
import time
import Stats


class Report():
    """性能测试报告"""

    def __init__(self):
        self.r = CRedis.CRedis()
        self.is_report = '1'

    def report(self):
        while self.is_report == '1':
            self.is_report = self.r.get('is_report')
            if self.is_report == '1':
                self.r.set('etime', time.time())
            tsnames = self.r.keys()
            'ctime' in tsnames and tsnames.remove('ctime')
            'etime' in tsnames and tsnames.remove('etime')
            'is_report' in tsnames and tsnames.remove('is_report')
            tsnames.sort()

            ctime = self.r.get('ctime')
            etime = self.r.get('etime')
            print('测试报告')
            print('----------------------------------------------------------------------------')
            print('开始时间    {0}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(ctime)))))
            print('运行时间    {0:.0f}(s)'.format(float(etime) - float(ctime)))
            print('{0:<49}{1:<10}{2:<10}{3:<10}{4:<10}'.format('事务名称', '总数', '成功', '失败', '失败率'))
            total_tscount = []
            total_tssuccess = []
            total_tsfail = []
            for tsname in tsnames:
                if 'success' in tsname or 'fail' in tsname:
                    continue
                tssuccess = self.r.get(tsname + '_success')
                if not tssuccess:
                    tssuccess = 0
                tsfail = self.r.get(tsname + '_fail')
                if not tsfail:
                    tsfail = 0
                tscount = int(tssuccess) + int(tsfail)
                if int(tscount) == 0:
                    tspercent = 0
                else:
                    tspercent = int(tsfail) / int(tscount) * 100

                total_tscount.append(tscount)
                total_tssuccess.append(int(tssuccess))
                total_tsfail.append(int(tsfail))
                print('{0:<45}{1:<8}{2:<8}{3:<8}{4:.2f}%'.format(tsname, tscount, tssuccess, tsfail, tspercent))

            print('\n响应时间(ms)')
            print('{0:<49}{1:<11}{2:<11}{3:<11}{4:<11}{5:<11}'.format('事务名称', '最小值', '最大值', '平均值', '中位数', '标准偏差'))
            for tsname in tsnames:
                if 'success' in tsname or 'fail' in tsname:
                    continue
                tstime = self.r.lrange(tsname)

                if tstime:
                    tstime = map(eval, tstime)
                    self.s = Stats.Stats(tstime)
                    min_sttime = self.s.min() * 1000
                    max_sttime = self.s.max() * 1000
                    average_sttime = self.s.avg() * 1000
                    median_sttime = self.s.median() * 1000
                    stdev_sttime = self.s.stdev()
                print('{0:<45}{1:<8.2f}{2:<8.2f}{3:<8.2f}{4:<8.2f}{5:<8.6f}/1000'.format(tsname,
                                                                                         min_sttime,
                                                                                         max_sttime,
                                                                                         average_sttime,
                                                                                         median_sttime,
                                                                                         stdev_sttime))
            time.sleep(30)
        else:
            file = 'result_' + format(time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time())))
            result = open(file, 'a+')

            result.write('测试报告\n')
            result.write('----------------------------------------------------------------------------\n')
            result.write('开始时间    {0}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S\n', time.localtime(float(ctime)))))
            result.write('运行时间    {0:.0f}(s)\n'.format(float(etime) - float(ctime)))
            result.write('{0:<49}{1:<10}{2:<10}{3:<10}{4:<10}\n'.format('事务名称', '总数', '成功', '失败', '失败率'))
            total_tscount = []
            total_tssuccess = []
            total_tsfail = []
            for tsname in tsnames:
                if 'success' in tsname or 'fail' in tsname:
                    continue
                tssuccess = self.r.get(tsname + '_success')
                if not tssuccess:
                    tssuccess = 0
                tsfail = self.r.get(tsname + '_fail')
                if not tsfail:
                    tsfail = 0
                tscount = int(tssuccess) + int(tsfail)
                if int(tscount) == 0:
                    tspercent = 0
                else:
                    tspercent = int(tsfail) / int(tscount) * 100

                total_tscount.append(tscount)
                total_tssuccess.append(int(tssuccess))
                total_tsfail.append(int(tsfail))
                result.write('{0:<45}{1:<8}{2:<8}{3:<8}{4:.2f}%\n'.format(tsname, tscount, tssuccess, tsfail, tspercent))
            result.write('响应时间(ms)\n')
            result.write('{0:<49}{1:<11}{2:<11}{3:<11}{4:<11}{5:<11}\n'.format('事务名称', '最小值', '最大值', '平均值', '中位数', '标准偏差'))
            for tsname in tsnames:
                if 'success' in tsname or 'fail' in tsname:
                    continue
                tstime = self.r.lrange(tsname)

                if tstime:
                    tstime = map(eval, tstime)
                    self.s = Stats.Stats(tstime)
                    min_sttime = self.s.min() * 1000
                    max_sttime = self.s.max() * 1000
                    average_sttime = self.s.avg() * 1000
                    median_sttime = self.s.median() * 1000
                    stdev_sttime = self.s.stdev()
                result.write('{0:<45}{1:<8.2f}{2:<8.2f}{3:<8.2f}{4:<8.2f}{5:<8.6f}/1000\n'.format(tsname,
                                                                                         min_sttime,
                                                                                         max_sttime,
                                                                                         average_sttime,
                                                                                         median_sttime,
                                                                                         stdev_sttime))

            result.close()


if __name__ == '__main__':
    report = Report()
    report.report()
