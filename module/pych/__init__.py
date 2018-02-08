# Copyright 2014-2018 Cray Inc.
# Other additional copyright holders may be indicated within.
#
# The entirety of this work is licensed under the Apache License,
# Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.
#
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
pych - The Python/Chapel interoperability module.
"""
import logging
import pych.configuration
import pych.runtime

RT = None
CONFIG = None
logging.basicConfig(                                # Setup default logging
    level=logging.ERROR,
    format="%(levelname)s:%(module)s:%(funcName)s: %(message)s"
)

try:
    CONFIG = pych.configuration.Configuration()     # Load configuration
    logging.basicConfig(                            # Setup logging
        level=CONFIG["log_level"],
        format="%(levelname)s:%(module)s:%(funcName)s: %(message)s"
    )

    RT = pych.runtime.Runtime(CONFIG)               # Setup runtime
except ValueError as exc:
    logging.error("Looks like there is an error in your configuration file.")
except IOError as exc:
    logging.error("If you are installing just now, "
                  "then ignore this error message: "
                  "Could not find config-file(pych.json), "
                  "check your installation or try re-installing.")
