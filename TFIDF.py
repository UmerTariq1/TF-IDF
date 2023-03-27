from dataHandler import Data_Handler

import math

class TFIDF_custom_class:

    '''
    How to use this class:


    If you dont have the index files:
        2) create an object of this class ( self.tfidf_obj = TFIDF_custom_class(data = data ). refer to __init__ method for further details (inc data format)
        3) call the createTfandIDF method ( self.tfidf_obj.createTfandIDF() ). you can save the data if you want by passing saveFile=True. see the arguments for further details
        After this go to the general steps below

    If you have the index files:
        2.1) load the tf file using the data_handler class ( self.data_handler.read_tf(filename+".tf") )
        2.2) load the idf file using the data_handler class ( self.data_handler.read_tf(filename+".idf") )
        3) create an object of this class ( self.tfidf_obj = TFIDF_custom_class(data=data, tf = tf, idf = idf) )
        After this go to the general steps below

    General steps:
        4) call the compute_tfidf method ( self.tfidf_obj.compute_tfidf() )
        5) call get_topN_results ( self.tfidf_obj.get_topN_results(query, N) ) using the query and the number of results you want. query argument is a single query string. N is an integer
        

    
    
    '''

    def __init__(self, data, tf={}, idf={}):
        '''
        initialize the class

        @args:
            data : dictionary. key will be the doc_id (id from corpus , and value will be a dictionary with index, headline and text            

            tf: [dictionary] : dictionary with key as the doc_id and value as a dictionary with key as the term and value as the tf of that term in that document : optional argument. dont pass if you want to create new tf. but if you do pass then also pass the idf
            idf: [dictionary] : dictionary with key as the term and value as the idf of that term : optional argument. dont pass if you want to create new idf. but if you do pass then also pass the tf

        
        '''
        self.data = data      # filled in read_and_process_data : dictionary :key will be the doc_id (id from corpus , and value will be a dictionary with index, headline and text headline will the headline from corpus and will be an empty list if there is no headline. otherwise it will be a list of words in the headline text will be a list of lists. of all the text in p tag from corpus.

        self.num_docs = len(data) # number of documents in the collection. will be 0 if index is loaded from the file
        
        self.idf = idf      # filled in compute_idf. It is a dictionary with key as the term and value as the idf of that term
        self.term_doc_freq = {} # filled in getTermDocumentCount. term_doc_freq is a dictionary with key as the term and value as the number of documents that contain the term t
        self.tf = tf        # filled in compute_tf. A nested dictionary. key will be the doc_id and value will be a dictionary with key as the term and value as the tf of that term in that document
        self.tfidf = {}        # filled in compute_tfidf. 

        self.data_handler = Data_Handler()


    def getTermDocumentCount(self, processHeadline):
        '''
        Returns a dictionary with key as the term and value as the number of times the term occurs in the collection
        @args:
            processHeadline: [boolean] : if True then the headline will be processed and the terms in the headline will be counted as well.
        @returns:
            term_doc_count: [dictionary] : dictionary with key as the term and value as the number of documents that contain the term t
        '''
        
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
    
    def compute_idf(self, processHeadline=True, saveFile=True, collectionName="collection", output_dir="output/"):
        '''
        Compute the inverse document frequency (idf) of the stemmed words/terms/tokens:
        
        this function should populate the self.idf dictionary
        self.idf is a dictionary with key as the term and value as the idf of that term
        self.idf = {"term1": idf1, "term2": idf2, ...}

        @args:
            processHeadline: [boolean] : if True then the headline will be processed and the terms in the headline will be counted as well.
            saveFile : [boolean] : if True then the tf will be saved in the output directory
        @returns:
            self.idf: [dictionary] : dictionary with key as the term and value as the idf of that term
            also saves the data in the self.idf variable and output file if saveFile=True. you can read it from there using the data_handler class read_idf function.
        '''

        self.term_doc_count = self.getTermDocumentCount(processHeadline)  # term_doc_count freq = number of documents that contain the term t

        self.idf = {}    

        for term, term_doc_count in self.term_doc_count.items():
            self.idf[term] = math.log(self.num_docs / term_doc_count)    

        if saveFile:
            self.data_handler.save_dict(self.idf, output_dir + collectionName + ".idf")   
            return self.idf
        else:
            return self.idf
        
    def compute_tf(self, processHeadline=True, saveFile = True, collectionName="collection", output_dir="output/"):
        '''
        computer the term frequency (tf) of the stemmed words per document:
        
        tf (term,doc) = number of times term t appears in document d / maxOccurrences

        where maxOccurrences is the number of times that the most frequent term of the document occurs in the document

        @args:
            processHeadline: [boolean] : if True then the headline will be processed and the terms in the headline will be counted as well.
            saveFile : [boolean] : if True then the tf will be saved in the output directory
        @returns:
            self.tf: [dictionary] : dictionary with key as the doc_id and value as a dictionary with key as the term and value as the tf of that term in that document
            also saves the data in the self.tf variable and output file if saveFile=True. you can read it from there using the data_handler class read_tf function.

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
        if saveFile:
            self.data_handler.save_dict(self.tf, output_dir + collectionName + ".tf")
            return self.tf
        else:
            return self.tf
        
    def compute_tfidf(self, processHeadline=True):
        '''
        using self.tf and self.idf, compute the tfidf for each term in each document. store the result in self.tfidf
        
        formula:
            tf-idf (term,doc) = tf (term,doc) * idf (term)

        @args:
            processHeadline: [boolean] : if True then the headline will be processed and the terms in the headline will be counted as well.

        @returns:
            None (saves the data in the self.tfidf variable)
        '''

        self.tfidf = {}

        for doc_id, doc_data in self.tf.items():
            for term, tf in doc_data.items():
                if doc_id not in self.tfidf:
                    self.tfidf[doc_id] = {}
                self.tfidf[doc_id][term] = tf * self.idf[term]

    def get_query_vector(self, query_terms):
        '''
        given a list of query terms, return the query vector

        @args:
            query_terms: [str] : list of terms of query. can send through query.split()
        @return:
            query_vector: a dictionary with key as the term and value as the tf-idf of that term in the query
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

    def get_scores_for_query(self, query_vector):
        '''
        given a query vector, return the similarity scores for each document in the collection

        @args:
            query_vector: a dictionary with key as the term and value as the tf-idf of that term in the query
        @return:
            scores: [(doc_id, score)] : list of tuples with doc_id and score for that document    

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
    
    def createTfandIDF(self, processHeadline=True, saveFile = True, collectionName="collection", output_dir="output/"):
        '''
        wrapper function to compute tf and idf. 

        @args:
            processHeadline: [boolean] : if True then the headline will be processed and the terms in the headline will be counted as well.
            saveFile : [boolean] : if True then the tf and idf will be saved in the output directory
            output_dir: [string] : output directory where the index files will be stored : optional argument. used to save the tf and idf files in case they are created.
            collectionName: [string] : name of the collection : optional argument. used to save the tf and idf files in case they are created.
        @returns:
            self.tf: [dictionary] : dictionary with key as the doc_id and value as a dictionary with key as the term and value as the tf of that term in that document
            self.idf: [dictionary] : dictionary with key as the term and value as the idf of that term in the collection
            also saves the data 

        '''
        return self.compute_tf(processHeadline, saveFile,collectionName, output_dir) , self.compute_idf(processHeadline, saveFile,collectionName, output_dir)


    def get_topN_results(self, query, N=10):
        '''
        given a query, return the top N results

        @args:
            query: string : query to search
            N: [int] : number of results to return
        @returns:
            top_docs_and_scores: [(doc_id, score)] : list of tuples with doc_id and score for that document
        '''

        query_terms_list = query.split()

        # Preprocess the query terms
        query_terms = self.data_handler.preprocess_query(query_terms_list)
        
        query_vector = self.get_query_vector(query_terms)

        # Get the scores for each document for this query
        scores = self.get_scores_for_query(query_vector)
        
        # Sort the documents by score
        scores.sort(key=lambda x: x[1], reverse=True)

        # Filter out documents with score of 0 and less than N documents
        top_docs_and_scores = [(doc_id, score) for doc_id, score in scores if score > 0][:N]

        return top_docs_and_scores