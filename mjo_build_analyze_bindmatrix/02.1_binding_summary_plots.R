zincids <- readr::read_csv(
    file = "../../databases/ZINC_instock/all_ligands.csv",
    col_names = "zincid",
    show_col_types = FALSE)

target_metadata <- readr::read_tsv(
    "product/target_metadata_20240924.tsv",
    show_col_types = FALSE)

scores <- arrow::read_parquet("product/donk_v1_scores.parquet")

scores <- scores |>
    dplyr::left_join(
        receptor_metadata |>
        dplyr::transmute(
            target_id,
            scaffold_class = scaffold_class |> as.factor()),
        by = "target_id")

scores |>
    dplyr::group_by(receptor


#################################
# N active vs Number of Ligands #
#################################

ligand_bind_counts_counts <- ligand_bind_counts |>
    dplyr::rename(n_active = n) |>
    dplyr::count(n_active)

plot <- ggplot2::ggplot(
  data = ligand_bind_counts_counts) +
  ggplot2::theme_bw() +
  ggplot2::geom_jitter(
    mapping = ggplot2::aes(
      x = n_active,
      y = n),
    alpha = 0.4,
    size = 0.8,
    shape = 16,
    width = 0.05,
    height = 0.05) +
  ggplot2::scale_x_log10(
    "Active at N Targets",
    breaks = c(1, 3, 10, 30, 100, 300, 1000, 3000)) +
  ggplot2::scale_y_log10(
    "Number of Ligands",
    breaks = c(1, 3, 10, 30, 100, 300, 1000, 3000, 10000))

ggplot2::ggsave(
    filename = "product/n_active_vs_size_20240924.pdf",
    plot = plot,
    width = 5,
    height = 4,
    useDingbats = FALSE)
