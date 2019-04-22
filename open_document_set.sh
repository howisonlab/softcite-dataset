# find ../../ -name "*PMC3365791*" -execdir atom -n=false {} \;
# find ../../ -name "PMC3365791.pdf" -execdir explorer \"{}\" \;
find ../../ -name "*$1*" -print
find ../../ -name "*$1.tei.xml" -execdir atom -n=false {} \;
find ../../ -name "*$1.ttl*" -execdir atom -n=false {} \;
find ../../ -name "*$1.pdf*" -execdir FoxitReader -n=false {} \;
# posix-extended
