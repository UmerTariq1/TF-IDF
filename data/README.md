The complete data file (nyt199501.xml) was too big (45 mb) to be uploaded on github so its compressed file is uploaded here. 
nytsmall is just a small version of the original data.

The data is given in the Extensible Markup Language format (XML), which is a format in- tended to be both human-readable and machine-readable. XML documents contain elements which are defined by opening and closing tags:

<HEADLINE>MIAMI QB COSTA IS HURRICANE TESTED</HEADLINE>

XML documents have a tree-like structure. Elements (or nodes) can have child nodes or sib- lings. For instance (see example on next page), the DOC tag has the child HEADLINE, DATELINE and TEXT. TEXT has several child nodes named P (for parapgraph - in general, XML tags are
not pre-defined, they can be defined for a data set as needed).

```
<DOC id="NYT_ENG_19950101.0001" type="story">

   <HEADLINE>MIAMI QB COSTA IS HURRICANE TESTED</HEADLINE>

  <DATELINE>MIAMI  (BC-FBC-MIAMI-COSTA-TEX)</DATELINE>
  
  <TEXT>
  
    <P>
      As a native of Philadelphia, the town of brotherly hate
  
      where fans have booed Santa Claus, Mike Schmidt and Julius Erving,
  
     Frank Costa should have been prepared.
    </P>
  
    <P>
      He wasn’t.
    </P>
  
  </TEXT>

</DOC>
```

In the above example, the DOC element has two attributes (id and story). For our implemen- tation, we disregard the type of the document, but the document id is of great importance, as our search engine will return document ids as the results of a search.
It is sufficient to use the following insight to process the data:
Each document begins with a line
<DOC id="...">
followed by the actual text of the document Documents end with a line </DOC>

For the computation of the tf.idf scores, only the text enclosed by the XML-tags HEADLINE, TEXT and P should be considered; the XML-tags themselves as well as the text enclosed by DATELINE should be ignored. The complete document collection is enclosed by a DOCS tag; this tag should be ignored as well.


Note that in the data the structure was generally followed that document will be inside the TEXT->P tag. but for some documents there isnt any P tag and the document text is directly placed in the TEXT tag. This is handled by data handler class 
