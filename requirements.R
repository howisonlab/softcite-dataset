library(reticulate)

use_virtualenv("/home/rstudio/.virtualenvs/r-reticulate", required = T)

# install SciPy
# virtualenv_install("/home/rstudio/.virtualenvs/r-reticulate", "scipy")
# virtualenv_install("/home/rstudio/.virtualenvs/r-reticulate", "pandas")


# import SciPy (it will be automatically discovered in "r-reticulate")
# scipy <- import("scipy")
