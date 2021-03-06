---
title       : Cryptocoin Investment
subtitle    : How rich could have you been ...?
author      : Antonello Finucci
job         : 
framework   : io2012        # {io2012, html5slides, shower, dzslides, ...}
highlighter : highlight.js  # {highlight.js, prettify, highlight}
hitheme     : tomorrow      # 
widgets     : [mathjax]            # {mathjax, quiz, bootstrap}
mode        : selfcontained # {standalone, draft}
knit        : slidify::knit2slides
---

## Investment in Cryptocoins....

- Nowdays there are a lot of people talking about cryptocoins and how risky or
rewarding they have been in the past.
- The app gives an overview about how good or bad an investment in one of the today 5 major cryptocoins would have been.
- The cryptocoin data are taken from the exchange plattform Poloniex using the


```r
        suppressPackageStartupMessages(library(PoloniexR))
```

- In the following slides an investment example, using Ethereum, that you could repeat using the app is shown

--- .class #id 

## The incredible growth of Crypto Coins

The development of the Ethereum price in $ from 2016-01-01 until the 2017-12-31.








```r
          ggplot(chart.df, aes(x= chart.df$Date, y= chart.df$close))+
            geom_line()+ labs(title = "Trend for the selected Cryptocoin",
                              x = "Investment period",y="ETH-USDT")
```

<img src="figure/unnamed-chunk-5-1.png" title="plot of chunk unnamed-chunk-5" alt="plot of chunk unnamed-chunk-5" style="display: block; margin: auto;" />


--- .class

## Investment example

If you would have invested 100$ in Ethereum on the 2016-01-01 at the end of last year you would have got....


```r
    amount_invested <- 100
    return_Dollar <- round((chart.df[chart.df$Date=="2017-12-31",5]/
                  chart.df[chart.df$Date=="2016-01-01",5]) *amount_invested, 2)
```

$Value = \frac{ETH_{value(2017-12-31)}}{ETH_{value(2016-01-01)}} * amount invested=$ 76758.74$


```r
# Percetage return
        
        Perc_ret <- round((return_Dollar- amount_invested)/amount_invested *100,2)
```

$Percetage Return = \frac{Value - amount invested}{amount invested}*100=$76658.74%

--- .class

## Conclusions

- Investment in the 5 cryptocoins contained in the app have been all very profitable
- In the investement example given for ETH you would have increased of 766.58 times your initial investment
- Remember that investing in Cryptocoins is very dangereous because of the high volatility
- Nobody knows if in the future they will keep developing like they have done in the past.
- For the moment enjoy my app and NO REGRETS...




