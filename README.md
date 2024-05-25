# MistrAND 7B v1

MistrAND 7B is a fine-tuned model using Mistral 7B able to generate text in Andalusian Spanish. To do so, it uses a [custom Andalusian Spanish ortography](https://jgchaparro.github.io/posts/Una-propuesta-ortogr%C3%A1fica-para-el-habla-andaluza/). This project is part of the Master's Degree Final Thesis titled `Conservational AI for endangered languages: a preservation strategy for Tsakonian Greek upon the Andalusian Spanish case`, aiming to preserve endangered languages by storing them in QLoRA adapters for unlimited use in the future.

# How to use

* Run `2. Run inference on MistrAND 7B` either locally or in Google Colab. Text can be inputed in Standard Spanish and its automatically converted 
into Andalusian Spanish.

# Requirements

* **Access to [Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) on Hugging Face**: Mistral 7B is a gated model, meaning that it is mandatory to create a HuggingFace account and accept model's usage terms.
* **A HuggingFace read or write token**: new tokens can be created within `Settings` → `Access Tokens`.

# Sections

The repository contains three main code notebooks:

* `0. Training dataset generation`: describes the data preparation using the [OASST2 dataset](https://huggingface.co/datasets/OpenAssistant/oasst2) as a basis.
* `1. Fine-tune Mistral 7B`: contains all necessary code to generate Andalusian QLoRA adapters.
* `2. Run inference on MistrAND 7B`: downloads the base model, adds MistrAND adapter and generates responses in Andalusian Spanish. 


# Links

* [Model card on HuggingFace](https://huggingface.co/jgchaparro/MistrAND-7B-v1)