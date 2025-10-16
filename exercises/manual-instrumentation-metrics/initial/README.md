# otel-manual-instrumentation-lab

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/lftraining/LFS148-code) [![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/lftraining/LFS148-code)


```bash
# grep responses
python app.py | tail -n +3 | jq '.resource_metrics[].scope_metrics[].metrics[] | select (.name=="http.server.request.duration")'

# load tests
ab -n 3000 -c 200 http://127.0.0.1:5000/users
```
