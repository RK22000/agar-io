# Learning To Play By Loosing

I'm looking to apply this [paper](https://arxiv.org/abs/1704.05588) to a bot that plays [Agar.io](agar.io).

## Step 1, Build the dataset

[x] Create a script that plays Agar io by moving in a straight line.

[x] Train a model to play agar io

## Instrutions to run agar.io model

1. Clone this repository.
2. Create a conda environment from the `env.yml` file. My conda environment is a directory called `env` in the root of my project. I've so set up `.gitignore` to ignore the `env` directory in the in project root.

```sh
conda env create -p <Location of new environment> -f env.yml
    or
conda env create -n <Name of new environment> -f env.yml
```

3. Run the main2.py python script.

```sh
python main2.py # Run the game bot for one round
python main2.py -r n # Run the game bot for n rounds
python main2.py -h # Show help
```
