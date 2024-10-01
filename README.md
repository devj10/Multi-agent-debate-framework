# disc-interact
to install conda on mac
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh
```
https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html

Create a new conda environment
```
conda create -n cs197 python=3.10.9
conda activate cs197
```

Clone the repository and install the requirements
```
git clone https://github.com/kanishkg/disc-interact.git
cd disc-interact
pip install -r requirements.txt
```

then run the test script
```
export CRFM_API_KEY=p4z0j9adj6edJOWBMnEqfPBZxAXlfOGd
python test.py
```
