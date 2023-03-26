from dataHandler import Data_Handler

import math

class TFIDF_custom_class:

    def __init__(self, data=[], tf={}, idf={}, collectionName="collection", output_dir="output/"):

        self.data = data      # will be empty if data is loaded from file. filled in read_and_process_data : dictionary :key will be the doc_id (id from corpus , and value will be a dictionary with index, headline and text headline will the headline from corpus and will be an empty list if there is no headline. otherwise it will be a list of words in the headline text will be a list of lists. of all the text in p tag from corpus.

        self.num_docs = len(data) # number of documents in the collection. will be 0 if index is loaded from the file
        
        self.idf = idf      # filled in compute_idf. It is a dictionary with key as the term and value as the idf of that term
        self.term_doc_freq = {} # filled in getTermDocumentCount. term_doc_freq is a dictionary with key as the term and value as the number of documents that contain the term t
        self.tf = tf        # filled in compute_tf. A nested dictionary. key will be the doc_id and value will be a dictionary with key as the term and value as the tf of that term in that document
        self.tfidf = {}        # filled in compute_tfidf. 

        self.data_handler = Data_Handler()

        self.collectionName = collectionName

        self.output_dir = output_dir


    def getTermDocumentCount(self, processHeadline):
        '''
        Returns a dictionary with key as the term and value as the number of times the term occurs in the collection
        '''
        
        #term_doc_freq is a dictionary with key as the term and value as the number of documents that contain the term t
        term_doc_count = {}
        #iterate over all the documents and populate the term_doc_count dictionary
        for doc_id, doc_data in self.data.items():
            doc_terms = set()
            if processHeadline and doc_data['headline']:
                for term in doc_data['headline']:
                    if term not in doc_terms:
                        doc_terms.add(term)
                        if term not in term_doc_count:
                            term_doc_count[term] = 0
                        term_doc_count[term] += 1
                
            for paragraph in doc_data['text']:
                for term in paragraph:
                    if term not in doc_terms:
                        doc_terms.add(term)
                        if term not in term_doc_count:
                            term_doc_count[term] = 0
                        term_doc_count[term] += 1
        return term_doc_count
    
    # Compute the inverse document frequency (idf) of the stemmed words/terms/tokens:
    def compute_idf(self, processHeadline=True):
        '''
        this function should populate the self.idf dictionary
        self.idf is a dictionary with key as the term and value as the idf of that term
        self.idf = {"term1": idf1, "term2": idf2, ...}
        '''

        self.term_doc_count = self.getTermDocumentCount(processHeadline)  # term_doc_count freq = number of documents that contain the term t

        self.idf = {}    

        for term, term_doc_count in self.term_doc_count.items():
            self.idf[term] = math.log(self.num_docs / term_doc_count)    


        self.data_handler.save_dict(self.idf, self.output_dir + self.collectionName + ".idf")   

    #computer the term frequency (tf) of the stemmed words per document:
    def compute_tf(self, processHeadline=True):
        '''
        tf (term,doc) = number of times term t appears in document d / maxOccurrences

        where maxOccurrences is the number of times that the most frequent term of the document occurs in the document
        '''

        self.tf = {} # a nested dictionary. key will be the doc_id and value will be a dictionary with key as the term and value as the tf of that term in that document
        
        for doc_id, doc_data in self.data.items():
            doc_terms = {}
            if processHeadline and doc_data['headline']:
                for term in doc_data['headline']:
                    if term not in doc_terms:
                        doc_terms[term] = 0
                    doc_terms[term] += 1
                
            for paragraph in doc_data['text']:
                for term in paragraph:
                    if term not in doc_terms:
                        doc_terms[term] = 0
                    doc_terms[term] += 1
                
            max_occurrences = max(doc_terms.values()) #we only need the max value, not the term

            for term, tf in doc_terms.items():
                if doc_id not in self.tf:
                    self.tf[doc_id] = {}
                self.tf[doc_id][term] = tf / max_occurrences

        self.data_handler.save_dict(self.tf, self.output_dir + self.collectionName + ".tf")
        
    def compute_tfidf(self, processHeadline=True):
        '''
        tf-idf (term,doc) = tf (term,doc) * idf (term)
        '''

        self.tfidf = {}


        #using self.tf and self.idf, compute the tfidf for each term in each document. store the result in self.tfidf
        for doc_id, doc_data in self.tf.items():
            for term, tf in doc_data.items():
                if doc_id not in self.tfidf:
                    self.tfidf[doc_id] = {}
                self.tfidf[doc_id][term] = tf * self.idf[term]

    def get_query_vector(self, query_terms):
        '''
        query_terms is a list of terms of query. can send through query.split()
        '''

        query_vector  = {}
        for term in query_terms:
            if term not in self.idf:
                continue
            if term not in query_vector:
                query_vector[term] = 0
            query_vector[term] += 1
        for term in query_vector:
            query_vector[term] = query_vector[term] * self.idf[term]

        return query_vector

    def get_doc_vector(self, doc_id):
        '''
        doc_id is the id of the document
        '''
        return self.tfidf[doc_id]
    
    def get_scores_for_query(self, query_vector):
        '''
        query_terms is a list of terms of query. can send through query.split()
        '''

        scores = []
        for doc_id in list(self.data.keys()):
            dot_product = 0
            
            for term in query_vector:
                if term in self.tfidf[doc_id]:
                    dot_product += query_vector[term] * self.tfidf[doc_id][term]
            #compute the denominator
            query_norm = math.sqrt(sum([i**2 for i in query_vector.values()]))
            doc_norm = math.sqrt(sum([i**2 for i in self.tfidf[doc_id].values()]))

            # Compute the similarity score
            if query_norm == 0 or doc_norm == 0:
                each_score = 0
            else:
                each_score = dot_product / (query_norm * doc_norm)
            scores.append((doc_id, each_score))

        return scores
