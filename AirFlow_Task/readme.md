

# **Django with Airflow Project**

## **Overview**
In this project, I integrated **Django** and **Airflow** to create a system that dynamically generates workflows based on data stored in a Django database. The project was split into two parts: setting up Django as the backend and configuring Airflow for workflow automation.

---

## **Part 1: Setting Up Django**

### **What I Did in Django**
1. **Created a Model for Workflow Parameters**  
   I designed a model called `Simulator` that stores essential data for workflows, including:
   - The **start date** for scheduling workflows.
   - The **schedule interval** (e.g., hourly, daily, or weekly).
   - A **KPI ID** to identify the process associated with the workflow.

   This model essentially defines how the workflows will behave.

2. **Built an API for KPI Calculations**  
   I implemented an endpoint `/simulator/kpi/` to process random inputs and return KPI values. This endpoint:
   - Accepts a random value as input.
   - Calculates a result based on a simple formula.
   - Returns the result as a JSON response.

3. **Prepared the Database**  
   I set up the database and ran migrations to create the `Simulator` table. Then, I added a few `Simulator` instances to simulate workflows.

---

## **Part 2: Airflow for Workflow Automation**

### **What I Did in Airflow**
1. **Integrated Django with Airflow**  
   I set up Airflow to read data from the Django database. To do this, I initialized the Django environment within Airflow, which allowed me to use Django ORM to fetch the `Simulator` data.

2. **Dynamic Workflow Generation**  
   I wrote a Python script in Airflow to generate DAGs dynamically:
   - Each DAG corresponds to one `Simulator` instance in the database.
   - The DAG IDs are named `simulator_dag_<id>` (e.g., `simulator_dag_1`).
   - The workflows are scheduled based on the `start_date` and `interval` fields in the `Simulator` model.

3. **Automated Tasks in DAGs**  
   Each DAG contains a task to:
   - Generate a random value.
   - Call the Django KPI API endpoint with the random value.
   - Log the response from the endpoint.

4. **Testing the Workflows**  
   I tested the workflows by starting the Airflow scheduler and triggering the DAGs through the Airflow UI. I monitored the logs to ensure the tasks were running correctly and the API calls were successful.

---

## **How It All Comes Together**
I used Django to define workflows and provide an API for processing. Airflow takes this data and automates the tasks according to the schedules defined in the database. This setup creates a powerful, flexible system for managing workflows dynamically.

