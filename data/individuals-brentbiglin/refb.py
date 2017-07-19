pmcid-citedFIXME: rdf:type citec:reference ;
    citec:full_quote FIXME ; # use triple quotes

    citec:on_pdf_page FIXME  ; # integer

    citec:spans_pages FIXME ; # true/false

    ca:isTargetOf
        [ rdf:type ca:CodeApplication ;
          ca:hasCoder "brentbiglin" ;
          ca:appliesCode [ rdf:type citec:reference_type ;
                           rdfs:label FIXME publication | user_guide | project_page | project_name ; # put one in triple quotes
                         ] ;
        ] ;
    ca:isTargetOf
        [ rdf:type ca:CodeApplication ;
          ca:hasCoder "brentbiglin" ;
          ca:appliesCode [ rdf:type citec:software_name ;
                           citec:isPresent FIXME ; # true/false
                           rdfs:label FIXME ; # use triple quotes
                         ] ;
        ] ;
    ca:isTargetOf
        [ rdf:type ca:CodeApplication ;
          ca:hasCoder "brentbiglin" ;
          ca:appliesCode [ rdf:type citec:version_number ;
                           citec:isPresent FIXME ; # true/false
                           rdfs:label FIXME ; # use triple quotes
                         ] ;
        ] ;
    ca:isTargetOf
        [ rdf:type ca:CodeApplication ;
          ca:hasCoder "brentbiglin" ;
          ca:appliesCode [ rdf:type citec:version_date ;
                           citec:isPresent FIXME ; # true/false
                           rdfs:label FIXME ; # use triple quotes
                         ] ;
        ] ;
    ca:isTargetOf
        [ rdf:type ca:CodeApplication ;
          ca:hasCoder "brentbiglin" ;
          ca:appliesCode [ rdf:type citec:url ;
                           citec:isPresent FIXME ; # true/false
                           rdfs:label FIXME ; # use triple quotes
                         ] ;
        ] ;
    ca:isTargetOf
        [ rdf:type ca:CodeApplication ;
          ca:hasCoder "brentbiglin" ;
          ca:appliesCode [ rdf:type citec:creator ;
                           citec:isPresent FIXME ; # true/false
                           rdfs:label FIXME ; # use triple quotes
                         ] ;
        ] ;
.
