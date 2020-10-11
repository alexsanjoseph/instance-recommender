# instance-recommender

### Getting started
* Clone the repository
```
git clone https://github.com/alexsanjoseph/instance-recommender
```
* Optionally create a new virtualenv
```
python3 -m virtualenv .env
source .env/bin/activate 
```
* Install dependencies
```
pip install -r requirements.txt
```
* Get recommendations
```
 ./recommender --vcpus 8 --memory 16 --max-vcpus 3 --max-memory 8
```

### Refresh instance list
```
python utils/refresh_instance_list.py
```