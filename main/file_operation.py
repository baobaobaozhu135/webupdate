# _*_encoding:utf-8_*_

import json
import sqlite3
import configure_file as conf


# 读取json文件并转化为json对象
def read_file_to_json(json_path):
    try:
        json_stream = open(json_path)
        data = json_stream.read()
        json_obj = {}
        if data:
            json_obj = json.loads(data)  # 因为直接从内存读取转为json所以用loads(加上s),从文件的话用load
        return json_obj
    except IOError:
        with open(json_path, "w") as json_obj:
            json.dump({}, json_obj, ensure_ascii=False)
            return {}


# 将网址及杂凑值写入json文件
def write_json_to_filepath(json_path, json_obj):
    with open(json_path, "w") as outfile:
        json.dump(json_obj, outfile, ensure_ascii=False)

# 将csv文件转化成list对象
def read_csv_file_to_list(csv_path):
    with open(csv_path) as csvFile:
        # csv_str_s = csv.reader(csvFile)  错误
        csv_str_s = csvFile.read()
        site_list = []
        if csv_str_s:
            # print csv_str_s
            # print csv_str_list[1]
            # site_list = list[csv_str_list]
            csv_str_list = csv_str_s.split("\n")
            site_list = csv_str_list
        return site_list


# 读取sqlite3并转化为list
def read_sqlite(sqlite_path, sql):
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        cursor.execute(sql)
        values = cursor.fetchall()
        sql_dict = {}

        if values:
            # print "values_count:" + str(len(values))
            for items in values:
                # print items
                sql_dict2 = {}
                sql_dict2["url_name"] = items[1]
                sql_dict2["last_modified"] = items[2]
                sql_dict2["eTag"] = items[3]
                sql_dict2["hash_text"] = items[4]
                sql_dict[items[0]] = sql_dict2
            # print sql_dict
            # print sql_dict[u'https://www.cato.org/publications']

        return sql_dict
    except Exception as e:
        print "ERROR:" + str(e)
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()


# read_sqlite(conf.sqlite_path, conf.sql)
# 更新sqlite 中网站是否可以监测
def update_sqlite_dynamic(sqlite_path, url):
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        cursor.execute(conf.update_sql + "'" + url + "'")

    except Exception as e:
        print "ERROR:" + str(e)
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()


# 修改sqlite 网站last_modified,eTag,hash_text
def update_sqlite_context(sqlite_path, url, last_modified, etag, hash_text):
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        sql = "update site_check set "
        if last_modified:
            sql = sql + "last_modified = '" + last_modified + "' "
        else:
            sql = sql + "last_modified = ''"
        if etag:
            sql = sql + ", etag = '" + etag + "' "
        else:
            sql = sql + ", etag = ''"
        if hash_text:
            sql = sql + ",hash_text = '" + hash_text + "' "
        else:
            sql = sql + ", hash_text = ''"
        sql = sql + " where url = '" + url + "'"
        # print sql
        cursor.execute(sql)
    except Exception as e:
        print "ERROR:" + str(e)
    finally:
        if cursor and conn:
            cursor.close()
            conn.commit()
            conn.close()
