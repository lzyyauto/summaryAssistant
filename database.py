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


def save_article(file, response):
    try:
        response_json = json.loads(response)
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
        ''', (file, response_json['type'], response_json['confidence'],
              response_json['summary'],
              json.dumps(response_json['details']['methods']),
              json.dumps(response_json['details']['tools']),
              json.dumps(response_json['details']['data_sources']),
              json.dumps(response_json['details']['key_insights']),
              response_json['notes']))
        cnx.commit()
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return
