

zincids <- readr::read_csv(
    file = "../../databases/ZINC_instock/all_ligands.csv",
    col_names = "zincid",
    show_col_types = FALSE)



#' Assemble donk scores
#'
#' @param data_path character directory .csv files are located
#' @param output_path character output .parquet path
#'
#' Write output_path .parquet file with columns
#'   <zincid> <energy> binds
assemble_donk_scores <- function(
    data_path,
    output_path) {

    cat(
        "data path: ", data_path, "\n",
        "output path: ", output_path, "\n",
        sep = "")

    file_index <- 1
    scores <- list.files(
        path = data_path,
        full.names = TRUE,
        pattern = "*.csv",
        recursive = TRUE) |>
        purrr::map_dfr(.f = function(path) {
            if (file_index %% 10 == 0) {
                cat("Reading  '", path, "' ", file_index, "\n", sep = "")
            }
            file_index <<- file_index + 1

            readr::read_tsv(
                file = path,
                show_col_types = FALSE) |>
                dplyr::mutate(
                    target_id = basename(path) |>
                        stringr::str_replace(".csv", "")) |>
                dplyr::select(-binds) |>
                dplyr::rename(binds = energy) |>
                tidyr::separate_wider_regex(
                    col = zincid,
                    patterns = c(
                        zincid = "[^ ]+", "[ ]+",
                        energy = "[^ ]+")) |>
                dplyr::mutate(
                    energy = as.numeric(energy)) |>
                dplyr::select(
                    target_id, zincid, energy, binds)                
        })
    scores |> arrow::write_parquet(output_path)
    scores
}

# takes about an hou2 hours  and laregely diskbound on great lakes
# produces a parquet of about ~72 Gb
scores <- assemble_donk_scores(
    data_path = "../pymolalign_designs_andDock/matrix_analysis",
    output_path = "product/donk_v1_scores.parquet")

# or if you want to reload it from disk
# takes about 5 minutes and uses ~90 Gb of memory
# scores <- arrow::read_parquet("product/donk_v1_scores.parquet")


energies_wide <- scores |>
    dplyr::select(zincid, target_id, energy) |>
    tidyr::pivot_wider(
        id_cols = zincid,
        names_from = target_id,
        values_from = energy)

# too much memory :(
#energies_wide <- zincids |>
#    dplyr::left_join(
#        energies_wide,
#        by = "zincid") |>
#    dplyr::mutate_all(~replace(., is.na(.), 10))

energies_wide |>
    arrow::write_parquet(
        "product/donk_v1_energies_wide.parquet")


binds_wide <- scores |>
    dplyr::select(zincid, target_id, binds) |>
    tidyr::pivot_wider(
        id_cols = zincid,
        names_from = target_id,
        values_from = binds)

#binds_wide <- zincids |>
#    dplyr::left_join(
#        binds_wide,
#        by = "zincid") |>
#    dplyr::mutate_all(~replace(., is.na(.), 0))


binds_wide |>
    arrow::write_parquet(
        "product/donk_v1_binds_wide.parquet")
