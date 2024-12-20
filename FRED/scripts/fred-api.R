
# install and load necessary packages/libraries

packages <- c("httr2", "jsonlite", "tidyverse", "glue")

# Loop through each package
for (pkg in packages) {
  # Check if the package is already installed
  if (!require(pkg, character.only = TRUE)) {
    # Install the package using renv::install if not already installed
    renv::install(pkg)
    # Load the package after installation
    library(pkg, character.only = TRUE)
  }
}


library(httr2)
library(jsonlite)
library(glue)
library(tidyverse)
library(purrr)  # For `pluck`
library(dplyr)  # For `glimpse`



# write a function that will use httr2 package


get_fred_series <- function(seriesID, start, end, units, api_key) {
  
  base_url <- "https://api.stlouisfed.org/fred/series/observations"
  
  
  # Construct the request
  response <- httr2::request(base_url) |>
    httr2::req_url_query(
      series_id = seriesID,
      api_key = api_key,
      file_type = "json",
      observation_start = start,
      observation_end = end,
      units = units
    ) |>
    httr2::req_perform()
  
  # Check if request was successful
  if (httr2::resp_status(response) == 200) {
    
    response_json <- 
      response |>
      httr2::resp_body_json() |>
      pluck('observations') |> 
      map_dfr(
        \(x) {
          tibble(
            date = x |> pluck('date'),
            value = x |> pluck('value')
          )
        }
      ) |> 
      setNames(c("date", seriesID))
    
    return(response_json)
    
  } else {
    
    # Message if API call is unsuccessful
    message("Request failed with status: ", httr2::resp_status(response))
    return(NULL)
  }
}



get_more_series <- 
  function(seriesIDs, start, end, units, api_key) {
    
    
    # initialise an empty list that will store the series 
    
    series_list <- lapply(seriesIDs, function(seriesID) {
      
      # get series data 
      
      series_data <- get_fred_series(seriesID, start, end, units, api_key)
      
      # now let us rename our columns accordingly; to match seriesID for ease of interpretation
      
      names(series_data)[2] <- seriesID
      return(series_data)
    })
    
    
    # join these datasets into one data frame
    
    
    combined_data <- purrr::reduce(
      series_list,
      dplyr::full_join, by = 'date')
    
    combined_data <- 
      combined_data |> 
      dplyr::mutate(date = lubridate::as_date(date))
    
    combined_data[-1] <- lapply(combined_data[-1], as.numeric)
    
    return(combined_data)
  }

