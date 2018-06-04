FROM openanalytics/r-base

MAINTAINER James Howison "jhowison@ischool.utexas.edu"

# system libraries of general use
RUN apt-get update && apt-get install -y \
    sudo \
    pandoc \
    pandoc-citeproc \
    libcurl4-gnutls-dev \
    libcairo2-dev \
    libxt-dev \
    libssl-dev \
    libssh2-1-dev \
    libssl1.0.0 \
    libxml2-dev


# basic shiny functionality
RUN R -e "install.packages(c('rmarkdown', 'shiny'), repos='https://cloud.r-project.org/')"

RUN R -e "install.packages(c('xml2'), repos='https://cloud.r-project.org/')"

# specific dependencies
RUN R -e "install.packages(c('tidyverse', 'shinydashboard'), repos='https://cloud.r-project.org/')"

RUN R -e "install.packages(c('data.world'), repos='https://cloud.r-project.org/')"

# copy the app to the image
RUN mkdir /root/softcite-dashboard
COPY softcite-dashboard /root/softcite-dashboard

COPY Rprofile.site /usr/lib/R/etc/
# COPY .Renviron /usr/lib/R/etc/

EXPOSE 3838

CMD ["R", "-e", "shiny::runApp('/root/softcite-dashboard')"]
