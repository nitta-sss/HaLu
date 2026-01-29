from Audio.Voice_Read import get_result_Hz

def reload_Hz(y):
    Hz = get_result_Hz_only()
    get_mean_f0(y, sr=16000)
    