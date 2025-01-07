import re


def is_ip_address(text):
    """
    判断一个字符串是否为 IP 地址（IPv4），支持带端口号的情况。
    """
    ip_pattern = re.compile(
        r'^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.){3}'
        r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)(:\d{1,5})?$'
    )
    return ip_pattern.match(text) is not None


def extract_main_domain(url):
    """
    提取 URL 或域名中的主域名，并过滤掉非域名的内容。
    """
    # 如果是 IP 地址，直接返回 None
    if is_ip_address(url):
        return None

    # 匹配主域名的正则表达式（忽略协议部分、路径和端口号）
    domain_pattern = re.compile(
        r'^(?:https?://|http?://)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})'
    )
    match = domain_pattern.search(url)
    if match:
        return match.group(1)  # 返回提取的主域名部分
    return None


def filter_domains(input_file, output_file):
    """
    读取输入文件，提取有效的主域名，并保存到输出文件。
    """
    try:
        # 读取输入文件并去除空行
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]

        # 提取主域名
        main_domains = []
        for line in lines:
            domain = extract_main_domain(line)
            if domain:  # 如果提取出主域名，加入结果集
                main_domains.append(domain)

        # 去重并排序
        main_domains = sorted(set(main_domains))

        # 保存到输出文件
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(main_domains))
        print(f"主域名提取完成，结果已保存到文件：{output_file}")

    except FileNotFoundError:
        print(f"输入文件 {input_file} 不存在，请检查文件路径。")
    except Exception as e:
        print(f"处理文件时发生错误：{e}")


if __name__ == "__main__":
    # 输入和输出文件路径
    input_file = "zichan.txt"  # 输入文件名（改为zichan.txt）
    output_file = "url.txt"  # 输出文件名（改为url.txt）
    filter_domains(input_file, output_file)
