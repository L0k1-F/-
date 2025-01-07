from tld import get_fld, get_tld
import re


def extract_main_domain(url):
    """
    提取主域名（忽略子域名部分）。
    使用 tld 库处理复杂后缀，确保提取主域名。
    """
    try:
        # 去掉协议部分 (http://, https://)
        url = re.sub(r'^https?://', '', url)

        # 去掉端口号和路径
        url = re.sub(r'[:/].*$', '', url)

        # 忽略 IP 地址
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', url):
            return None

        # 提取主域名
        fld = get_fld(url, fix_protocol=True)  # 使用 tld 提取主域名
        return fld
    except Exception:
        return None


def process_domains(input_file, output_file):
    """
    处理输入文件，提取主域名并输出到文件。
    """
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 提取主域名
        domains = set()
        for line in lines:
            domain = extract_main_domain(line.strip())
            if domain:
                domains.add(domain)

        # 排序并写入输出文件
        sorted_domains = sorted(domains)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(sorted_domains))

        print(f"处理完成，共提取出 {len(sorted_domains)} 个主域名。结果已保存到 {output_file}")

    except FileNotFoundError:
        print(f"输入文件 {input_file} 不存在，请检查文件路径！")
    except Exception as e:
        print(f"处理时发生错误：{e}")


# 示例运行
if __name__ == "__main__":
    # 输入文件名
    input_file = 'zichan.txt'
    # 输出文件名
    output_file = 'url.txt'
    process_domains(input_file, output_file)
