FROM rocker/binder

RUN apt-get update && apt-get install -y \
    libpython3-dev \
    python3-dev \
    python3-rdflib \
    python3-virtualenv \
    python3-pip \
    python3-pytest \
    python3-setuptools \
    vim \
    less


RUN install2.r --error \
      --deps TRUE \
      reticulate

# Set up virtual env (runs as root)
ENV VIRTUAL_ENV=/home/rstudio/.virtualenvs/r-reticulate
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./requirements.R .
RUN Rscript ./requirements.R

RUN installGithub.r datadotworld/dwapi-r
RUN installGithub.r datadotworld/data.world-r


RUN install2.r --error \
      --deps TRUE \
      here \
      BiocManager

RUN Rscript -e 'BiocManager::install("Biostrings")'


# Ensure that rstudio can access the virtual_env
RUN chown -R rstudio:rstudio $VIRTUAL_ENV

