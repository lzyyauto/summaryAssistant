import json

import mysql.connector

from config import (MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT,
                    MYSQL_USER)

cnx = mysql.connector.connect(host=MYSQL_HOST,
                              port=MYSQL_PORT,
                              user=MYSQL_USER,
                              password=MYSQL_PASSWORD,
                              database=MYSQL_DATABASE)

cursor = cnx.cursor()


def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (   
            id INT AUTO_INCREMENT,
            title VARCHAR(255),
            type ENUM('traffic_acquisition', 'keyword_research', 'overseas_strategies', 'not_relevant'),
            confidence FLOAT,
            summary TEXT,
            methods JSON,
            tools JSON,
            data_sources JSON,
            key_insights JSON,
            notes TEXT,
            processed BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id)
        )
    ''')


def insert_article(title):
    cursor.execute('INSERT INTO articles (title) VALUES (%s)', (title, ))
    cnx.commit()


def update_article(title, response_json):
    cursor.execute(
        '''
        UPDATE articles 
        SET type = %s,
            confidence = %s,
            summary = %s,
            methods = %s,
            tools = %s,
            data_sources = %s,
            key_insights = %s,
            notes = %s,
            processed = TRUE 
        WHERE title = %s
    ''', (response_json['type'], response_json['confidence'],
          response_json['summary'],
          json.dumps(response_json['details']['methods']),
          json.dumps(response_json['details']['tools']),
          json.dumps(response_json['details']['data_sources']),
          json.dumps(response_json['details']['key_insights']),
          response_json['notes'], title))
    cnx.commit()


def is_article_processed(title):
    cursor.execute('SELECT processed FROM articles WHERE title = %s',
                   (title, ))
    result = cursor.fetchone()
    return bool(result and result[0])


def save_article(file, response):
    try:
        if is_article_processed(file):
            print(f"文件 {file} 已处理过，跳过")
            return True

        response_json = json.loads(response)

        details = response_json.get('details', {})
        cursor.execute(
            '''
            INSERT INTO articles (
                title, type, confidence, summary, 
                methods, tools, data_sources, key_insights, 
                notes, processed
            ) VALUES (
                %s, %s, %s, %s, 
                %s, %s, %s, %s, 
                %s, TRUE
            )
        ''', (file, response_json.get(
                'type', 'not_relevant'), response_json.get(
                    'confidence', 0.0), response_json.get(
                        'summary', ''), json.dumps(details.get('methods', [])),
              json.dumps(details.get(
                  'tools', [])), json.dumps(details.get('data_sources', [])),
              json.dumps(details.get('key_insights',
                                     [])), response_json.get('notes', '')))
        cnx.commit()
        return True
    except json.JSONDecodeError as e:
        print(f"JSON解析错误 ({file}): {e}")
        return False
    except Exception as e:
        print(f"保存文章时出错 ({file}): {e}")
        return False
