# _*_encoding:utf-8_*_

# csv_path = "../repertory/site_csv.csv"  # csv文件地址
# json_path = "../repertory/recode_json.json".replace("/", "\\")  # json文件地址
#logFormat = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"  # 日志输入格式
#user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)  AppleWebKit 537.36 (KHTML, like Gecko) Chrome"  # 请求头user-agent
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"  # 请求头accept

sqlite_path = r"../repertory/site_list.db3".replace("/", "\\")
# sqlite_path = r"../repertory/site_list.db3"

sql = 'select site_url, site_name from site_info where is_dynamic = 0 and can_be_visited = 1'

can_visit_sql = "select site_url, site_name from site_info where can_be_visited = 1"
not_need_proxy_sql = "select site_url, site_name from site_info where can_be_visited = 1 and need_proxy = 0"

can_check_sql = "select url,url_name,last_modified, etag, hash_text from site_check where can_check = 1"
# can_check_sql = "select url,url_name,last_modified, etag, hash_text from site_check"
update_sql = "update site_check set can_check = -1 where url = "
