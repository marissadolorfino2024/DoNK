

zincids <- readr::read_csv(
    file = "../../databases/ZINC_instock/all_ligands.csv",
    col_names = "zincid",
    show_col_types = FALSE)

receptor_metadata <- readr::read_tsv(
    "product/target_metadata_20240924.tsv",
    show_col_types = FALSE)


scores <- arrow::read_parquet("product/donk_v1_scores.parquet")


statistics <- list(
    ligand = list(),
    target = list(),
    interaction = list())


################
# Ligand stats #
################

statistics$ligand$n_total <- nrow(zincids)
statistics$ligand$n_distinct <- zincids |>
    dplyr::distinct(zincid) |>
    nrow()

statistics$ligand$n_energy <- scores |>
    dplyr::distinct(zincid) |>
    nrow()

scores |>
    dplyr::group_by(zincid) |>
    dplyr::summarize(
        mean_ligand_energy = mean(energy

statistics$ligand$mean_energy <- 
    
    mean(scores$energy)       

statistics$ligand$median_energy <-
    median(scores$energy)

ligand_bind_counts <- scores |>
    dplyr::filter(binds == 1) |>
    dplyr::count(zincid)

statistics$ligand$n_bind <- ligand_bind_counts |>
    nrow()

statistics$ligand$n_bind_unique <- ligand_bind_counts |>
    dplyr::filter(n == 1) |>
    nrow()

statistics$ligand$mean_bind <- ligand_bind_counts |>
    dplyr::summarize(
        mean_bind = mean(n)) |>
    dplyr::pull(mean_bind)

statistics$ligand$median_bind <- ligand_bind_counts |>
    dplyr::summarize(
        median_bind = median(n)) |>
    dplyr::pull(median_bind)



################
# Target stats #
################

statistics$target$n_total <- nrow(target_metadata)
statistics$target$n_distinct <- target_metadata |>
    dplyr::distinct(target_id) |>
    nrow()

statistics$target$n_energy <- scores |>
    dplyr::distinct(target_id) |>
    nrow()

statistics$target$mean_energy <-
    mean(scores$energy)       

statistics$target$median_energy <-
    median(scores$energy)

target_bind_counts <- scores |>
    dplyr::filter(binds == 1) |>
    dplyr::count(target_id)

statistics$target$n_bind <- target_bind_counts |>
    nrow()

statistics$target$n_bind_unique <- target_bind_counts |>
    dplyr::filter(n == 1) |>
    nrow()

statistics$target$mean_bind <- target_bind_counts |>
    dplyr::summarize(
        mean_bind = mean(n)) |>
    dplyr::pull(mean_bind)

statistics$target$median_bind <- target_bind_counts |>
    dplyr::summarize(
        median_bind = median(n)) |>
    dplyr::pull(median_bind)

statistics |>
    jsonlite::toJSON() |>
    cat(file = "product/statistics.json")
