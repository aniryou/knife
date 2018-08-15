#!/usr/bin/env bash

# Test
head data/enwikiquote-20170206-cirrussearch-content.json
head data/enwikiquote-20170206-cirrussearch-content.json | jq --raw-output 'select(.title!=null) | {title:.title, category:[.category[]]} | {title:.title, categories: .category | join(";")} | [.title, .categories] | @tsv'


# Complete data
touch data/enwikiquote-20170206-cirrussearch-title-categories.tsv
time $(cat data/enwikiquote-20170206-cirrussearch-content.json | jq --raw-output 'select(.title!=null) | {title:.title, category:[.category[]]} | {title:.title, categories: .category | join(";")} | [.title, .categories] | @tsv' >data/enwikiquote-20170206-cirrussearch-title-categories.tsv)


# Shell-quote
cat jq_cmd.foo | parallel --shell-quote


# Parallel with pipe
touch data/enwikiquote-20170206-cirrussearch-title-categories.tsv
time $(cat data/enwikiquote-20170206-cirrussearch-content.json | parallel --pipe jq\ --raw-output\ \'select\(.title\!\=null\)\ \|\ \{title:.title,\ category:\[.category\[\]\]\}\ \|\ \{title:.title,\ categories:\ .category\ \|\ join\(\"\;\"\)\}\ \|\ \[.title,\ .categories\]\ \|\ @tsv\'\ \>\>data/enwikiquote-20170206-cirrussearch-title-categories.tsv)


# Parallel with pipe-part
touch data/enwikiquote-20170206-cirrussearch-title-categories.tsv
time $(cat data/enwikiquote-20170206-cirrussearch-content.json | parallel --pipe-part --block 2m jq\ --raw-output\ \'select\(.title\!\=null\)\ \|\ \{title:.title,\ category:\[.category\[\]\]\}\ \|\ \{title:.title,\ categories:\ .category\ \|\ join\(\"\;\"\)\}\ \|\ \[.title,\ .categories\]\ \|\ @tsv\'\ \>\>data/enwikiquote-20170206-cirrussearch-title-categories.tsv)
