**Installation:**
Requirements: 
+ pip3
+ docker
+ allure command line from [https://docs.qameta.io/allure/2.0/#_get_started]

`pip3 install -r requirements.txt` 

**Usage:**
Run tests locally with allure reporting:
`$PROJECT_HOME/bin/run_tests_locally.sh`

Run one of tests suits in Docker container:
`$PROJECT_HOME/bin/build_docker_image.sh`
`$PROJECT_HOME/bin/run_meta_tests.sh`
