
# necessary package
  
  
library(httr2)
library(jsonlite)
library(glue)
library(tidyverse)


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

# write a functions that will use httr2 package


# import api_key

# json_file <- jsonlite::fromJSON("FRED/secrets.json")
# 
# fred_api <- json_file$api_key




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
      ) 
    
    return(response_json)
    
  } else {
    
    # Message if API call is unsuccessful
    message("Request failed with status: ", httr2::resp_status(response))
    return(NULL)
  }
}



# dff_data <- get_fred_series(
#   "DFF",
#   "2020-01-01",
#   "2023-01-01",
#   "lin",
#   fred_api)

