pmcidFIXME: rdf:type citec:in_text_mention ; # use in text mention name
    citec:full_quote FIXME ; # use triple quotes

    citec:on_pdf_page FIXME  ; # integer

    citec:spans_pages FIXME ; # true/false

    ca:isTargetOf
        [ rdf:type ca:CodeApplication ;
          ca:hasCoder "brentbiglin" ;
          ca:appliesCode [ rdf:type citec:mention_type ;
                           rdfs:label FIXME software | algorithm |  hardware | other ; # put one in triple quotes
                           ca:certainty FIXME1-10 ; # integer
                           ca:memo FIXME ; # use triple quotes
                         ] ;
        ] ;
    ca:isTargetOf
        [ rdf:type ca:CodeApplication ;
          ca:hasCoder "brentbiglin" ;
          ca:appliesCode [ rdf:type citec:software_was_used ;
                           citec:isPresent FIXME; # true/false
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
    citec:has_reference pmcid-citedFIXME: ; # name reference like pmcid-cited:a2004-40-NAT_GENET_Author-YYYY, no quotes
.
