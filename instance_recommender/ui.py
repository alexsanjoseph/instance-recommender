

import streamlit as st

from instance_recommender.css import current_css
from instance_recommender.recommender import best_reco
from instance_recommender.instance_list import get_list_of_instances

from instance_recommender.inventory import Inventory


def run_streamlit_ui(inventory_source_url):
    
    inventory = Inventory(source_url=inventory_source_url, refresh=True)

    st.markdown("# AWS Instance Recommender!")
    st.markdown(current_css, unsafe_allow_html=True)

    region = st.sidebar.selectbox("region", inventory.get_available_regions())

    st.sidebar.markdown("# Required Resources")

    vcpus = st.sidebar.number_input("# of cores", min_value=1, value=100)
    memory = st.sidebar.number_input("Total RAM", min_value=1, value=230)

    allowed_archs = ['x86_64', 'arm64', 'i386']
    arch = st.sidebar.selectbox("Select Architecture", allowed_archs)
    exclude_burstable = st.sidebar.checkbox("Exclude Burstables?", value=True)

    instance_regex = st.sidebar.text_input("Filter Indices by Regex(optional)")

    st.sidebar.markdown("# Constraints")

    min_vcpus, max_vcpus = st.sidebar.slider("Min/Max vCPUs for instance", value=(2, 128), min_value=1, max_value=128)
    min_memory, max_memory = st.sidebar.slider("Min/Max memory for instance", value=(2, 128), min_value=1, max_value=128)

    selected_instances = inventory.get_pricing_with_constraints({
            "region": "us-east-1",
            "vcpus": {
                "min": min_vcpus,
                "max": max_vcpus
            },
            "memory": {
                "min": min_memory,
                "max": max_memory
            },
            "exclude_burstable": exclude_burstable,
            "arch": arch,
            "region": region
        })
    selected_instances = selected_instances[selected_instances['name'].str.contains(instance_regex)]

    if selected_instances.shape[0] == 0:
        st.markdown("**Error! No instances found matching the criteria. Please relax the constraints and try again!**")
        st.stop()

    recommended_instances = best_reco(
        required_resources = {
            "memory": memory,
            "vcpus": vcpus
        },
        instance_df=selected_instances)

    total_price = round(sum(recommended_instances['units'] * recommended_instances['price']), 3)
    total_vcpus = round(sum(recommended_instances['units'] * recommended_instances['vcpus']), 3)
    total_mem = round(sum(recommended_instances['units'] * recommended_instances['memory']), 3)

    # st.markdown(f'------------------------------------------------------------------------------')
    st.markdown("## Recommendations")
    st.markdown("### Configuration")
    st.markdown(f'Total VCPUs: **{total_vcpus}**, Total Memory: **{total_mem} GB**')
    st.markdown(f'Total price for this setup: **${total_price}/hour**, **${round(total_price * 720, 3)}/month**')

    st.markdown("### Instances")
    st.dataframe(recommended_instances)

    st.markdown(f'------------------------------------------------------------------------------')
    # st.markdown(f'==============================================================================')
    st.markdown("## Details")
    st.markdown("#### Filtered Instances")
    st.dataframe(selected_instances)


