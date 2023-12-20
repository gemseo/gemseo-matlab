ARG MATLAB_VERSION

FROM mathworks/matlab:$MATLAB_VERSION

# Use root for installing in the system.
USER root

RUN  apt update \
  && apt install software-properties-common --yes \
  && add-apt-repository ppa:deadsnakes/ppa \
  && apt update \
  && apt install --yes \
                 git \
                 python3-pip \
                 python3-venv \
                 python3.9 \
                 libpython3.9 \
                 python3.10 \
                 libpython3.10 \
                 python3.11 \
                 libpython3.11 \
  && apt clean \
  && apt --yes autoremove \
  && rm -rf /var/lib/apt/lists/*

RUN  pip install 'tox<5' \
  && rm -rf $HOME/.cache/pip

# The matlabengine package from PyPI expects matlab to be installed in /usr/local/MATLAB
RUN  mkdir -p /usr/local \
  && ln -s /opt/matlab /usr/local/MATLAB

ARG MLM_LICENSE_FILE="27000@licence-matlab.pf.irt-aese.local"
ENV MLM_LICENSE_FILE=$MLM_LICENSE_FILE

# Reset for having a standard usage.
ENTRYPOINT []
CMD ["bash"]
