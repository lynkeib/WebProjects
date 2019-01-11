library(dplyr)
library(lubridate)
library(stringr)
library(ggplot2)
data <- read.csv('/Users/chengyinliu/D/2018_Fall/Pet_Project/Bike/los-angeles-metro-bike-share-trip-data/metro-bike-share-trip-data.csv')

data$Start.Time.Sub <- data$Start.Time %>%
  substr(start = 1,
         stop = 10)
data$Start.Time.Sub <- data$Start.Time %>%
  substr(start = 1,
         stop = 10)
data$Start.Time.Sub <- ymd(data$Start.Time.Sub)

data_try <- data %>%
  filter(Bike.ID == 6728) %>%
  arrange(Start.Time.Sub)

data_try_2 <- data %>%
  mutate(Start.Time.ymd = strsplit(data$Start.Time, 'T'))

data$Start.Time.NEW <- str_replace(data$Start.Time, 'T', ' ')
data$Start.Time.NEW <- ymd_hms(data$Start.Time.NEW)
data_try <- data %>%
  filter(Bike.ID == 6728) %>%
  arrange(Start.Time.NEW)

data_try$order <- c(1:220)

write.csv(data_try, '/Users/chengyinliu/data_try.csv')

data <- read.csv('/Users/chengyinliu/D/2018_Fall/Pet_Project/Bike/los-angeles-metro-bike-share-trip-data/metro-bike-share-trip-data.csv')
data$Start.time <- mdy_hms(data$Start.time)
summary(data)

data %>%
  ggplot(aes(x = Duration)) +
  geom_histogram() +
  labs(x = 'Duration',
       y = 'Count',
       title = 'Histogram of Duration')

