from celery import shared_task
from detection.models import *
from django.shortcuts import render
from detection.core.ProcessResearchDocument import *
from detection.views import *
from sentence_transformers import SentenceTransformer


# model = SentenceTransformer("all-MiniLM-L6-v2")
model = 0

def UniversityUploadProcess(university):
    pending_research_papers = ResearchDocument.objects.filter(university_id=university, is_processed=False)
    # print("research documents were uploaded by university")
    # print("there are ", pending_research_papers.count(), " unprocessed documents")
    print("there are ", len(pending_research_papers), " paper")

    return pending_research_papers

# @shared_task
def UniversityUploadProcessDocuments(university):
    pending_research_papers = UniversityUploadProcess(university)
    for index, pending_research_paper in enumerate(pending_research_papers):
        text = ResearchDocumentParse(pending_research_paper)
        sentences, sentences_objs = ResearchDocumentStoreTextSentences(pending_research_paper, text)
        if len(sentences) != len(sentences_objs):
            print("sentences and sentences_objs length are not equal")
        sentence_vectors = ResearchDocumentGenerateTextVector(pending_research_paper, model, sentences, sentences_objs)
        pending_research_paper.is_processed = True
        pending_research_paper.save()

    return pending_research_papers

    