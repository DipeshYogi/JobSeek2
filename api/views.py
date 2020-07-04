from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import psycopg2
from api.serializers import recomm_serializer
from rest_framework import status
from rest_framework.renderers import JSONRenderer

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


try:
    conn = psycopg2.connect(   user='lvdbzgnnnthckg',
                                    password= '7ef0652e2f717ff49f5369871183b2dcdd15d9c52a7c55fcef98779d410dcb10',
                                    host = 'ec2-184-72-237-95.compute-1.amazonaws.com',
                                    port = '5432',
                                    database = 'd32b9rckhe5166',

                                    )

    cursor = conn.cursor()
    print ('Connected')


except (Exception, psycopg2.Error) as error:
                    print ("error while connecting to postgres")


class GetConn(APIView):

    def get(self,request):
        cursor.execute('Select * from portal_jobs where owner_id=1')
        rec = cursor.fetchall()
        cursor.execute('select username from auth_user where id=1')
        usr_name = cursor.fetchone()

        return Response ({'user':usr_name,'Jobs posted':rec})

class GetRecomm(APIView):
    """Get recommendation for a Profile"""
    serializer_class = recomm_serializer
    renderer_classes = [JSONRenderer]

    def get(self,request):
        n1 = self.serializer_class(data=request.data)
        if n1.is_valid():
            n1 = n1.validated_data.get('n1')

            cursor.execute('select p_skills, s_skills, img, exp from  users_profile where user_id = %s', (n1,))
            rec = cursor.fetchall()

            rec = pd.DataFrame(rec, columns=['p_skills','s_skills','img','exp'])
            rec['id'] = n1


            cursor.execute('select id, title, req_skills, exp from portal_jobs where owner_id <> %s', (n1,))
            jobs = cursor.fetchall()
            jobs = pd.DataFrame(jobs, columns=['id', 'title', 'req_skills', 'exp'])

            users_dta = rec['p_skills']+ ' '+rec['s_skills']
            jobs_dta = jobs['title']+ ' '+jobs['req_skills']

            jobid = jobs['id']

            data1 = pd.concat([users_dta, jobs_dta]).reset_index(drop=True)
            count = CountVectorizer(stop_words='english', ngram_range=(1, 2))
            count = CountVectorizer(stop_words='english', ngram_range=(1, 2))
            mat = count.fit_transform(data1)
            score = linear_kernel(mat,mat)
            req_score = score[0]
            req1_score = list(enumerate(req_score))
            req1_score = req1_score[1:]
            req1_score = pd.DataFrame(req1_score,columns=['index','score'])
            req1_score['JobId'] = jobid
            req1_score = req1_score.sort_values(by='score', ascending=False)
            req1_score = req1_score[req1_score['score']>=1]['JobId']
            req1_score = tuple(req1_score)
            #print(req1_score)

            cursor.execute('select * from portal_jobs where id in %s',(req1_score,))
            recomm_jobs = cursor.fetchall()

            cursor.execute('select username from auth_user where id = %s', (n1,))
            name = cursor.fetchall()

            return Response(recomm_jobs)
        else:
            return Response(n1.errors, status = status.HTTP_400_BAD_REQUEST)
