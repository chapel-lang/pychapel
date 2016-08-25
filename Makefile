INSTALL_DIR=$(HOME)/pychdev
MODULE_DIR=module
DOC_DIR=docs

OPEN_CMD = $(shell which xdg-open 2>/dev/null || which open 2>/dev/null )

all:

run: clean deploy chapel

pych: clean deploy
	pych --check

makechapel:
	[ -d $(CHPL_HOME) ] && (cd $(CHPL_HOME) && make -j)

deploy: makechapel
	cd $(MODULE_DIR) && python setup.py install --prefix $(INSTALL_DIR)
	[ -d $(CHPL_HOME) ] && (cd $(INSTALL_DIR)/share/pych/lib && ln -s -f $(CHPL_HOME)/lib/linux64*/* .)

undeploy:
	rm -rf $(INSTALL_DIR)

upload:
	#cd $(MODULE_DIR) && python setup.py register
	cd $(MODULE_DIR) && python setup.py bdist sdist upload

chapel:
	#python $(INSTALL_DIR)/share/pych/examples/chapel.inline.multi.py
	#python $(INSTALL_DIR)/share/pych/examples/chapel.sfile.hellolib.py
	#pych --compile $(INSTALL_DIR)/share/pych/sfiles/chapel/chapel.hellolib.exported.chpl
	python $(INSTALL_DIR)/share/pych/examples/chapel.bfile.hello.py
	python $(INSTALL_DIR)/share/pych/examples/chapel.bfile.fib.py

c:
	python $(INSTALL_DIR)/share/pych/examples/c.inline.py

doc:
	cd $(DOC_DIR) && make html
ifneq ($(OPEN_CMD),)
	$(OPEN_CMD) $(DOC_DIR)/build/html/index.html
endif

test: deploy
	( export PATH=$(INSTALL_DIR)/bin:$(PATH); \
	  export PYTHONPATH=$(INSTALL_DIR)/lib/python2.7/site-packages; \
	  py.test --boxed module/testing docs/source/examples; \
	  pych --testing; \
	  rm -f `find . -type f -name "*.pyc"`; \
	  rm -rf `find . -type d -name __pycache__` )

clean:
	rm -rf $(MODULE_DIR)/build
	rm -rf $(MODULE_DIR)/dist
	rm -f $(INSTALL_DIR)/var/pych/store/c/*.so
	rm -f $(INSTALL_DIR)/var/pych/store/chapel/*.so
	rm -f /tmp/tmp*.a
	rm -f /tmp/temp-*.chpl
	rm -f /tmp/temp-*.c
	rm -f `find . -type f -name "*.pyc"`
	rm -rf `find . -type d -name __pycache__`
