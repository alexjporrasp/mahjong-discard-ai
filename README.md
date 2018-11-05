Before installing tensorflow we must make sure we have Python 3.6.x installed, a newer version like the 3.7.0 will not work. Once we have Python installed and we add its route to the PATH we can check the version by executing the following command.

```python -V```

If everything is okay we may proceed to CUDA installation. But prior to that we need to make sure out GPU is CUDA compatible. We need CUDA Toolkit 9.0 and the associated drivers. For that we go to https://developer.nvidia.com/cuda-90-download-archive and select
the operating system. We also need to install CuDNN v7.0 since it is apart from CUDA. Make sure that you add the directory where you installed the cuDNN DLL to your PATH. To download the library you must create and validate an NVIDIA account beforehand.

Now we can install tensorflow and the rest of needed packages (i.e. numpy and pandas). We are doing this with 'pip'. To check your pip version open a console a type the following.
```pip -V```
If it is lower than 10 you may need to upgrade. After that we install the packages by typing:
```pip install tensorflow-gpu
pip install numpy
pip install pandas
```

Upon successful we may now execute Python scripts that use tensorow technology.

# Instructions

To use the client you need to pass a dictionary containing the current state of the game. For example:

```state_sample = {'Riichi': [],
                  'Discards_0': [101, 89],
                  'Melds_0': [],
                  'Discards_1': [14, 4],
                  'Melds_1': [],
                  'Discards_2': [37, 65],
                  'Melds_2': [],
                  'Discards_3': [76],
                  'Melds_3': [[56, 62, -65, 2]],
                  'Hand': [22, 23, 45, 47, 53, 58, 61, 68, 87, 103, 111, 118, 133],
                  'Remaining': 76,
                  'Dora': [104],
                  'Seat': 0}
```
