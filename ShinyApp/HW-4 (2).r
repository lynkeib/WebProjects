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

# Define server function required to create the scatterplot
server <- function(input, output, session) {
  df <- reactive({
    req(input$file1)
    read.csv(input$file1$datapath, header = input$header)
  })
  
  observeEvent(df(), {
    updateSelectInput(session, "datevar", choices=colnames(df()))
    updateSelectInput(session, "tsvar", choices=colnames(df()), selected = colnames(df())[2])
  })
  
  
  # Create scatterplot object the plotOutput function is expecting 
  output$ts_dygraph <- renderDygraph({
    data=df()
    data[,input$datevar]=as.Date(data[,input$datevar])
    data$Date=as.Date(floor_date(data[,input$datevar], "month"))
    data$y=as.numeric(data[,input$tsvar])
    data=data%>%group_by(Date)%>%summarize(Monthly_y=sum(y))
    
    don <- xts(x = data$Monthly_y, order.by = data$Date)
    
    dygraph(don,main="Monthly Data") %>%
      dyOptions(labelsUTC = TRUE, fillGraph=TRUE, fillAlpha=0.1, drawGrid = FALSE, colors="#D8AE5A") %>%
      dyRangeSelector() %>%
      dyCrosshair(direction = "vertical") %>%
      dyHighlight(highlightCircleSize = 5, highlightSeriesBackgroundAlpha = 0.2, hideOnMouseOut = FALSE)  %>%
      dyRoller(rollPeriod = 1)
  
  })
  
  
  #Create file content table
  output$contents <- renderTable({
    # input$file1 will be NULL initially. After the user selects
    # and uploads a file, it will be a data frame with 'name',
    # 'size', 'type', and 'datapath' columns. The 'datapath'
    # column will contain the local filenames where the data can
    # be found.
    #inFile <- input$file1
    
    if (is.null(df()))
      return(NULL)
    
    df()
  })

  
  output$evaluation <- renderTable({
    ####code for modeling'data=df()[,c(input$datevar,input$tsvar)]
    data=df()[,c(input$datevar,input$tsvar)]
    names(data)=c("ds","y")
    data$ds=format(as.Date(data$ds))
    
    train.data=df()[1:ceiling(nrow(df())*input$train.size/100),c(input$datevar,input$tsvar)]
    test.data=df()[(ceiling(nrow(df())*input$train.size/100)+1):nrow(df()),c(input$datevar,input$tsvar)]
    names(train.data)=c("ds","y")
    names(test.data)=c("ds","y")
    train.data$ds=format(as.Date(train.data$ds))
    test.data$ds=format(as.Date(test.data$ds))
    
    day1=as.Date(first(train.data$ds))
    dayend=as.Date(last(test.data$ds))
    ts.train=ts(train.data$y,start = c(year(day1), as.numeric(format(day1, "%j"))), frequency = 365)
    ts.test=ts(test.data$y,end=c(year(dayend),as.numeric(format(dayend, "%j"))+1), frequency = 365)
    ts.y=ts(data$y,start = c(year(day1), as.numeric(format(day1, "%j"))), frequency = 365)
    
    # Function that returns Root Mean Squared Error
    rmse <- function(error)
    {
      sqrt(mean(error^2))
    }
    
    # Function that returns Mean Absolute Error
    mae <- function(error)
    {
      mean(abs(error))
    }
    
      if (input$mod == 'Seasonal Naive') {
       
        forecast=snaive(ts.train,h=length(ts.test))
        results=data.frame(accuracy(forecast,test.data$y))
      } else if(input$mod=='Smoothing') {
        m_smooth <- ets(ts(train.data$y), damped = T)
        forecast <- forecast(m_smooth, h=nrow(test.data))
        forecast$ds=format(forecast$ds)
        
        results=data.frame(accuracy(forecast,test.data$y))
    
      } else if(input$mod=='Prophet'){
        m_prophet <- prophet(train.data,yearly.seasonality = T,weekly.seasonality = T,
                             daily.seasonality = T, seasonality.prior.scale = 24)
        future <- make_future_dataframe(m_prophet, periods = (100-input$train.size)*nrow(df())/100)
        forecast <- predict(m_prophet, future)
        forecast$ds=format(forecast$ds)
        error= forecast[(ceiling(nrow(df())*input$train.size/100)+1):nrow(df()),'yhat']-test.data$y
        
        results=data.frame("RMSE"=rmse(error),"MAE"=mae(error), "Training %"=paste0(input$train.size,"%"),
                           "Count Train"=nrow(train.data),"Count Test"=nrow(test.data), "Count Forecast"=nrow(forecast),
                           "Count df()"=nrow(df()))
      } else if(input$mod=='Auto Arima'){
        #M3 Auto Arima
        M3=auto.arima(ts.train,seasonal = TRUE, approximation = FALSE)
        forecast=forecast(M3,h=length(ts.test))

        results=data.frame(accuracy(forecast,test.data$y))
      }

  })
  
  output$forecast_dygraph <- renderPlot({
    ####code for modeling
    data=df()[,c(input$datevar,input$tsvar)]
    names(data)=c("ds","y")
    data$ds=format(as.Date(data$ds))
    
    train.data=df()[1:ceiling(nrow(df())*input$train.size/100),c(input$datevar,input$tsvar)]
    test.data=df()[(ceiling(nrow(df())*input$train.size/100)+1):nrow(df()),c(input$datevar,input$tsvar)]
    names(train.data)=c("ds","y")
    names(test.data)=c("ds","y")
    train.data$ds=format(as.Date(train.data$ds))
    test.data$ds=format(as.Date(test.data$ds))
    
    day1=as.Date(first(train.data$ds))
    dayend=as.Date(last(test.data$ds))
    ts.train=ts(train.data$y,start = c(year(day1), as.numeric(format(day1, "%j"))), frequency = 365)
    ts.test=ts(test.data$y,end=c(year(dayend),as.numeric(format(dayend, "%j"))+1), frequency = 365)
    ts.y=ts(data$y,start = c(year(day1), as.numeric(format(day1, "%j"))), frequency = 365)
    
    if (input$mod == 'Seasonal Naive') {
      #M1 Seasonal Naive
      M1=snaive(ts.train,h=length(ts.test))
      autoplot(ts.y) +theme_bw() +autolayer(M1$mean)+
        xlab("Year")+ ylab("Y")+
        ggtitle("Naive Exponential Smoothing Model")
   
      
    } else if(input$mod=='Smoothing') {
      #M2 Smoonthing
      m_smooth <- ets(ts(train.data$y), damped = T)
      forecast <- forecast(m_smooth, h=nrow(test.data))
      
      yhat=ts(forecast$mean,end=c(year(dayend),as.numeric(format(dayend, "%j"))+1), frequency = 365)
      
      
      autoplot(ts.y) +theme_bw() +autolayer(yhat)+
        xlab("Year")+ ylab("Y")+
        ggtitle("Smoothing Model")
      
    } else if(input$mod=='Prophet'){
      #M2 Prophet
      m_prophet <- prophet(train.data,yearly.seasonality = T,weekly.seasonality = T,
                           daily.seasonality = T, seasonality.prior.scale = 24)
      future <- make_future_dataframe(m_prophet, periods = (100-input$train.size)*nrow(df())/100)
      forecast <- predict(m_prophet, future)
      forecast$ds=format(forecast$ds)
      
      new=forecast[(nrow(train.data)+1):nrow(data),c('ds','yhat')]
      new$ds=as.Date(new$ds)
      
      new$yhat=ts(new$yhat,end=c(year(dayend),as.numeric(format(dayend, "%j"))+1), frequency = 365)
      
      autoplot(ts.y) +theme_bw() +autolayer(new$yhat)+
        xlab("Year")+ ylab("Y")+
        ggtitle("Prophet Model")

     
    } else if(input$mod=='Auto Arima'){
      #M3 Auto Arima
      M3=auto.arima(ts.train,seasonal = TRUE, approximation = FALSE)
      forecast=forecast(M3,h=length(ts.test))
      autoplot(ts.y) +theme_bw() +autolayer(forecast$mean)+
        xlab("Year")+ ylab("Y")+
        ggtitle("Auto Arima Model")
      
    }
    
    
  })
  
  output$forecasting <- renderTable({
    data=df()[,c(input$datevar,input$tsvar)]
    names(data)=c("ds","y")
    data$ds=format(as.Date(data$ds))
    day1=as.Date(first(data$ds))
    dayend=as.Date(last(data$ds))
    y=ts(data$y,start = c(year(day1), as.numeric(format(day1, "%j"))), frequency = 365)
    
    if (input$mod == 'Seasonal Naive') {
     forecast=snaive(y,h=input$horizon)

     new=data.frame('Date'=format(seq(dayend+1, by = "day", length.out = input$horizon),"%Y-%m-%d"),
                   'Forecast'=forecast$mean,
                   'Lower'=forecast$lower,
                    'Upper'=forecast$upper)
      
  
    } else if (input$mod=='Smoothing'){
      m_smooth <- ets(data$y,damped = T, lambda = 'auto')
      forecast <- forecast(m_smooth, h=input$horizon)
      new=data.frame('Date'=format(seq(dayend+1, by = "day", length.out = input$horizon),"%Y-%m-%d"),
                   'Forecast'=forecast$mean,
                   'Lower'=forecast$lower,
                    'Upper'=forecast$upper)
      
    } else if (input$mod=='Prophet'){
      
      m_prophet <- prophet(data)
      future <- make_future_dataframe(m_prophet, periods = input$horizon)
      forecast <- predict(m_prophet, future)
      forecast$ds=format(forecast$ds)
      new=tail(forecast[c('ds', 'yhat', 'yhat_lower', 'yhat_upper')],input$horizon)
      names(new)=c('Date','Forecast','Lower','Upper')
      new
      
    } else if (input$mod=='Auto Arima'){
      M3=auto.arima(y,lambda = "auto")
      
      forecast=forecast(M3,h=input$horizon)
      new=data.frame('Date'=format(seq(dayend+1, by = "day", length.out = input$horizon),"%Y-%m-%d"),
                     'Forecast'=forecast$mean,
                     'Lower'=forecast$lower,
                     'Upper'=forecast$upper)
      
    }
    
    
  })
  
  output$dygraph <- renderDygraph({
    data=df()[,c(input$datevar,input$tsvar)]
    names(data)=c("ds","y")
    data$ds=format(as.Date(data$ds))
    day1=as.Date(first(data$ds))
    dayend=as.Date(last(data$ds))
    y=ts(data$y,start = c(year(day1), as.numeric(format(day1, "%j"))), frequency = 365)
    
    if (input$mod == 'Seasonal Naive') {
      forecast=snaive(y,h=input$horizon,level=95)
      
      names(forecast)
      new=data.frame('ds'=seq(dayend, by = "day", length.out = input$horizon),
                     'yhat'=forecast$mean,
                     'yhat_lower'=forecast$lower,
                     'yhat_upper'=forecast$upper)
      
      names(new)=c('ds','yhat','yhat_lower','yhat_upper')
      
      data <- xts(x = new[,-1], order.by = new$ds)
      
      dygraph(data,main='Seasonal Naive Forecasting Plot') %>%
        dySeries(c('yhat_lower','yhat', 'yhat_upper'))
      
      
      
    } else if (input$mod=='Smoothing'){
      m_smooth <- ets(data$y,damped = T, lambda = 'auto')
      forecast <- forecast(m_smooth, h=input$horizon,level=95)
      
      #forecast
      new=data.frame('ds'=seq(dayend, by = "day", length.out = input$horizon),
                     'yhat'=forecast$mean,
                     'yhat_lower'=forecast$lower,
                     'yhat_upper'=forecast$upper)
      
      names(new)=c('ds','yhat','yhat_lower','yhat_upper')
      
      data <- xts(x = new[,-1], order.by = new$ds)
      
      dygraph(data,main='Smoothing Forecasting Plot') %>%
        dySeries(c('yhat_lower','yhat', 'yhat_upper'))
      
    } else if (input$mod=='Prophet'){
      
      m_prophet <- prophet(data)
      future <- make_future_dataframe(m_prophet, periods = input$horizon)
      forecast <- predict(m_prophet, future)
      forecast$ds=format(forecast$ds)
      new=tail(forecast[c('ds', 'yhat', 'yhat_lower', 'yhat_upper')],input$horizon)
      new$ds=as.Date(new$ds)
      data <- xts(x = new[,-1], order.by = new$ds)
      
      dygraph(data,main='Prophet Forecasting Plot') %>%
        dySeries(c('yhat_lower','yhat', 'yhat_upper'))
      
    } else if (input$mod=='Auto Arima'){
      FM3=auto.arima(y,seasonal = TRUE, approximation = FALSE)
      forecast=forecast(FM3,h=input$horizon,level=95)
      #forecast
      new=data.frame('ds'=seq(dayend, by = "day", length.out = input$horizon),
                     'yhat'=forecast$mean,
                     'yhat_lower'=forecast$lower,
                     'yhat_upper'=forecast$upper)
      
      names(new)=c('ds','yhat','yhat_lower','yhat_upper')
      
      data <- xts(x = new[,-1], order.by = new$ds)
      
      dygraph(data,main='Auto Arima Forecasting Plot') %>%
        dySeries(c('yhat_lower','yhat', 'yhat_upper'))
      
    }
  })
  
  
}

# Create Shiny app object
shinyApp(ui = ui, server = server)
