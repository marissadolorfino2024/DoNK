target_metadata <- data.frame(
    target_id = arrow::open_dataset(
        sources = "product/donk_v1_binds_wide.parquet")$schema$names) |>
    dplyr::filter(target_id != "zincid")


target_metadata <- target_metadata |>
    tidyr::separate_wider_regex(
        cols = target_id,
        patterns = c(
            scaffold_info = ".*",
            "_prepped_formatted_",
            design_info = ".*",
            "_energies_",
            design_radius = "[0-9]+",
            "angdesign"),
        cols_remove = FALSE) |>
    dplyr::mutate(
        design_radius = as.numeric(design_radius))

target_metadata <- target_metadata |>
    dplyr::mutate(
        scaffold_class = dplyr::case_when(
            scaffold_info == "1a28_progest" ~ "NHR",
            scaffold_info == "1a52_estro" ~ "NHR",
            scaffold_info == "2am9_andro" ~ "NHR",
            scaffold_info == "3gws_thyr" ~ "NHR",
            scaffold_info == "3kfc_lxr" ~ "NHR",
            scaffold_info == "5c1m_mu" ~ "GPCR",
            scaffold_info == "5wiu_dopd4" ~ "GPCR",
            scaffold_info == "6kpc_CB2" ~ "GPCR",
            scaffold_info == "6me5_MT1" ~ "GPCR",
            scaffold_info == "7jur_MEK" ~ "Kinase_STE", # MAP3K1
            scaffold_info == "7qpi_VDR" ~ "NHR",
            # Kinase classification based on
            # http://kinase.com/wiki/index.php/Kinase_classification
            scaffold_info |> stringr::str_detect("^AGC") ~ "Kinase_AGC",
            scaffold_info |> stringr::str_detect("^CAMK") ~ "Kinase_CAMK",
            scaffold_info |> stringr::str_detect("^CK1") ~ "Kinase_CK1",
            scaffold_info |> stringr::str_detect("^CMGC") ~ "Kinase_CMGC",
            scaffold_info |> stringr::str_detect("^OTHER") ~ "Kinase_OTHER",
            scaffold_info |> stringr::str_detect("^STE") ~ "Kinase_STE",
            scaffold_info |> stringr::str_detect("^TKL") ~ "Kinase_TKL",
            scaffold_info |> stringr::str_detect("^TYR") ~ "Kinase_TYR"))

target_metadata <- target_metadata |>
    dplyr::mutate(
        scaffold_uniprot_id = dplyr::case_when(
            scaffold_info == "1a28_progest" ~ "PRGR_HUMAN",
            scaffold_info == "1a52_estro" ~ "ESR1_HUMAN",
            scaffold_info == "2am9_andro" ~ "ANDR_HUMAN",
            scaffold_info == "3gws_thyr" ~ "THB_HUMAN",
            scaffold_info == "3kfc_lxr" ~ "NR1H2_HUMAN",
            scaffold_info == "5c1m_mu" ~ "OPRM_MOUSE",
            scaffold_info == "5wiu_dopd4" ~ "DRD4_HUMAN",
            scaffold_info == "6kpc_CB2" ~ "CNR2_HUMAN",
            scaffold_info == "6me5_MT1" ~ "MTR1A_HUMAN",
            scaffold_info == "7jur_MEK" ~ "MP2K1_RABIT", # MAP3K1
            scaffold_info == "7qpi_VDR" ~ "S4R4S2_PETMA",
            # Kinase classification based on
            # http://kinase.com/wiki/index.php/Kinase_classification
            TRUE ~ scaffold_info |>
                stringr::str_extract("[^_]+_(.*_HUMAN)", group = 1)))

target_metadata <- target_metadata |>
    tidyr::separate_wider_regex(
        cols = design_info,
        patterns = c(
            design_backbone_index = "[0-9]+",
            "_[0-9]+_",
            design_sequence_bias = "[a-z]+",
            "_",
            design_sequence_index = "[0-9]+")) |>
    dplyr::mutate(
        design_backbone_index = as.integer(design_backbone_index),
        design_sequence_index = as.integer(design_sequence_index))
        
target_metadata <- target_metadata |>
    dplyr::select(
        target_id,
        scaffold_class,
        scaffold_uniprot_id,
        design_radius,        
        design_backbone_index,
        design_sequence_bias,
        design_sequence_index)

target_metadata |>
    readr::write_tsv("product/target_metadata.tsv")
