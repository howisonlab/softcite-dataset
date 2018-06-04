## ui.R ##
library(shinydashboard)

dashboardPage(skin = "black",
  dashboardHeader(title = "Softcite"),
  dashboardSidebar(disable = TRUE),
  dashboardBody(
    # Boxes use row orientation
    fluidRow(
      
      #ouput stats as defined in server.r
      valueBoxOutput("num_articles"),
      valueBoxOutput("num_coders"),
      valueBoxOutput("num_mentions"),
      
      
      box(title = "Mention Composition",
          plotOutput("mention_compositions")),
      
      box(
        title = "Software Names by Number of Mentions",
        plotOutput("software_names_chart")
      )
  )
)
)