import Db
import ip


db = Db.DB()
sn = 1000000000000599
sensor_name_pre = 'test'
num = 599

for x in range(20000):
    sn += 1
    num += 1
    mac = ip.randomMAC()
    sensor_name = sensor_name_pre + str(num)

    sql = "INSERT INTO `WIPS`.`device` (`sn`, `ip`, `mac`, `server_id`, `vid`, `coords`, `sensor_name`, `version`, `hard_version`, `update_status`, `vpn_ip`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    valu = (str(sn), '10.18.209.217', mac, '1', '1001', '', sensor_name, '2.0.1.3523', '3', '2', '')
    scanNum = db.insert(sql, valu)
