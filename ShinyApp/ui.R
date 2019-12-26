library(shiny)
library(shinythemes)
library(readr)
library(ggplot2)
library(stringr)
library(dplyr)
library(DT)
library(tools)
library(prophet)
library(RSNNS)
library(forecast)
library(readxl)
library(lubridate)
library(zoo)
library(dygraphs)
library(xts) 

# Define UI for application that plots features of movies
ui <- fluidPage(
  theme=shinytheme('cosmo'),
  ##titlePanel("Forecasting"),
  
  navbarPage(title = 'DSO 522 Forecasting'
  ),
  
  img(src = "https://www.mbamission.com/blog/wp-content/uploads/2016/11/USC-Marshall.jpg", height = "90px"),
  
  
  
  # Sidebar layout with a input and output definitions
  sidebarLayout(
    
    # Inputs
    sidebarPanel(
      
      h3("Load File (Only csv files and only time series per day)"),      
      
      fileInput("file1", "Choose CSV File",
                accept = c(
                  "text/csv",
                  "text/comma-separated-values,text/plain",
                  ".csv")),
      
      checkboxInput("header", "Header", TRUE),
      
      h3("Select Variables"),      # Third level header: Plotting
      
      # Select variable for date 
      selectInput(inputId = "datevar", 
                  label = "Date (format:YYYY-MM-DD):",
                  choices = names(df)),
      
      # Select variable for Time Series 
      selectInput(inputId = "tsvar", 
                  label = "Time Series:",
                  choices = names(df)),
      
      # Set forecasting horizon
      sliderInput(inputId = "horizon", 
                  label = "Days ahead for forecasting:", 
                  min = 0, max = 100, 
                  value = 30),
      #Parameters
      h3("Select Parameters"), 
      sliderInput(inputId = "train.size", 
                  label = "Training sample size(%):", 
                  min = 0, max = 100, 
                  value = 80),
      
      #Models
      h3("Select Models"), 
      selectInput(inputId = "mod", 
                  label = "Select Models:",
                  choices = c('Seasonal Naive','Smoothing','Auto Arima','Prophet')),
      
      
      
      h5("Built by"),
      
      img(src = "https://media.licdn.com/dms/image/C5603AQECZWV3InECbw/profile-displayphoto-shrink_200_200/0?e=1580947200&v=beta&t=MHHTW1FdPkBySJMLvJsn7M_HchrLVf65IhAzu5K1cn8", height = "90px"),
      img(src = "https://media.licdn.com/dms/image/C5603AQGaICLb7JtTtw/profile-displayphoto-shrink_200_200/0?e=1580947200&v=beta&t=STYSGyJasi9QIEiJsiTDFtkhY09Yr8RYd0PsMJh4vkY", height = "90px"),
      img(src = "https://media.licdn.com/dms/image/C5603AQEi8sYMs9Lj3Q/profile-displayphoto-shrink_200_200/0?e=1580947200&v=beta&t=VlNb6ba9HPoTS8G96ybtX-aVCRs5_gGMmiIJANZPxIU", height = "90px"),
      img(src = "https://media.licdn.com/dms/image/C5603AQFZ23hF0BH_Qw/profile-displayphoto-shrink_200_200/0?e=1580947200&v=beta&t=V2n7TwwzIUmH6yO_eIfJFAgdI0YxZChDwPOGUZMhRCs", height = "90px"),
      img(src = "https://media.licdn.com/dms/image/C5103AQHXf5iWcA871A/profile-displayphoto-shrink_200_200/0?e=1580947200&v=beta&t=yMVYlCI1TS_51w79naMA3Z5IMjgh8ZmPwBQWyJoY08k", height = "90px")
      
      
      
      
    ),
    
    # Output:
    mainPanel(
      
      ##img(src = "https://www.mbamission.com/blog/wp-content/uploads/2016/11/USC-Marshall.jpg", height = "90px"),
      
      tabsetPanel(id = "tabspanel", type = "tabs",
                  tabPanel(title = "File Content", 
                           tableOutput("contents")),
                  tabPanel(title = "Plot", 
                           dygraphOutput(outputId = "ts_dygraph")),
                  tabPanel(title = "Evaluation", 
                           tableOutput("evaluation")),
                  tabPanel(title = "Evaluation Plot",
                           plotOutput("forecast_dygraph")),
                  tabPanel(title = "Forecasting Results", 
                           tableOutput("forecasting")),
                  tabPanel(title="Forecasting Plot",
                           dygraphOutput("dygraph"))
                  
                  
                  
      )
    )
  )
)