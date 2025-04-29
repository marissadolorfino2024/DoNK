#!/bin/bash

for i in $(seq 5000 8676)
do
	dir=$(cat tasks.txt | sed -n "$i p")
	script="prep_struct_${i}.sh"

	cat <<EOF  > $script
#!/bin/bash
#SBATCH --job-name=dock_prep10_${i}
#SBATCH --account=maom0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=5GB
#SBATCH --time=2:00:00
#SBATCH --error=prepare10_${i}.err
#SBATCH --output=prepare10_${i}.out

# usage: run blastermaster to prepare the grids and INDOCK file for receptors and ligands (prep for docking). blastermaster will run for each receptor directory specified in input file (tasks.txt)

# cd into directory in docking directory corresponding to each receptor to be docked to

cd $dir
	
prepare_dir=${dir}_prepared_struct

mkdir \$prepare_dir

cd \$prepare_dir

cp ../rec.pdb .
cp ../xtal-lig.pdb .

source ${DOCK_TEMPLATE}/scripts/dock_blastermaster_standard.sh

pushd custom
cp ../working/rec.ms .
$DOCKBASE/proteins/sphgen/bin/sphgen -i INSPH -o OUTSPH
# edit custom/all_spheres.sph.pdb --> custom/binding_site.sph.pdb
$DOCKBASE/proteins/showsphere/doshowsph.csh all_spheres.sph 0 all_spheres.sph.pdb
# look up original spheres in all_spheres.sph to get radii correct
$DOCKBASE/proteins/pdbtosph/bin/pdbtosph binding_site.sph.pdb binding_site.sph
python ${DOCK_TEMPLATE}/scripts/sph_to_pdb.py \
      	--input binding_site2.sph \
       	--output binding_site2.sph.pdb
python ${DOCK_TEMPLATE}/scripts/copy_sphere_radii.py \
      	--input binding_site.sph \
      	--lookup all_spheres.sph \
      	--output binding_site2.sph
popd


cp custom/binding_site2.sph working/matching_spheres.sph
cp custom/binding_site2.sph working/all_spheres.sph
cp custom/binding_site2.sph working/lowdielectric.sph
cp custom/binding_site.sph.pdb xtal-lig.pdb
cp custom/binding_site2.sph working/xtal-lig.match.sph



source ${DOCK_TEMPLATE}/scripts/dock_visualize_setup.sh
EOF

	sbatch $script
	#rm $script
done


