# indy-community-demo

This repository contains demos built using [django-indy-community](https://github.com/AnonSolutions/django-indy-community).  Please refer to this repository for framework documentation.

The master branch of this repository contains a "bare bones" application incorporating django-indy-community, using the provided UI.  To run this demo:

Open two shells, and in each shell run:

```bash
git clone https://github.com/bcgov/von-network.git
cd von-network
./manage build
./manage start
```

... and in the second shell:

```bash
git clone https://github.com/AnonSolutions/indy-community-demo.git
cd indy-community-demo/docker
./manage start
```

That's it!  Connect to (http://localhost:8000/indy/)

For more detailed instructions on running the demo, and options on running all services locally, see the [documentation in django-indy-community](https://github.com/AnonSolutions/django-indy-community/tree/master/docker).

For instructions on how to incorporate django-indo-community into your own application, [please see ./docs](./docs)


## Immunizations Consent Demo

This demo illistrates the following business scenario:

> Bob wants to enroll his child at Faber Secondary School, however Faber needs proof that the child's immunizations are up to date.  Bob need to provide the local Health Authority with Consent to release this information to Faber.

To see this demo, check out the "imms_demo" branch of this repository:

```bash
git clone https://github.com/AnonSolutions/indy-community-demo.git
cd indy-community-demo/docker
git checkout imms_demo
```

For an overview of this scenario, please see TBD link to docs to be included.

