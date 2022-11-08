import numpy as np

def data_loader(filepath):
    """Чтение ваттметрограмм из файла"""
    file_handler = open(filepath, 'r')

    mpcs = list()
    labels = list()
    
    for data_str in file_handler:
        (label, mpc_str) = data_str.split('lb')
        (samples_count_str, mpc_str) = mpc_str.split('cnt')
        labels.append(int(label))
        samples_count = int(samples_count_str)

        mpc_str = mpc_str.strip('[]')

        mpc = np.fromstring(mpc_str, dtype=float, sep=',', count=samples_count)
        mpcs.append(mpc)
        #print(label)

    file_handler.close()

    mpcs = np.array(mpcs)
    labels = np.array(labels)
    return (labels, mpcs)




