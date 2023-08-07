import csv
from collections import defaultdict

filename = 'traf.txt'

with open(filename, 'r') as file:
    reader = csv.reader(file, delimiter=';')

    unique_nodes = set()
    total_data_transfer = 0
    udp_data_transfer = 0
    nodes_data_transfer = defaultdict(int)
    subnet_sessions = defaultdict(int)
    node_sessions = defaultdict(set)
    total_time = 0

    for row in reader:
        source_node = row[0].split(':')[0]
        destination_node = row[2].split(':')[0]
        udp_flag = row[4] == 'true'
        data_transfer = int(row[5])
        transfer_time = float(row[6])
        total_time += transfer_time

        unique_nodes.add(source_node)
        unique_nodes.add(destination_node)

        total_data_transfer += data_transfer

        nodes_data_transfer[source_node] += data_transfer
        nodes_data_transfer[destination_node] += data_transfer

        if udp_flag:
            udp_data_transfer += data_transfer

        subnet = '.'.join(destination_node.split('.')[:3])
        subnet_sessions[subnet] += 1

        node_sessions[source_node].add(destination_node)

# Q1. Количество уникальных узлов в наблюдаемой сети
unique_node_count = len(unique_nodes)
print(f"Q1. Количество уникальных узлов в наблюдаемой сети: {unique_node_count}")

# Q2. Средняя скорость передачи данных всей наблюдаемой сети
if total_time > 0:
    average_data_transfer_rate = total_data_transfer / total_time
print(f"Q2. Средняя скорость передачи данных всей наблюдаемой сети: {round(average_data_transfer_rate, 2)}байт/сек")

# Q3. Верно ли утверждение "UDP используется для передачи данных с максимальной пиковой скоростью"?
udp_usage_percentage = (udp_data_transfer / total_data_transfer) * 100
udp_peak_speed_statement = udp_usage_percentage > 50
print(
    f"Q3. Утверждение 'UDP используется для передачи данных с максимальной пиковой скоростью' верно: {udp_peak_speed_statement}")

# Q4. Узлы с самой высокой средней скоростью передачи данных (топ 10)
top_10_nodes = sorted(nodes_data_transfer.items(), key=lambda x: x[1], reverse=True)[:10]
print("Q4. Узлы с самой высокой средней скоростью передачи данных:")
for node, data_transfer in top_10_nodes:
    if len(node_sessions[node]) > 0:
        transfer_rate = data_transfer / len(node_sessions[node])
        print(f"Узел: {node}, Средняя скорость передачи данных: {round(transfer_rate, 2)} байт/сек")

# Q5. Самые активные подсети /24 (топ 10)
top_10_subnets = sorted(subnet_sessions.items(), key=lambda x: x[1], reverse=True)[:10]
print("Q5. Самые активные подсети /24:")
for subnet, sessions in top_10_subnets:
    print(f"Подсеть {subnet}: сессий {sessions}")

# Q6. Узлы, которые могут являться посредниками (PROXY)
proxy_nodes = set()
for node, sessions in node_sessions.items():
    protocols = set()
    for destination_node in sessions:
        if destination_node in node_sessions:
            protocols.update(node_sessions[destination_node])
    if len(protocols) > 1:
        proxy_nodes.add(node)

print("Q6. Узлы, которые могут являться посредниками (PROXY):")
proxy_nodes_count = len(proxy_nodes)
print(f"Всего узлов, которые могут являться посредниками: {proxy_nodes_count}")
if proxy_nodes_count > 0:
    top_10_proxy_nodes = list(proxy_nodes)[:10]
    print("Топ 10 узлов, которые могут являться посредниками:")
    for node in top_10_proxy_nodes:
        print(node)
