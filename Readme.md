# How to run

## Prerequisites:

- [conda](https://docs.conda.io/projects/miniconda/en/latest/)
- [ollama](https://ollama.ai/download)

## Environment setup:

### Ollama:

```sh
ollama serve
```

In different terminal window run:

```sh
ollama pull openhermes
```

### Python:

```sh
conda create -n <NAME_OF_THE_ENVIRONMENT>
conda activate <NAME_OF_THE_ENVIRONMENT>
conda install --file ./requirements_conda.txt
pip install -r ./requirements.txt
```

### Run:

```sh
ollama serve
```

In different terminal window run:

```sh
# Do not forget to activate your environment before executing this command.
python ./src/main.py --number=100 --use_expert=False --csv=game_data_with_expert.csv
```
