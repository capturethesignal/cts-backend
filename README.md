# Capture the Signal' backend tools and template challenge

- [Challenge Structure](#challenge-structure)
- [Development workflow](#development-workflow)
- [Running the Backend](#running-the-backend)
- [Docker Images](#docker-images)

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
for release before each contest, unless you want to spoil the fun :-)

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
