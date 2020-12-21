# instance-recommender
## Motivation
Most cloud cost calculators online only calculate prices of Virtual Machines provided by the cloud provider. 

When microservices are involved, one might need a more granular distribution of resources. 

Once a calculation of total resources needed to run a microservices infrastructure is measured, this tool will can be used to calculate an price optimal distribution of EC2 instances needed to run all workloads.

## Getting started
* Clone the repository
```
git clone https://github.com/alexsanjoseph/instance-recommender
```
### With docker
* Build the image
```
$ docker build -t instance-recommender .
```
* Run the image
```
$ docker run -p 8501:8501 instance-recommender
```
### Without Docker
* Optionally create a new virtualenv
```
python3 -m virtualenv .env
source .env/bin/activate 
```
* Install dependencies
```
pip install -r requirements.txt
```
* Run streamlit UI using
```
 streamlit run streamlit.py
```

![Example UI](example_ui.png)


### Utils
#### Refresh inventory
The following script will update the pricing inventory used. 
```
python utils/refresh_instance_list.py
```

### Credits
[ec2instances.info](https://ec2instances.info) for providing a well defined structured inventory of EC2 pricing.