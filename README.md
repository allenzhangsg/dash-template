# dash-template

A **Plotly Dash** website template for deployments on **Kubernetes**.

This template can help you deploy your dash application 
on a distributed k8s cluster with well managed background callbacks.

### Few takeaways
1. Proper Celery configuration
2. Dashboard level authorization control
3. Containerization
4. Application server (Flask) configuration

### Environment variables
1. `REDIS_URL`
in `redis://host:port` format
2. `DEPLOYENV`
if set to `Production` or `Dev`, the corresponding isolated redis queue will be used. 
Otherwise, it will use `dickcache` as the background manager, which means a non-distributed system.
3. `ACCESS_CONTROL`
in `{"dashboard1":{"user":["joe"], "group":["group1"]}}` format used to control the access to every dashboard.

If you find this project useful, please give it a lovely ⭐ :)