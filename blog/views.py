import nltk
from django.shortcuts import render
from rest_framework import status

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd

from .apps import ApiConfig, VectorizerConfig

from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords.words('english')
import string

string.punctuation

def transform_text(text):
    text = text.lower()
    text = nltk.wordpunct_tokenize(text)
    # removing special character and appending it into y
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

class PostView(APIView):
    serializer_class = PostSerializer

    def get(self, request):
        query = Post.objects.all()
        serializer = PostGetSerializer(query, many=True)
        data = []
        for post in serializer.data:
            post_like = Like.objects.filter(
                post=post['id']).filter(like=True).count()
            mylike = Like.objects.filter(post=post['id']).filter(
                user=request.user).first()
            if mylike:
                post['like'] = mylike.like
            else:
                post['like'] = False
            post['totallike'] = post_like
            comment_query = Comment.objects.filter(
                post=post['id']).order_by('-id')
            comment_serializer = CommentSerializer(comment_query, many=True)
            comment_data = []
            for comment in comment_serializer.data:
                reply_query = Reply.objects.filter(comment=comment['id'])
                reply_serializer = ReplySerializer(reply_query, many=True)
                comment['reply'] = reply_serializer.data
                comment_data.append(comment)
            post['comment'] = comment_data
            data.append(post)
        return Response(data)

    def post(self, request, format=None):

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data['content']
            naiveModel = ApiConfig.model
            naiveVect = VectorizerConfig.model
            convertString = str(message)
            message = convertString
            data = [message]
            print(data)


            vect = naiveVect.transform(data).toarray()


            my_prediction = naiveModel.predict(vect)
            print(my_prediction)
            serializer.save()
            result = {
                "data": serializer.data,
                "pred": my_prediction

            }

            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddALike(APIView):

    # authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        try:
            data = request.data
            c_user = request.user
            post_id = data['id']
            post_obj = Post.objects.get(id=post_id)
            like_obj = Like.objects.filter(
                post=post_obj).filter(user=c_user).first()
            if like_obj:
                old_like = like_obj.like
                like_obj.like = not old_like
                like_obj.save()
            else:
                Like.objects.create(
                    post=post_obj,
                    user=c_user,
                    like=True,
                )
            response_msg = {'error': False}
        except:
            response_msg = {'error': True}
        return Response(response_msg)


class AddComment(APIView):

    # authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        try:
            c_user = request.user
            data = request.data
            post_id = data['postid']
            post_obj = Post.objects.get(id=post_id)
            comment_text = data['comment']
            Comment.objects.create(
                user=c_user,
                post=post_obj,
                title=comment_text,
            )
            response_msg = {'error': False, "postid": post_id}
        except:
            response_msg = {'error': True}
        return Response(response_msg)


class AddReply(APIView):
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        try:
            c_user = request.user
            data = request.data
            comment_id = data['commentid']
            comment_obj = Comment.objects.get(id=comment_id)
            replytext = data['replytext']
            Reply.objects.create(
                user=c_user,
                comment=comment_obj,
                title=replytext,
            )
            response_msg = {'error': False}
        except:
            response_msg = {'error': False}
        return Response(response_msg)
