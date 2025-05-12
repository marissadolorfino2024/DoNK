#!/bin/bash

## this is an example script for running DiffDock with all 8 chemical probes against a set of proteins
## paths will need to modified  

for i in $(seq 1 200) ## this will also need to be modified depending on the number of proteins, job limits, etc. 
do
        
        beg=$((100 * (i - 1) + 1))
        cap=$(expr $beg + 99)
	
	cat <<EOF  > batch_diffdock.sh
#!/bin/sh
#SBATCH --job-name=diffdock_batch${i}
#SBATCH --account=
#SBATCH --partition=spgpu,gpu
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=20GB
#SBATCH --time=120:00:00
#SBATCH --output=diffdock_batch${i}.out
#SBATCH --error=diffdock_batch${i}.err

time {
sed -n '${beg},${cap}p' 10ang_tasks.txt | while read -r line
do
	      protein="/nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/AF_fold_designs/10angstrom_0.3temp_AF_rank1_files/\${line}"
	
	      smiles="C1=CC=C(C=C1)O" # phenol

	      time python -m inference --config default_inference_args.yaml --protein_path \$protein --ligand \$smiles --out_dir /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/diffdockalign_designs_andDock/10ang-design_diffdock_results/\${line::-4}_phenol_preds --samples_per_complex 100


        smiles="C1=CC=CC=C1" # benzene

        time python -m inference --config default_inference_args.yaml --protein_path \$protein --ligand \$smiles --out_dir /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/diffdockalign_designs_andDock/10ang-design_diffdock_results/\${line::-4}_benzene_preds --samples_per_complex 100


        smiles="C1CCCCC1" # cyclohexane

        time python -m inference --config default_inference_args.yaml --protein_path \$protein --ligand \$smiles --out_dir /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/diffdockalign_designs_andDock/10ang-design_diffdock_results/\${line::-4}_cyclohexane_preds --samples_per_complex 100


        smiles="[2H]C([2H])([2H])C(C([2H])([2H])[2H])O" # 2-propanol

        time python -m inference --config default_inference_args.yaml --protein_path \$protein --ligand \$smiles --out_dir /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/diffdockalign_designs_andDock/10ang-design_diffdock_results/\${line::-4}_2propanol_preds --samples_per_complex 100


        smiles="CC(=O)NC" # N-methylacetamide

        time python -m inference --config default_inference_args.yaml --protein_path \$protein --ligand \$smiles --out_dir /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/diffdockalign_designs_andDock/10ang-design_diffdock_results/\${line::-4}_N-methylacetamide_preds --samples_per_complex 100


        smiles="C1=CN=CN=C1" # pyrimidine

        time python -m inference --config default_inference_args.yaml --protein_path \$protein --ligand \$smiles --out_dir /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/diffdockalign_designs_andDock/10ang-design_diffdock_results/\${line::-4}_pyrimidine_preds --samples_per_complex 100


        smiles="C1=CN=CN1" # 1H-imidazole

        time python -m inference --config default_inference_args.yaml --protein_path \$protein --ligand \$smiles --out_dir /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/diffdockalign_designs_andDock/10ang-design_diffdock_results/\${line::-4}_1H-imidazole_preds --samples_per_complex 100


        smiles="CC(=O)O" # acetic acid

        time python -m inference --config default_inference_args.yaml --protein_path \$protein --ligand \$smiles --out_dir /nfs/turbo/umms-maom/MPProjects/chemical_space/dock_dev/donk_v1/diffdockalign_designs_andDock/10ang-design_diffdock_results/\${line::-4}_aceticacid_preds --samples_per_complex 100

done

}
EOF
        sbatch batch_diffdock.sh

	rm batch_diffdock.sh

done
