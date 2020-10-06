# from

from instance_list import get_list_of_instances


def give_best_recommendation(required_resources, instance_df):
    pass


def display_output(output):
    print(output)


if __name__ == "__main__":
    constraints = {
        "vcpu": {
            "min": 4,
            "max": 16
        }
    }

    instance_df = get_list_of_instances(constraints)

    required_resources = {
        "vcpu": 200,
        "mem": 500
    }

    output = give_best_recommendation(required_resources, instance_df)
    display_output(output)
