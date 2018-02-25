#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)

library(dplyr)
library(ggplot2)

coin_chart <- function(coin_type, amount, start_date, end_date, selector){
# IMPORTING THE DATA
# the data are imported directly from Poloniex
library(PoloniexR)

Sys.setenv(tz = "UTC")
poloniex.public <- PoloniexPublicAPI()

# SELECTING THE PAIR
  coin_code <- as.character()
  
  if (coin_type == "Bitcoin"){coin_code <- "BTC"}
  if (coin_type == "Ethereum"){coin_code <- "ETH"}
  if (coin_type == "Ripple"){coin_code <- "XRP"}
  if (coin_type == "BitcoinCash"){coin_code <- "BCH"}
  if (coin_type == "Litecoin"){coin_code <- "LTC"}

pair    <- paste0("USDT_",coin_code)

#SELECTING THE TIME FRAME
from    <- as.POSIXct(start_date," 00:00:00 UTC")
to      <- as.POSIXct(end_date," 00:00:00 UTC")
period  <- "D"

chart.data <- ReturnChartData(theObject = poloniex.public,
                              pair      = pair,
                              from      = from,
                              to        = to,
                              period    = period)

# Transforming the time serie into a data frame

chart.df <- data.frame(as.data.frame(chart.data))
# including the date column of the xts object

chart.df <- mutate(chart.df, Date = row.names(chart.df))

# bringing the column "Date" at the first position in the df

chart.df <- chart.df[ , c("Date", "high", "low", "open", "close", "volume", "quotevolume",
                          "weightedaverage")]
# Transforming the "Date" column into date format

chart.df$Date <- as.Date(chart.df$Date, "%Y-%m-%d")

if (selector == 1){
pair <- paste0(coin_code,"/USDT")

g <- ggplot(chart.df, aes(x= chart.df$Date, y= chart.df$close))+
        geom_line(colour = "blue")+ labs(title = "Plot of the selected Cryptocoin",
                    x = "Investment Time Frame",y=pair)+
        theme_bw()
return(g)
}

return_Dollar <- round((chart.df[chart.df$Date==end_date,5]/
                          chart.df[chart.df$Date==start_date,5]) * amount, 2)

}


# Define server logic required to draw a histogram
server <- function(input, output) {
   
  output$coin_img <- renderImage({
       list(src = paste0("www/",input$coin,".png"),
         contentType = 'image/png',
         width = 250,
         height = 250,
         align = "center"
         
         )
  }, deleteFile = FALSE)
  

  output$coin_plot <- renderPlot({
        
      coin_chart(input$coin, 0, input$entry, input$exit, 1)
  
  })
  
  
  
  output$returnD <- renderText({
    dollar <- coin_chart(input$coin, input$amount,
                         input$entry, input$exit, 0)
    
    paste("You would get: ", dollar, "$")
    
  })
  
  output$returnP <- renderText({
    dollar <- coin_chart(input$coin, input$amount,
                 input$entry, input$exit, 0)
    
    paste("The percentage change is: ", round((dollar- input$amount)/input$amount *100,2), "%" )
    
  })
  
}
         
   



