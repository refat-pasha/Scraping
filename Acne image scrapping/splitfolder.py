import splitfolders

# Replace 'input_folder' with the path to your 9 folders
# Replace 'output_folder' with the desired output directory
splitfolders.ratio(input='acne', output="data of acne_img", seed=42, ratio=(.7, .15, .15))
