import fitz # pymupdf
import numpy as np
import io
from django.core.files.base import ContentFile
from detection.models import *
import re
from nltk.tokenize import sent_tokenize

def ResearchDocumentParse(document: ResearchDocument):
    """
    Parses and analyzes a research document, extracting text, images, and reference data.

    This function processes a research paper (PDF) to:
    - Extract all textual content and embedded images from each page.
    - Compute document-level statistics such as number of words, sentences, characters, pages, images, and references.
    - Identify the 'References' section and separate it from the main content.
    - Save all extracted information (images, references, parsed text, and basic stats) into related database models.

    Args:
        document (ResearchDocument): The research document instance containing file metadata and path.

    Returns:
        str: The main text of the document excluding the 'References' section.
        Returns an empty string if no 'References' section is found.

    Notes:
        - Uses PyMuPDF (`fitz`) for text and image extraction.
        - Automatically creates related database records for statistics, text, images, and references.
        - If the 'References' section is missing, an error record is logged.
    """


    no_of_pages = 0
    no_of_words = 0
    no_of_characters = 0
    no_of_sentences = 0
    no_of_references = 0
    size_of_document = 0
    no_of_images = 0
    images_list = list()
    find_references_word = "references"
    find_references_index = -1
    reference_text = ""
    original_text = ""

    text = ""
    doc_pdf = fitz.open(document.research_document_file.path)

    for page_number, page in enumerate(doc_pdf):
        image_list = page.get_images(full=True)

        for img_index, image_tuple in enumerate(image_list):

            xref = image_tuple[0]
            base_image = doc_pdf.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_file = ContentFile(image_bytes)

            filename = f"page_{page_number+1}_img_{img_index+1}.{image_ext}"

            research_document_images_obj = ResearchDocumentImages()
            research_document_images_obj.research_document_id = document
            research_document_images_obj.image.save(filename, image_file, save=False)
            research_document_images_obj.save()


        num_images_on_page = len(image_list)
        no_of_images += num_images_on_page
        images_list.append(image_list)
        no_of_pages += 1

        temp = page.get_text("text")
        text += temp

    # print("Document is ", text)

    no_of_words = len(text.split())
    no_of_characters = len(text)
    size_of_document = document.research_document_file.size    

    find_references_index = text.lower().rfind(find_references_word.lower())
    # print("last references found in ", find_references_index)

    if find_references_index == -1:
        error_obj = ResearchDocumentParseError()
        error_obj.research_document_id = document
        error_obj.parse_text = text
        error_obj.error_message = "There are no References section in the research paper"
        error_obj.save()
        return ""
    else:
        reference_text = text[find_references_index:]
        original_text = text[:find_references_index]

    # finding_references_list = re.split(r"\n[\{][0-9]+[\}]", reference_text)
    finding_references_list = re.split(r"\n\n", reference_text)

    print("there ", len(finding_references_list), " references")
    no_of_sentences = len(sent_tokenize(original_text))

    document_basic_stats_obj = ResearchDocumentBasicStats()
    document_basic_stats_obj.research_document_id = document
    document_basic_stats_obj.size_of_document = size_of_document
    document_basic_stats_obj.no_of_sentences = no_of_sentences
    document_basic_stats_obj.no_of_words = no_of_words
    document_basic_stats_obj.no_of_characters = no_of_characters
    document_basic_stats_obj.no_of_images = no_of_images
    document_basic_stats_obj.no_of_references = len(finding_references_list)
    document_basic_stats_obj.save()


    for index, reference_text in enumerate(finding_references_list):
        document_reference_obj = ResearchDocumentReferences()
        document_reference_obj.research_document_id = document
        document_reference_obj.index = index
        document_reference_obj.reference_text = reference_text
        print("reference length is ", reference_text)
        document_reference_obj.save()

    document_parse_text_obj = ResearchDocumentParseText()
    document_parse_text_obj.research_document_id = document
    document_parse_text_obj.parse_text = original_text
    document_parse_text_obj.save()


    print("orignal: ", original_text)
    print("reference: ", reference_text)

    return original_text

def ResearchDocumentGetSentencesFromText(document_extracted_text):
    """
    Tokenizes extracted document text into a list of sentences using natural language processing.

    Args:
        document_extracted_text (str): The full extracted text from the research document.

    Returns:
        list[str]: A list of sentences extracted from the text.

    Notes:
        - Uses NLTK's `sent_tokenize` for accurate sentence segmentation.
        - Provides better precision compared to manual regex-based sentence splitting.
    """

    # # Split on .\n, or !, ?, or newline not preceded by period
    # sentences = re.split(r'\.\n|[!?]\s+|(?<!\.)\n', document_extracted_text)
    # # Clean and filter
    # sentences = [s.strip() for s in sentences if s.strip()]
    # return sentences

    # More Accurate one
    sentences = sent_tokenize(document_extracted_text)
    return sentences

def ResearchDocumentStoreTextSentences(document, document_extracted_text):
    """
    Stores each sentence from the extracted research text as a separate record in the database.

    This function:
    - Splits the research paper text into sentences.
    - Saves each sentence in the `ResearchDocumentEnhancedText` model with its index.
    - Returns both the list of sentences and their corresponding database objects.

    Args:
        document (ResearchDocument): The research document being processed.
        document_extracted_text (str): The textual content extracted from the research paper.

    Returns:
        tuple[list[str], list[ResearchDocumentEnhancedText]]:
            - A list of extracted sentences.
            - A list of their respective saved database objects.

    Notes:
        - Prints confirmation messages after successful storage.
        - Essential for downstream processes like vectorization and semantic analysis.
    """

    sentences = ResearchDocumentGetSentencesFromText(document_extracted_text)
    sentences_objs = list()

    for index, sentence in enumerate(sentences):
        document_enhanced_text_obj = ResearchDocumentEnhancedText()
        document_enhanced_text_obj.research_document_id = document
        document_enhanced_text_obj.sentence_index = index
        document_enhanced_text_obj.sentence_enhanced_text = sentence
        document_enhanced_text_obj.save()
        sentences_objs.append(document_enhanced_text_obj)

    print("info: Document's text stored successfully")
    print("There are ", len(sentences_objs), " sentences")
    return sentences, sentences_objs


def ResearchDocumentGenerateTextVector(document, model, sentences, sentences_objs):
    """
    Generates vector embeddings for each sentence in a research document using a given NLP model.

    This function encodes each sentence into a numerical vector representation,
    which is then saved in the `ResearchDocumentTextVector` model alongside its related sentence record.

    Args:
        document (ResearchDocument): The document being analyzed.
        model: The sentence embedding model (e.g., SentenceTransformer or similar encoder).
        sentences (list[str]): List of sentences to be vectorized.
        sentences_objs (list[ResearchDocumentEnhancedText]): Corresponding sentence database objects.

    Returns:
        list: The list of generated sentence vectors (as NumPy arrays or lists).

    Notes:
        - Each sentence vector is converted to a list before storage for database compatibility.
        - Enables semantic similarity analysis, document comparison, and other NLP-based features.
    """

    sentences_vectors = model.encode(sentences)
    print("vectors: ", sentences_vectors, "\n\n")

    for index, sentences_vector in enumerate(sentences_vectors):
        research_document_sentence_vector_obj = ResearchDocumentTextVector()
        research_document_sentence_vector_obj.research_document_id = document
        research_document_sentence_vector_obj.research_document_enhanced_text_id = sentences_objs[index]
        research_document_sentence_vector_obj.text_vector = sentences_vector.tolist()
        research_document_sentence_vector_obj.save()
    
    return sentences_vectors
