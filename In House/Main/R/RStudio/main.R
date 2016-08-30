library(pacman)

pkg_vector <- c('dplyr', 'Matrix', 'caret', 'randomForest', 'xgboost')
p_load(char=pkg_vector)


splits <- function(df, metric) {
  splitIdx <- createDataPartition(df[, metric], p=.67, list = FALSE)
  traindf <- df[splitIdx[, 1], ]
  testdf <- df[-splitIdx[, 1], ]
  return(list(train=data.frame(traindf), test=data.frame(testdf)))
}

clean <- function(df, metric, lt, ut) {
  newdf <- df %>%
    filter(df[metric] >= lt, df[metric] <= ut)
  return(newdf)
}


wrt <-
  read.csv('/Users/Dino/Dropbox/Work/Projects/MISC/R/RStudio/profitability-cogs-csv-files/wrtTrain.csv') %>%
  as.data.frame() %>%
  mutate(X=NULL)

wrt.df <-
  wrt %>%
    mutate(
      isAuto = factor(isAuto),
      inksPerPc = totInks/qty,
      impsPerPc = totImps/qty,
      totEstImps = qty*totInks,
      # estError = (totImps-totEstImps)/(totImps),
      timePerEstImp = runtime/totEstImps,
      timePerRecImp = runtime/totImps,
      estImpsPerTime = totEstImps/runtime,
      recImpsPerTime = totImps/runtime
    )

amc.df <-
  wrt.df %>%
    mutate(timePerEstImp = NULL,
           timePerRecImp = NULL,
           estImpsPerTime = NULL,
           recImpsPerTime = NULL)

ac <-
  amc.df %>%
    splits('isAuto')

ac.trainY <- ac$train$isAuto[]
ac.trainX <-
  ac$train %>%
    mutate(runtime=NULL, isAuto=NULL, totImps=NULL, estImpsPerPc=(totEstImps/qty), impsPerPc=NULL)

ac.testY <- ac$test$isAuto[]
ac.testX <-
  ac$test %>%
  mutate(runtime=NULL, isAuto=NULL, totImps=NULL, estImpsPerPc=(totEstImps/qty), impsPerPc=NULL)


# wrt.filt <- wrt.df %>% filter(timePerEstImp >= 4, timePerEstImp <= 1000)

wrt.250filt <- clean(wrt.df, 'timePerEstImp', 4, 250)
wrt250.split <- splits(wrt.df, 'timePerEstImp')

# inTrainWRT <- createDataPartition(wrt.df$runtime, p=.67, list = FALSE)

# wrt.train.df <- wrt.df[inTrainWRT[, 1], ]
# wrt.test.df <- wrt.df[-inTrainWRT[, 1], ]
