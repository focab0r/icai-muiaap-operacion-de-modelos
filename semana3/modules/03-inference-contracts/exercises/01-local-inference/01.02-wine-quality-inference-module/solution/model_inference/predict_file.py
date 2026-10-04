"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""

# Implementa el comando:
# python -m model_inference.predict_file --input <csv> --output <csv>
# No dejes un archivo de salida parcial si alguna fila es inválida.


import argparse
import os
import pandas as pd

from model_inference.contracts import WineQualityRequest
from model_inference.preprocess import preprocess_wine_request, PREPROCESSING_VERSION
from model_inference.inference import load_wine_quality_model, infer_wine_quality


def read_csv(path):
	
	if not os.path.exists(path):
		raise Exception("[X] ERROR: Invalid path")
	df = pd.read_csv(path)
	d = df.to_dict(orient="Index")
	l = []
	for id_row, values in d.items():
		try:
			l.append(WineQualityRequest(**values))
		except:
			raise Exception(f'[X] ERROR: Invalid value detected at line {id_row}')

	return l




if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Prediction of wines')
	parser.add_argument('--input', help='Input file', required=True)
	parser.add_argument('--output', help='Output file', required=True)
	args = parser.parse_args()
	
	print(f'[*] Input file: {args.input}')
	print(f'[*] Output file: {args.output}')

	# Read input csv
	l = read_csv(args.input)
	print("[+] CSV readed")
	
	# Parse input
	pre_l = []
	for elem in l:
		new_elem = preprocess_wine_request(elem)
		pre_l.append(new_elem)

	# Execute model
	model = load_wine_quality_model()
	result_list = []
	num_elem = 0
	for elem in pre_l:
		result, confidence = infer_wine_quality(elem, model)
		result_list.append((result, confidence))
		print(f'[+] Result: {result}, conf: {confidence}')


	# Save results
	print("[*] Saving results...")
	counter = 0
	with open(args.output, "w") as f:
		f.write("sample_id,quality_band,confidence,model_version,preprocessing_version\n")
		for r, c in result_list:
			f.write(l[counter].sample_id+","+str(r)+","+str(c)+","+model["model_version"]+","+str(PREPROCESSING_VERSION)+"\n")
			counter+=1
	print("[+] Results saved")
	print("[+++] Finished")

