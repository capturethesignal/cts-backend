# Capture the Signal' backend tools and template challenge

- [Capture the Signal' backend tools and template challenge](#capture-the-signal-backend-tools-and-template-challenge)
  - [Challenge Structure](#challenge-structure)
  - [Development workflow](#development-workflow)
  - [Running the Backend](#running-the-backend)
  - [Docker Images](#docker-images)
  - [Deployment on AWS](#deployment-on-aws)

To get started and create a **new edition of the CTS**, it's advisable to
create a separate repo or branch to keeps things clean.

```bash
$ cp -R . /some/path/cts-EVENT_NAME
$ cd /some/path/cts-EVENT_NAME
$ git init
```

and continue from there. If you prefer working with branches, go with a new
branch!

## Challenge Structure

This repository is intended for the team that runs the Capture the Signal, not
for release before each contest, unless you want to spoil the fun 😉

It contains the code to run the RF-over-IP server, in a dockerized fashion (one
challenge per container). Each challenge can be customized for each competition
without rebuilding each docker image (although it'd take only a few seconds to
do).

The [cts-tools repository](https://github.com/capturethesignal/cts-tools)
contains instructions and material that can be handed out to the participants,
yet only to the participants.

The `challenges/` folder in the present repository contains the challenge
files, each in the following structure:

* `cts-signal_<N>`:
  - `bomb/` contains the GNURadio flowgraph
    + `assets/` for any static file that you need to ship with your signal
    + `requirements.pip` should you need signal-specific Python dependencies
    + `main.sh` is the main that will be launched to run the signal
    + `signal.grc` is the main flowgraph
    + `Makefile` is used to compile the flowgraph into Python code `signal.py` (this should not be checked into the repository)
    + `signal.cfg` is the configuration file referenced by the signal
  - `README.md` please be nice, document your challenge

## Development workflow
To create new signals, we suggest re-using existing ones. After all, as long as
you keep the same structure, it's just another GNURadio flowgraph to edit!

1. Make a copy of a signal that is known to work
    ```bash
    $ cp -R cts-signal_0 cts-signal_<N>
    $ cd cts-signal_<N>
    ```
2. Work on your `signal.grc` (e.g., using GNURadio Companion) and bare in mind
   that everything should be self contained within the `signal_<N>` sub-folder.
3. Test that your signal works well in GNURadio.

## Running the Backend
Just as easy as:

```bash
$ docker-compose up -d              # bring up ALL signals
$ docker-compose ps
$ docker-compose logs -f signal_0   # attach to signal_0 stdout

$ docker-compose up signal_0        # bring up one signal and do not detach

```

Now you can test it by pointing it to the right virtual frequency (i.e., port).

## Docker Images
All challenges develope so far can run on the `capturethesignal/cts-base`
image, which is based on `capturethesignal/gnuradio-mini-docker`. Both are
hosted on the Docker Hub public registry:

  * [docker.com/u/capturethesignal](https://hub.docker.com/u/capturethesignal)

but can be built locally if needed: check the [docker/](docker/) subfolder and the [phretor/gnuradio-mini-docker](https://github.com/phretor/gnuradio-mini-docker) repository.

## Deployment on AWS
We've always been using AWS to deploy our CTS backends, but of course feel free to use whatever platform you prefer, and please keep this just as a reference. If you have enough time and are willing to share, the community would be enormously grateful to anyone who will send us a pull request with a Terraform script 😉

* Computing
  * Streaming RF over IP challenges
    * 1 m5a.4xlarge instance size it depending on how many challenges/contestants will be receiving the streamed signals
      * we suggest to deploy this in any of the public sub-networks, with all ports open
      * have Docker and Docker Compose installed
      * install AWS efs-utils to mount the `/var/challenges` EFS, to which you'll `git clone` this repository, and/or any other challenges that you're willing to run
      * when AWS ECS will support port ranges, this instance could be replaced by a bunch of properly sized ECS tasks/containers
  * Score board (based on CTFd)
    * 1 Relational Database Service (RDS) database instance
      * create an initial database named `ctfd`
      * note the endpoint in the `DATABASE_URL` variable below
      * has to support JSON data types: we use MariaDB >= 10.4.18
      * we haven't had [any success with using Amazon Aurora](https://github.com/CTFd/CTFd/issues/1936) although it [should support JSON data types](https://aws.amazon.com/blogs/database/using-json-with-mysql-5-7-compatible-amazon-aurora/)
    * 1 ElastiCache Redis instance
      * note the endpoint in the `REDIS_URL` below
    * 1 Elastic File System (EFS) file system for persistent storage
      * 1 EFS access point for the uploads (e.g., `/var/uploads`)
      * 1 EFS access point for the logs (e.g., `/var/log/CTFd`)
      * 1 EFS access point for the challenges
    * 1 ECS (Elastic Container Service) Fargate cluster
      * augment the default IAM role to include access to EFS
      * 1 task definition
        * 1 container pointing to the [ctfd/ctfd](https://hub.docker.com/r/ctfd/ctfd) Docker Image (or, feel free to use ours [capturethesignal/CTFd](https://hub.docker.com/r/capturethesignal/ctfd/))
          * mount `/var/uploads` and `/var/log/CTFd` into the container and define at least these variables
          * `ACCESS_LOG = -`
          * `ERROR_LOG = -`
          * `DATABASE_URL = mysql+pymysql://admin:CHANGEME@RDS_ENDPOINT.amazonaws.com/ctfd`
          * `LOG_FOLDER = /var/log/CTFd`
          * `UPLOAD_FOLDER = /var/uploads`
          * `MAIL_USERNAME = YOUR_AWS_SES_SMTP_USER`
          * `MAIL_PASSWORD = YOUR_AWS_SES_SMTP_PASS`
          * `MAIL_PORT = 587`
          * `MAIL_SERVER = YOUR_AWS_SES_SMTP_HOST`
          * `MAIL_TLS = true`
          * `MAIL_USEAUTH = true`
          * `MAILFROM_ADDR = noreply@your.domain`
          * `REDIS_URL = redis://ELASTICACHE_ENDPOINT.cache.amazonaws.com:6379`
          * `REVERSE_PROXY = true`
          * `SECRET_KEY = CHANGEME`
          * `WORKERS = 4`
          * more info at: https://docs.ctfd.io/docs/deployment/configuration/#server-level-configuration
        * 1 service to run 1 instance of the task definition above
          * the service needs to be associated a Security Group with 8000/tcp inbound rule allowed
          * the service will receive HTTP requests from the ALB and will forward them to port 8000
          * any time you'll restart or change the service, AWS ECS will re-configure the ALB automatically, so you won't need to change anything public facing
  * Accessing the infrastructure
    * 1 micro instance to debug, test, monitor, just in case
      * we suggest to deploy this in any of the private sub-networks, with only port 22 open
      * make this accessible from the outside via a TCP/IP network load balancer

* Networking (use [this CloudFormation template](https://docs.aws.amazon.com/codebuild/latest/userguide/cloudformation-vpc-template.html))
  * 1 VPC (Virtual Private Cloud)
  * 1 Internet Gateway
  * 2 NAT Gateways
  * 2 Private sub-networks
  * 2 Public sub-networks
  * route tables
  * 1 Application Load Balancer (ALB) to the scoreboard (use HTTPS if you can, ACM SSL certificates are free)
  * 1 TCP/IP load balancer to the EC2 instance(s)
  * (recommended) host your domain on Route 53 for ease of maintenance/integration
  * make sure that you create enough security groups (SGs) and that machines/containers can reach each other, including (but not limited to):
    * the EFS instance should have a SG configured with an inbound rule that allows traffic to NFS port (2049) from
      * the 2 EC2 instances
      * the ECS container
    * the RDS instance should have a SG configured with an inbound rule that allows traffic to NFS port (2049) from the ECS container
    * the Redis instance should have a SG configured with an inbound rule that allows traffic to Redis port (6379) from the ECS container
    * the ECS task should be associated to a SG configured with inbound rules to allow traffic to port 8000/tcp (HTTP) from the ALB's SG

We're almost certain we've missed something 😇