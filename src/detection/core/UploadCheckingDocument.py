from celery import shared_task
from detection.models import *
from django.shortcuts import render
from detection.core.ProcessCheckingDocument import *
from detection.views import *
from sentence_transformers import SentenceTransformer


# model = SentenceTransformer("all-MiniLM-L6-v2")
model = 0

# @shared_task
def InstructorUploadProcessCheckingDocuments(instructor, checking_document):

    text = CheckingDocumentParse(checking_document)
    sentences, sentences_objs = CheckingDocumentStoreTextSentences(checking_document, text)
    if len(sentences) != len(sentences_objs):
        print("sentences and sentences_objs length are not equal")
    sentence_vectors_obj = CheckingDocumentGenerateTextVector(checking_document, model, sentences, sentences_objs)
    checking_document.is_processed = True
    checking_document.save()

    return sentence_vectors_obj