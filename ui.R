#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
shinyUI(
  fluidPage(
  
  # Application title
  titlePanel(h2("How rich would have you become investing in",
                span("just", style = "color:red"),
                span("OneCoin", style = "color:blue"),"?",
                 align ="center" )),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
       selectInput("coin", "Please select a coin from the list:",
                   choices = c("Bitcoin",
                               "Ethereum",
                               "Ripple",
                               "BitcoinCash",
                               "Litecoin"),
                   selected = "Bitcoin"),
       numericInput("amount", "Select the amount of money ($) to invest:",
                     value = 0, min= 0),
       
       dateInput("entry", "Select an entry date for your investment:",
                 value = "2018-01-01"),
       
       dateInput("exit", "Select the end date for your investment:"),
       
       imageOutput("coin_img")
       
    ),
    
    
    # Show a plot of the generated distribution
    mainPanel(
        
        plotOutput("coin_plot",width = "100%", height = "400px"),
       
        h1(textOutput("returnD"), style="color:blue"),
        h1(textOutput("returnP"), style="color:red")
        
        
    )
  ),
  
  
    
    titlePanel(h1("App Documentation", align = "center", style="color:red")),
    
    mainPanel(
      
      h3("Description", style="color:blue"),
      code("This app allow the user to assess the return of an investment, done in the past, in one of the 5 major criptocoins for market capitalization.
         The data are from the Poloniex exchange."),
      h3("How does it works?", style="color:red"),
      h4("The user start choosing the coin from the selecting box:"),
      
        selectInput("pippo", "Please select a coin from the list:",
                    choices = c("Bitcoin")),
      
      h4("it is possible to select among 5 coins:"),
      h5("1. Bitcoin - symbol BTC on poloniex exchange"),
      h5("2. Ethereum - symbol ETH on poloniex exchange"),
      h5("3. Ripple - symbol XRP on poloniex exchange"),
      h5("4. Bitcoin Cash - symbol BCH on poloniex exchange"),
      h5("5. Litecoin - symbol LTC on poloniex exchange"),
      br(),
      h4("the app automatically show the logo for the selected coin!", style="color:red"),
      h4("The next step is to select the amount in $ that you would have liked to invest."),
      numericInput("in", "Select the amount of money ($) to invest:",
                   value = 0, min= 0),
      
      h4("Then you should select the starting and end date for your investment"),
      h4("please note that if the data relative to the selected coin are not available, for the date that you´ve selected, it´s because the coin was not existing yet!", style = "color:red"),
      h4("The starting date is set as default on the 2018-01-01, while the end date is automatically set to the current date."),
      dateInput("ent", "Select an entry date for your investment:",
                value = "2018-01-01"),
      
      dateInput("exi", "Select the end date for your investment:"),
      h4("The app automatically show the trend of the selected coin for the selected time frame and compute the value of your investment at the end date and the percentage return."),
      h4("NOTE: 1 USDT = 1 USD", style="color:red"),
      h2("Enjoy!!!", style="color:blue")
      
  )
    
    
      
    
  )
  
)
