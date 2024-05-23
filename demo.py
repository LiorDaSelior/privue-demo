import json
import privue.client as client
import privue.util as util
import streamlit as st


tab1, tab2, tab3 = st.tabs(["Privatization Example", "File Privatization", "Estimation"])


### tab 1 ###
# st.session_state handling
def save_changes_tab_1():
    st.session_state["max_value"] =  st.session_state["max_value_input"]
    st.session_state["min_value"] =  min(st.session_state["min_value_input"], st.session_state["max_value"]-1)

if "start_flag_tab_1" not in st.session_state:
    st.session_state["max_value"] = 100
    st.session_state["min_value"] = 0
st.session_state["start_flag_tab_1"] = True

# header and explanation
tab1.header("Privatizing single value using SUE-LDP")
explanation_str_list = [
    "In this demo, we will present the privatization technique SUE-LDP in action.",
    "You need to specify the limits of the range from which you want to privatize values- [Min value, Max value].",
    "The range will be divided evenly into sub-sections, the number of them will be determined by the number of buckets.",
    "Lower number of buckets corresponds with lower privacy and higher accuracy.",
    "The algorithm will randomly select indexes where the value in them will be 1 - the probabilities depend on the privacy budget epsilon (0 in the other indexes).",
    "Lower epsilon value corresponds with higher privacy and lower accuracy."
]
for explanation_str in explanation_str_list:
    tab1.write(explanation_str)
tab1.markdown("***")

# privatization demo
epsilon = tab1.slider("Select epsilon value - privacy budget", min_value = 0.1, max_value=6.0, step=0.1)
min_value = tab1.number_input("Min. Value", value = st.session_state["min_value"], step = 1, key ="min_value_input", max_value=st.session_state["max_value"]-1, on_change=save_changes_tab_1)
max_value = tab1.number_input("Max. Value", value = st.session_state["max_value"], step = 1, key ="max_value_input", on_change=save_changes_tab_1)
bucket_number = int(tab1.number_input("Bucket number", value = 20, step = 1, min_value=1))
user_value = tab1.number_input("User value (to be privatized)")

if tab1.button("Run the privatization!", type="primary"):
    tab1.header("This is what leaves the user's device (Privatized value):")
    tab1.bar_chart(client.get_private_vector(epsilon, max_value, min_value, bucket_number, user_value))
    tab1.write("Table - which sub-section each index represents (high probability candidates for the original value):")
    tab1.table(util.get_granularity_dataframe(min_value, max_value, bucket_number))


### tab 2 ###
# st.session_state handling
def save_data():
    for j in range(6):
        if j in st.session_state and st.session_state[f"attr_data_{j}"] is not None:
            st.session_state[f"attr_data_{j}"] = [st.session_state[j+6*0], st.session_state[j+6*1], st.session_state[j+6*2]]
    st.session_state["attr_num_val"] = st.session_state["attr_slider"]
    st.session_state["epsilon_val"] = st.session_state["epsilon_slider"]
    try:
        st.session_state["file_input_data_str"] = st.session_state["file_input"].getvalue().decode("utf-8")
    except AttributeError:
        st.session_state["file_input_data_str"] = None
    st.session_state["file_output_data_str"] = None

if "start_flag" not in st.session_state:
    for j in range(0,6):
        st.session_state[f"attr_data_{j}"] = None
    st.session_state["attr_num_val"] = 1
    st.session_state["epsilon_val"] = 0.1
    st.session_state["attr_data_0"] = [0,100,20]
    st.session_state["file_output_data_str"] = None
st.session_state["start_flag"] = True

# header columns (header + reset button)
header_col1, header_col2 = tab2.columns([7, 1])
header_col1.header("Data Privatization Demo (SUE-LDP)")
if header_col2.button("Reset"):
    del st.session_state["start_flag"]
    st.rerun()

explanation_str_list = [
    "After you understood the privatization technique for a single record, now you will be able to privatize a whole file of records.",
    "You need to specify the same type of parameters as in the previous section, now for multiple values (up to 6 per user)."
]
for explanation_str in explanation_str_list:
    tab2.write(explanation_str)
tab2.markdown("***")

# value selection slider
tab2.write("1) Select number of values for each record:")
attr_num = tab2.slider("", value=st.session_state[f"attr_num_val"], min_value = 1, max_value=6, step=1, key="attr_slider", on_change=save_data)
tab2.markdown("***")

# json file input
tab2.write("2) Choose a JSON file (following the required format):")
file_col1, file_col2 = tab2.columns(2)
uploaded_file = file_col1.file_uploader("Choose input file here", type="json", key="file_input", on_change=save_data)

example_json_dict = {
    "worker_1": {
        "day_0":[10,20,50],
        "day_1":[5.4,30,60]
    },
    "worker_2": {
        "day_0":[7,30.2,75],
        "day_1":[6,30,40],
        "day_2":[5,30,45]
    }
}
example_data = json.dumps(example_json_dict)

file_col2.info("Required format: File must be comprised of main JSON Objects - each represents a unique user. Every user's object has nested JSON objects which represent timestamps. The numeric values for each timestamp are held in an array (consistent order for every timestamp). If a user doesn't have a record for a timestamp, it shouldn't appear in the user object. Here is an example file (3 values per user record):", icon="ℹ️")
file_col2.download_button(
    label="Download json input file example",
    data=example_data,
    file_name="example.json",
)
tab2.markdown("***")

# epsilon selection slider
tab2.write("3) Select epsilon value - privacy budget:")
tab2.info("Lower epsilon value corresponds with :green[higher] privacy and :red[lower] accuracy.", icon="❕")
epsilon = tab2.slider("", value=st.session_state[f"epsilon_val"], min_value = 0.1, max_value=6.0, step=0.1, key="epsilon_slider", on_change=save_data)
tab2.markdown("***")

# parameters selection
tab2.write("4) Choose parameters for each value (Order of appearance in the timestamp array):")
tab2.info("Lower number of buckets corresponds with :red[lower] privacy and :green[higher] accuracy.", icon="❕")
for j in range(attr_num):
    if st.session_state[f"attr_data_{j}"] is None:
        st.session_state[f"attr_data_{j}"] = [0,100,20]  
for j in range(attr_num, 6):
    st.session_state[f"attr_data_{j}"] = None
col_list = []
row_num = attr_num // 3
col_list = [tab2.columns(3) for _ in range(row_num)]
if (attr_num % 3 != 0):
    col_list.append(tab2.columns(attr_num % 3))
if len(col_list) == 0:
    total = None
total = col_list[0]
for i in range(len(col_list) - 1):
    total += col_list[(i + 1)]
row_sum = total
j = 0
if total is not None:
    for col in row_sum:
        attr_data = st.session_state[f"attr_data_{j}"]
        if attr_data is not None:
            col.subheader(f"Value {j+1} parameters:")
            col.number_input("Min. Value", value = attr_data[0], step = 1, on_change=save_data, key=j+6*0)
            col.number_input("Max. Value", value = attr_data[1], step = 1, on_change=save_data, key=j+6*1)
            col.number_input("Number of buckets", value = attr_data[2], step = 1, on_change=save_data, min_value=1, key=j+6*2)
        j += 1
        
# submit btn
def submit_btn_func():
    attr_number = st.session_state["attr_num_val"]
    min_value_per_attr_iter = [st.session_state[f"attr_data_{i}"][0] for i in range(attr_number)]
    max_value_per_attr_iter = [st.session_state[f"attr_data_{i}"][1] for i in range(attr_number)]
    bucket_amount_per_attr_iter = [st.session_state[f"attr_data_{i}"][2] for i in range(attr_number)]
    st.session_state["file_output_data_str"] = util.privatize_json_str(st.session_state["file_input_data_str"], st.session_state["epsilon_val"], max_value_per_attr_iter, min_value_per_attr_iter, bucket_amount_per_attr_iter)

if "file_input_data_str" in st.session_state and st.session_state["file_input_data_str"] is not None:
    tab2.button(
        label="Submit and privatize",
        on_click = submit_btn_func,
        type = "primary"
    )
    
if "file_output_data_str" in st.session_state and st.session_state["file_output_data_str"] is not None:
    tab2.download_button(
        label="Download privatized JSON output file",
        data=st.session_state["file_output_data_str"],
        file_name="output.json",
        type = "primary"
    )


### tab 3 ###
# header and explanation
tab3.header("Histogram and average estimation")
explanation_str_list = [
    "After privatizing your file, you can upload it here for estimation of the different values.",
    'Each value will be represented with: ',
    '1) An "average" histogram - portrays an estimation of the distribution of the actual data.',
    '2) Estimation of the average value (which was calculated using the "average" histogram).',
    '3) Table - which sub-section each index in the histogram represents (to clarify sub-section distribution).'
]
for explanation_str in explanation_str_list:
    tab3.write(explanation_str)
tab3.markdown("***")

# file upload and estimation
def present_results():
    if "privatized_file_input" in st.session_state and st.session_state["privatized_file_input"] is not None:
        json_str = st.session_state["privatized_file_input"].getvalue().decode("utf-8")
        res = util.avg_estimation_with_json_str(json_str, True)
        attr_list = json.loads(json_str)["attr_data"]
        print(res)
        tab3.write("Results:")
        value_index = 0
        for value_result in res:
            tab3.write(f"Average histogram for value {value_index+1}:")
            tab3.bar_chart(value_result[1])
            tab3.table(util.get_granularity_dataframe(attr_list[value_index][1], attr_list[value_index][0], attr_list[value_index][2]))
            tab3.write(f"Estimated average for value {value_index+1} = {value_result[0]}")
            tab3.markdown("***")
            value_index += 1
    
uploaded_privatized_file = tab3.file_uploader("Choose input file here", type="json", key="privatized_file_input", on_change=present_results)
tab3.markdown("***")