CC = gcc
CFLAGS = $(shell python3-config --cflags)
LDFLAGS = $(shell python3-config --embed --ldflags)
PYTHONPATH_TMP = $(PYTHONPATH):/workspaces/python

rational: rational.o
	$(CC) $^ $(LDFLAGS) -o $@

rational.o: rational.c
	$(CC) $(CFLAGS) -fPIE -c $< -o $@

run:
	@PYTHONPATH=$(PYTHONPATH_TMP) ./rational

clean:
	rm -f rational rational.o