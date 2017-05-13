## Description
This is a AWS lambda function, used to catch CloudWatch event: ECS task STOPPED,
send notification to Slack channel and store it to Elasticsearch.
Inspired by official AWS blog post [Monitor Cluster State with Amazon ECS Event Stream](https://aws.amazon.com/blogs/compute/monitor-cluster-state-with-amazon-ecs-event-stream/)
## Usage
Complete setup requires a few AWS steps you need to follow, before you can use your Lambda function,
Setup AWS CloudWatch event, configure SNS, Role, permissions, etc...
Follow the step by step guide from official [AWS blog post](https://aws.amazon.com/blogs/compute/monitor-cluster-state-with-amazon-ecs-event-stream/)

**IMPORTANT**
In blog post , guys from AWS have few bugs :)
So in section 'Configure Function', keep in mind that for Lambda Handler you need to set like this your_python_file_name.method_in_file
Other wise you will get cannot import module error, [check stackoverflow answer](https://www.google.rs/search?q=lambda+canot+import+module&oq=lambda+canot+import+module&aqs=chrome..69i57.3778j0j7&sourceid=chrome&ie=UTF-8)
You must install all deps using pip install and zip it with your package.
Keep in mind that .py file should be at root level when you do package zipping.
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
