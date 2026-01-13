import os, argparse
import torch
import numpy as np
from makani.makani.models.model_package import LocalPackage, load_model_package
from datetime import datetime, timedelta, timezone
from FCNV3_ens_perturbation_tool import SphericalGaussian

def main(IC_data_path, IC_time_str, ens_mem, save_path, FCNV3_weight='FCNV3_weight', fore_hr=60, device="cuda:0"):
  # device that we want to use
  device = torch.device(device)
  
  # directory where the model package resides
  model_package_dir = FCNV3_weight
  model = load_model_package(LocalPackage(model_package_dir)).to(device)
  
  
  # input setting
  IC_data =np.load(IC_data_path)
  IC_time = datetime.strptime(str(IC_time_str), "%Y%m%d%H").replace(tzinfo=timezone.utc) 
  
  # save setting
  os.makedirs(save_path, exist_ok=True)
  ens_mem = np.int_(ens_mem)
  for ens_i in range(ens_mem):
    save_ens_path = os.path.join(save_path,f'ens{ens_i:0>2}')
    os.makedirs(save_ens_path, exist_ok=True)
    input_data = torch.tensor(IC_data[None,...]).to(device)
    # normalize the input now to avoid jumping back and forthabs
    input_data = (input_data - model.in_bias)/model.in_scale
    perturbation = SphericalGaussian(noise_amplitude=0.15)
    input_data = perturbation(input_data)
    total_step = np.int_(np.int_(fore_hr)/6) 
    
    # Get the noise state for the batch index
    noise_state = model.model.preprocessor.get_internal_state(tensor=True)
    print('-----------------------')
    print(f'Looping ensemble member:{ens_i}...')
    print(datetime.now())
    with torch.no_grad():
        with torch.inference_mode():
            with torch.autocast(device_type="cuda", dtype=torch.float32): 
                print('start predicting')
                # total_output_data = input.cpu().numpy()
                np.save(os.path.join(save_ens_path,f'output_weather_000h.npy'),\
                        (input_data*model.out_scale+model.out_bias).cpu().numpy())
                for time_i in range(total_step):
                    front_step_fore_time  = IC_time + timedelta(hours=time_i * 6)
                    model.model.preprocessor.set_internal_state(noise_state)
                    # test_data = model(input, ic_time, normalized_data=False, replace_state=False)
                    pred_data = model(input_data, front_step_fore_time, normalized_data=True, replace_state=False)
                    input_data = pred_data
                    np.save(os.path.join(save_ens_path,f'output_weather_{(time_i+1)*6:0>3}h.npy'),\
                            (pred_data*model.out_scale+model.out_bias).cpu().numpy())
                    print(f'finishing output_weather_{(time_i+1)*6:0>3}h.npy')
                    print(datetime.now())
  
                  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Define arguments to get YAML config file.
    parser.add_argument('--input_data',  required=True, help='input_data/ncep_initial_condition.npy')
    parser.add_argument('--input_time',  required=True, help='format: 2025091800')
    parser.add_argument('--ens_mem',  required=True, help='how many ensemble members')
    parser.add_argument('--output_folder',  required=True, help='output_data_2025091800')
    parser.add_argument('--weight',  help='FCNV2 weight', default='FCNV3_weight')
    parser.add_argument('--fore_hr',  help='forecast hour', default=72)
    parser.add_argument('--device',  help='cpu or cuda', default='cuda:0')
    args = parser.parse_args()  
    
    main(args.input_data, args.input_time, args.ens_mem, args.output_folder, FCNV3_weight=args.weight, fore_hr=args.fore_hr, device=args.device)  

