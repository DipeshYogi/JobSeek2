import psycopg2

class GetConnection():
    """get connection to the postgres database"""

    def obtain_conn(self):
        try:
            conn = psycopg2.connect(   user='lvdbzgnnnthckg',
                                            password= '7ef0652e2f717ff49f5369871183b2dcdd15d9c52a7c55fcef98779d410dcb10',
                                            host = 'ec2-184-72-237-95.compute-1.amazonaws.com',
                                            port = '5432',
                                            database = 'd32b9rckhe5166',

                                            )

            cursor = conn.cursor()
            return cursor


        except (Exception, psycopg2.Error) as error:
            print ("error while connecting to postgres")
