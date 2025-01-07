import time
import requests
import os


def query_domain_with_retry(domain, api_key, retry_limit=3, delay=1):
    """
    查询单个域名的百度权重，并处理速率限制和错误。
    :param domain: 要查询的域名
    :param api_key: 爱站 API Key
    :param retry_limit: 最大重试次数
    :param delay: 请求之间的延迟（以秒为单位）
    """
    retries = 0
    while retries < retry_limit:
        try:
            # 构造请求 URL
            url = f'https://apistore.aizhan.com/baidurank/siteinfos/{api_key}?domains={domain}'
            print(f"正在查询域名: {domain}")
            
            # 发送请求
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 如果 HTTP 状态码不是 200，将抛出异常
            
            # 处理速率限制错误
            if '"code":100008' in response.text:
                print(f"速率限制触发，等待 {delay * 2} 秒后重试...")
                time.sleep(delay * 2)  # 如果触发速率限制，等待 2 倍的延迟时间后重试
                retries += 1
                continue
            
            # 解析返回的 JSON 数据
            data = response.json()
            if data['status'] == 'error':
                print(f"查询域名 {domain} 时出错，错误信息: {data['msg']}")
                return  # 如果 API 返回错误状态，直接退出
            
            # 提取百度权重信息
            if data['status'] == 'success' and data['data']['success']:
                pc_br = data['data']['success'][0]['pc_br']  # PC 端百度权重
                print(f'域名: {domain} 的 PC 端百度权重是: {pc_br}')
                
                # 将结果保存到文件中
                filename = f'{pc_br}.txt'
                with open(filename, 'a+', encoding='utf-8') as file:
                    file.write(domain + '\n')
                print(f"域名 {domain} 的查询结果已保存到文件: {filename}")
                return  # 查询成功，退出函数
            else:
                print(f"未能获取域名 {domain} 的数据，可能是 API 返回了空数据。")
                return

        except requests.exceptions.RequestException as e:
            print(f"请求域名 {domain} 时发生网络错误: {e}")
        except KeyError:
            print(f"解析 API 响应时出错，API 响应: {response.text}")
        except Exception as e:
            print(f"查询域名 {domain} 时发生未知错误: {e}")
        
        # 如果发生错误，增加重试计数并延迟一段时间
        retries += 1
        print(f"正在重试 ({retries}/{retry_limit}) ...")
        time.sleep(delay)

    print(f"域名 {domain} 查询失败，已达到最大重试次数。")


def main():
    # 设置 API Key
    api_key = "your_api"  # 请替换为你的爱站 API Key
    file_path = "url.txt"  # 默认文件路径为当前目录下的 url.txt

    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"未找到文件 {file_path}，请确保文件在脚本当前目录下。")
            return

        # 从文件中读取域名
        with open(file_path, 'r', encoding='utf-8') as file:
            domains = [line.strip() for line in file if line.strip()]
        
        if not domains:
            print("文件中没有可用的域名，请检查文件内容。")
            return

        # 遍历域名列表并查询每个域名
        for domain in domains:
            query_domain_with_retry(domain, api_key, retry_limit=3, delay=1)
    except Exception as e:
        print(f"读取文件 {file_path} 时发生错误: {e}")


if __name__ == "__main__":
    main()
