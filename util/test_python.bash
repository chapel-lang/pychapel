#!/usr/bin/env bash
#
# Run the python unittests for code in docs/source/examples/.
set -e

CWD=$(cd $(dirname $0) ; pwd)
source $CWD/common.bash

export CHPL_HOME=$REPO_ROOT/chapel-src
CHPL_GIT_URL=${CHPL_GIT_URL:-git://github.com/chapel-lang/chapel.git}
CHPL_GIT_BRANCH=${CHPL_GIT_BRANCH:-master}

log_info "Cloning Chapel source (branch: ${CHPL_GIT_BRANCH} repo: ${CHPL_GIT_URL}) into: ${CHPL_HOME}"
git clone --branch $CHPL_GIT_BRANCH $CHPL_GIT_URL $CHPL_HOME

log_info "Moving to: ${CHPL_HOME}"
cd $CHPL_HOME

log_info "Building Chapel"
export CHPL_LIBMODE=shared
source util/quickstart/setchplenv.bash && \
    make -j

# Install python dependencies for running the tests (not building the docs).
log_info "Installing python test dependencies."
pip install -r $TST_DIR/requirements.txt

(
    log_info "Moving to: ${MODULE_DIR}"
    cd $MODULE_DIR

    log_info "Installing pychapel from setup.py"
    python setup.py install
)

log_info "Running pych --check"
pych --check

# Copying pyChapel libchpl dependencies
cp $CHPL_HOME/lib/linux64*/* $VIRTUAL_ENV/share/pych/lib/

log_info "Moving to: ${REPO_ROOT}"
cd $REPO_ROOT

num_procs=`python -c "import multiprocessing; print(multiprocessing.cpu_count())"`
log_info "Number of CPUs to use for parallel testing = $num_procs"

log_info "Running py.test over $TST_DIR and doc examples"
py.test --verbose --junitxml=$REPO_ROOT/python-results.xml -n $num_procs --boxed $TST_DIR docs/source/examples/
# we run with pytest-xdist's --boxed flag so that the tests run independently
# of each other (this prevents materialization conflicts and the segfault I
# noticed with larger materializations)

log_info "Running pych --testing..."
pych --testing
