# MailTrack Test
## _Francisco José Diego Acosta_

### Structure
* `datos` : raw csv data files.
* `sql` : sql files to solved question given the data schema in `prueba_data.pdf`
* `prueba_data` : python module 
* `main.py` : execution file
* `Makefile` : execution controller

### Execution
```sh
# create the virtual environment
make create 
# install dependencies
make install
# run all (create install and run the app)
make run
```


### Usage
```
git clone https://github.com/frandiego/mailtrack_test.git
cd mailtrack_test
make run
```

