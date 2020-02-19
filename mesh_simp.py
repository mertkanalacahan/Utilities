import sys
import os
import subprocess
import glob

# This script takes all obj files in a folder and simplifies them
# according to settings given in filter script below. Just put this
# script under your MeshLab directory which also includes meshlabserver.exe
# Tested with MeshLab 2016.2

filter_script_mlx = """<!DOCTYPE FilterScript>
<FilterScript>
 <filter name="Simplification: Quadric Edge Collapse Decimation">
  <Param type="RichInt" value="50625" name="TargetFaceNum" />
  <Param type="RichFloat" value="0" name="TargetPerc" />
  <Param type="RichFloat" value="0.3" name="QualityThr" />
  <Param type="RichBool" value="false" name="PreserveBoundary" />
  <Param type="RichFloat" value="40" name="BoundaryWeight" />
  <Param type="RichBool" value="true" name="PreserveNormal" />
  <Param type="RichBool" value="true" name="PreserveTopology" />
  <Param type="RichBool" value="true" name="OptimalPlacement" />
  <Param type="RichBool" value="true" name="PlanarQuadric" />
  <Param type="RichBool" value="false" name="QualityWeight" />
  <Param type="RichBool" value="true" name="AutoClean" />
  <Param type="RichBool" value="false" name="Selected" />
  </filter>
</FilterScript>"""

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def create_tmp_filter_file(filename='filter_file_tmp.mlx'):
    with open(os.path.join(get_script_path(), filename), 'w') as f:
        f.write(filter_script_mlx)
    return os.path.join(get_script_path(), filename)

def reduce_faces(in_file, out_file, filter_script_path):
    command = "meshlabserver -i " + in_file + " -s " + filter_script_path + " -o " + out_file
    output = subprocess.call(command, shell=True)
    print()
    print("Done:")
    print(in_file + " > " + out_file + ": " + str(output))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print(sys.argv[0] + " path_to_folder_including_input_meshes")
        exit(0)

    in_mesh_folder = sys.argv[1]
    folder_name = "SimplifiedMeshes"

    all_files = glob.glob(os.path.join(in_mesh_folder, "*.obj"))

    try:
        os.mkdir(os.path.join(get_script_path(), folder_name))
    except OSError as e:
        print(sys.stderr, "Exception creating folder for meshes: " + str(e))
        exit(0)

    filter_path = create_tmp_filter_file()

    for f in all_files:
        filename = f.split('\\')[-1]
        out_mesh = os.path.join(get_script_path(), folder_name, filename)
        reduce_faces(f, out_mesh, filter_path)

    print()
    print("Done simplifying, find files at: " + os.path.join(get_script_path(), folder_name))
    if os.path.exists(filter_path):
        os.remove(filter_path)