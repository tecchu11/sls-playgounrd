.PHONY: install

install:
	-@asdf plugin add python
	-@asdf plugin add nodejs
	-@asdf plugin add pre-commit
	@asdf install
	@npm ci
	@asdf reshim python
	@pip install pipenv
	@pipenv sync -d
	@pre-commit install
