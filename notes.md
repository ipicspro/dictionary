dictionary


https://code.tutsplus.com/tutorials/how-to-write-your-own-python-packages--cms-26076
https://code.tutsplus.com/tutorials/how-to-write-package-and-distribute-a-library-in-python--cms-28693

www.github.com	homedrms@gmail.com	Hyr65sd43hey2U93	ipicspro

> make new env
python -m venv env

> collect dependencies
pip freeze > requirements.txt



>Make package distribution

> test
python setup.py test




> create distribution:

> * create a source distribution - (wheel)
python setup.py bdist_wheel

> or - older method
> create a source distribution - (eggs)
python setup.py sdist




> install package from github
git clone https://ipicspro@github.com/ipicspro/dictionary.git
pip install --upgrade dictionary/dist/dictionary-0.1-py3-none-any.whl
or
sudo python setup.py install
or 
pip install git+https://github.com/ipicspro/dictionary.git#egg=dictionary
*pip install --upgrade git+https://github.com/ipicspro/dictionary.git#egg=dictionary

pip install --upgrade https://raw.githubusercontent.com/ipicspro/dictionary/master/dist/dictionary-0.1-py3-none-any.whl
pip install --upgrade https://github.com/ipicspro/dictionary/raw/master/dist/dictionary-0.1-py3-none-any.whl
pip install --upgrade https://githubusercontent.com/ipicspro/dictionary/blob/0e2520170236c155cf61992e214427b26e021291/dist/dictionary-0.1-py3-none-any.whl
pip install --upgrade https://github.com/ipicspro/dictionary/blob/0e2520170236c155cf61992e214427b26e021291/dist/dictionary-0.1-py3-none-any.whl
#python -m pip install https://githubusercontent.com/ipicspro/dictionary/archive/45dfb3641aa4d9828a7c5448d11aa67c7cbd7966.tar.gz#egg=django[argon2]
# pip install --upgrade https://github.com/jkbr/httpie/tarball/master
# pip install git+https://github.com/jkbr/httpie.git#egg=httpie



# git clone https://github.com/ipicspro/dictionary.git
# git clone https://ipicspro:password@github.com/ipicspro/dictionary.git

> install package from local
pip install dist/request_headers-0.1-py3-none-any.whl

pip install --upgrade https://github.com/ipicspro/dictionary/master
pip install --upgrade https://github.com/ipicspro/dictionary.git





> uninstall package
pip uninstall dictionary